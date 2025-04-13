import torch
import torch.nn.functional as F  # Importing functional to use softmax
import numpy as np
from PIL import Image
from torchvision import transforms
from facenet_pytorch import MTCNN
from timm import create_model
import torch.nn as nn
from django.conf import settings
import os
import uuid


# Device setup
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# MTCNN face detector
mtcnn = MTCNN(keep_all=False, device=device)

def crop_face_and_get_original(img_path):
    img = Image.open(img_path).convert('RGB')
    img_cv = np.array(img)
    boxes, _ = mtcnn.detect(img)

    if boxes is not None:
        box = boxes[0].astype(int)
        x1, y1, x2, y2 = box
        face_crop = img_cv[y1:y2, x1:x2]
        return face_crop, img_cv
    else:
        print("⚠️ Face not detected!")
        return None, None

def preprocess_for_model(face_img, input_size):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(input_size),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])
    tensor = transform(Image.fromarray(face_img)).unsqueeze(0)
    return tensor.to(device)

def get_last_conv_layer(model):
    for name, module in reversed(list(model.named_modules())):
        if isinstance(module, nn.Conv2d):
            print(f"[OK] Using layer: {name}")
            return module
    raise ValueError("❌ No Conv2d layer found.")

def load_model(model_name, weight_path, input_size):
    model = create_model(model_name, pretrained=False, num_classes=2)
    model.load_state_dict(torch.load(weight_path, map_location=device))
    model.eval().to(device)
    conv_layer = get_last_conv_layer(model)
    return model, conv_layer, input_size

from pytorch_grad_cam import GradCAM, EigenCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import cv2
from matplotlib import pyplot as plt
import os
from django.conf import settings
import os


def generate_gradcam_and_ensemble_predict(request, img_path):
    """
    Generate Grad-CAM visualization based on ensemble prediction from multiple models (XceptionNet, ViT, EfficientNet-B3).
    """
    # Load models
    x_model, x_layer, x_size = load_model("xception", "D:/Projects/Minor Project/Deepfake Detection/models/xceptionnet_20k.pth", (299, 299))
    v_model, v_layer, v_size = load_model("vit_tiny_patch16_224", "D:/Projects/Minor Project/Deepfake Detection/models/vit_deit_tiny_5epochs.pth", (224, 224))
    e_model, e_layer, e_size = load_model("efficientnet_b3", "D:/Projects/Minor Project/Deepfake Detection/models/efficientnet_b3_model.pth", (300, 300))

    # Get face and full image
    face_crop, original_image = crop_face_and_get_original(img_path)
    if face_crop is None:
        return "No face detected", 0.0, None

    # Preprocess the face crop for each model
    x_tensor = preprocess_for_model(face_crop, x_size)
    v_tensor = preprocess_for_model(face_crop, v_size)
    e_tensor = preprocess_for_model(face_crop, e_size)

    # Make predictions
    with torch.no_grad():
        x_out = F.softmax(x_model(x_tensor), dim=1)
        v_out = F.softmax(v_model(v_tensor), dim=1)
        e_out = F.softmax(e_model(e_tensor), dim=1)

    # Average output of all models (Ensemble Prediction)
    avg_output = (x_out + v_out + e_out) / 3
    final_pred = torch.argmax(avg_output).item()
    final_label = "Real" if final_pred == 0 else "Fake"
    confidence = avg_output[0][final_pred].item()

    # Best model selection based on confidence
    confs = {
        "XceptionNet": x_out[0][final_pred].item(),
        "ViT": v_out[0][final_pred].item(),
        "EfficientNet-B3": e_out[0][final_pred].item()
    }
    best_model = max(confs, key=confs.get)

    # Assign the label here
    label = final_label  # This line should assign the label before using it below

    # Choose model and cam method
    if best_model == "XceptionNet":
        model, layer, tensor, input_size = x_model, x_layer, x_tensor, x_size
        cam_method = GradCAM
    elif best_model == "ViT":
        model, layer, tensor, input_size = v_model, v_layer, v_tensor, v_size
        cam_method = EigenCAM
    else:
        model, layer, tensor, input_size = e_model, e_layer, e_tensor, e_size
        cam_method = GradCAM

    # Resize image
    resized_full_image = cv2.resize(original_image, input_size)
    rgb_norm = np.float32(resized_full_image) / 255.0

    # Generate Grad-CAM visualizations for both classes
    cam = cam_method(model=model, target_layers=[layer])
    visuals = []
    for class_idx in [0, 1]:
        grayscale_cam = cam(input_tensor=tensor, targets=[ClassifierOutputTarget(class_idx)])[0]
        vis = show_cam_on_image(rgb_norm, grayscale_cam, use_rgb=True, colormap=cv2.COLORMAP_JET)
        visuals.append((class_idx, vis))

    # Create directory if not exists
    grad_cam_dir = os.path.join(settings.MEDIA_ROOT, "grad_cams")
    os.makedirs(grad_cam_dir, exist_ok=True)

    # Generate a unique filename
    filename = f"gradcam_{uuid.uuid4().hex}_{label}_{confidence:.2f}.jpg"
    grad_cam_path = os.path.join(grad_cam_dir, filename)

    # Save image
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    for i, (cls, vis) in enumerate(visuals):
        label = "Real" if cls == 0 else "Fake"
        axs[i].imshow(vis)
        axs[i].set_title(f"Grad-CAM for class: {label}")
        axs[i].axis("off")
    plt.tight_layout()
    plt.savefig(grad_cam_path)
    plt.close()

    # Generate the public URL
    grad_cam_url = settings.MEDIA_URL + f"grad_cams/{filename}"
    grad_cam_full_url = request.build_absolute_uri(grad_cam_url)

    return label, confidence, grad_cam_full_url
