import torch
import timm
from torchvision import transforms
from PIL import Image

# Load model globally to avoid reloading each time
def load_model():
    model = timm.create_model("efficientnet_b3a.ra2_in1k", pretrained=False, num_classes=2)
    model.load_state_dict(torch.load("models/efficientnet_b3_model.pth", map_location=torch.device("cpu")))
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image_label(image):
    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        predicted_class = torch.argmax(outputs, dim=1).item()
        return 'real' if predicted_class == 1 else 'fake'
