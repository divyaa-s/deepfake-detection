import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms
from facenet_pytorch import MTCNN
from timm import create_model
import torch.nn as nn
from skimage.feature import local_binary_pattern
import cv2
from pytorch_grad_cam import GradCAM, EigenCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import os
import uuid
from django.conf import settings
import matplotlib.pyplot as plt


device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=False, device=device)


# ---------- Feature Extraction Functions ----------

def extract_lbp(face_image):
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray, P=8, R=1, method='uniform')
    lbp_hist = np.histogram(lbp.ravel(), bins=np.arange(0, 59), range=(0, 58))
    return lbp_hist[0]

def extract_eye_reflection(face_image, detector):
    if isinstance(face_image, Image.Image):
        face_image = np.array(face_image)

    boxes, probs = detector.detect(face_image)
    if boxes is None or len(boxes) == 0:
        return np.zeros(10)

    x1, y1, x2, y2 = map(int, boxes[0])
    
    # Make sure the box is within bounds
    h, w = face_image.shape[:2]
    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))
    
    face = face_image[y1:y2, x1:x2]

    # Return zeros if crop is invalid
    if face.size == 0 or face.shape[0] < 10 or face.shape[1] < 10:
        return np.zeros(10)

    gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    eye_reflections = []
    for (ex, ey, ew, eh) in eyes:
        eye_roi = face[ey:ey+eh, ex:ex+ew]
        avg_intensity = np.mean(eye_roi)
        eye_reflections.append(avg_intensity)

    while len(eye_reflections) < 10:
        eye_reflections.append(0.0)

    return np.array(eye_reflections[:10])


def extract_skin_texture_features(face_image):
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)
    laplacian = cv2.Laplacian(enhanced_gray, cv2.CV_64F)
    laplacian_var = laplacian.var()
    return np.array([laplacian_var], dtype=np.float32)


# ---------- Model and GradCAM Setup ----------

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


# ---------- Main Grad-CAM + Prediction Function ----------

def generate_gradcam_and_ensemble_predict(request, img_path):
    # Load models
    x_model, x_layer, x_size = load_model("xception", "D:/Projects/Minor Project/Deepfake Detection/models/xceptionnet_20k.pth", (299, 299))
    v_model, v_layer, v_size = load_model("vit_tiny_patch16_224", "D:/Projects/Minor Project/Deepfake Detection/models/vit_deit_tiny_5epochs.pth", (224, 224))
    e_model, e_layer, e_size = load_model("efficientnet_b3", "D:/Projects/Minor Project/Deepfake Detection/models/efficientnet_b3_model.pth", (300, 300))
    c_model, c_layer, c_size = load_model("convnext_tiny", "D:/Projects/Minor Project/Deepfake Detection/models/convnext_tiny_deepfake.pth", (224, 224))

    # Detect face and get crop
    face_crop, original_image = crop_face_and_get_original(img_path)
    if face_crop is None:
        return "No face detected", 0.0, None, None, None, None

    # Extract features
    lbp_features = extract_lbp(face_crop)
    lbp_features = (lbp_features - lbp_features.min()) / (lbp_features.max() - lbp_features.min() + 1e-5)  # Normalizing LBP features

    eye_reflection_features = extract_eye_reflection(face_crop, mtcnn)
    eye_reflection_features = eye_reflection_features / (np.max(eye_reflection_features) + 1e-5)  # Normalizing eye reflection features

    skin_texture_features = extract_skin_texture_features(face_crop)

    # Preprocess for models
    x_tensor = preprocess_for_model(face_crop, x_size)
    v_tensor = preprocess_for_model(face_crop, v_size)
    e_tensor = preprocess_for_model(face_crop, e_size)
    c_tensor = preprocess_for_model(face_crop, c_size)

    # Perform predictions
    with torch.no_grad():
        x_out = F.softmax(x_model(x_tensor), dim=1)
        v_out = F.softmax(v_model(v_tensor), dim=1)
        e_out = F.softmax(e_model(e_tensor), dim=1)
        c_out = F.softmax(c_model(c_tensor), dim=1)

    outputs = [x_out, v_out, e_out, c_out]
    all_probs = [out[0].tolist() for out in outputs]

    avg_real_prob = sum([p[0] for p in all_probs]) / len(all_probs)
    avg_fake_prob = sum([p[1] for p in all_probs]) / len(all_probs)
    final_pred = 0 if avg_real_prob > avg_fake_prob else 1
    confidence = avg_real_prob if final_pred == 0 else avg_fake_prob

    confs = {
        "XceptionNet": x_out[0][final_pred].item(),
        "ViT": v_out[0][final_pred].item(),
        "EfficientNet-B3": e_out[0][final_pred].item(),
        "ConvNeXt": c_out[0][final_pred].item()
    }
    best_model = max(confs, key=confs.get)
    label = "Uncertain" if confidence < 0.5 else ("Real" if final_pred == 0 else "Fake")

    # Grad-CAM Setup
    model, layer, tensor, input_size = {
        "XceptionNet": (x_model, x_layer, x_tensor, x_size),
        "ViT": (v_model, v_layer, v_tensor, v_size),
        "EfficientNet-B3": (e_model, e_layer, e_tensor, e_size),
        "ConvNeXt": (c_model, c_layer, c_tensor, c_size),
    }[best_model]

    cam_method = EigenCAM if best_model == "ViT" else GradCAM
    resized_full_image = cv2.resize(original_image, input_size)
    rgb_norm = np.float32(resized_full_image) / 255.0

    cam = cam_method(model=model, target_layers=[layer])
    visuals = []
    for class_idx in [0, 1]:
        grayscale_cam = cam(input_tensor=tensor, targets=[ClassifierOutputTarget(class_idx)])[0]
        vis = show_cam_on_image(rgb_norm, grayscale_cam, use_rgb=True, colormap=cv2.COLORMAP_JET)
        visuals.append((class_idx, vis))

    # Save Grad-CAM visualization
    grad_cam_dir = os.path.join(settings.MEDIA_ROOT, "grad_cams")
    os.makedirs(grad_cam_dir, exist_ok=True)

    filename = f"gradcam_{uuid.uuid4().hex}_{label}_{confidence:.2f}.jpg"
    grad_cam_path = os.path.join(grad_cam_dir, filename)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    for i, (cls, vis) in enumerate(visuals):
        axs[i].imshow(vis)
        axs[i].set_title(f"Grad-CAM for class: {'Real' if cls == 0 else 'Fake'}")
        axs[i].axis("off")
    plt.tight_layout()
    plt.savefig(grad_cam_path)
    plt.close()

    grad_cam_url = settings.MEDIA_URL + f"grad_cams/{filename}"
    grad_cam_full_url = request.build_absolute_uri(grad_cam_url)

    return label, confidence, grad_cam_full_url, lbp_features, eye_reflection_features, skin_texture_features
