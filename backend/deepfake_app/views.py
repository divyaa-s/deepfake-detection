from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import os

from .models import VideoUpload, DetectionResult, DeepfakeImage, AwarenessContent, Report
from .serializers import VideoUploadSerializer, DetectionResultSerializer, AwarenessContentSerializer, ReportSerializer
from .deepfake_detection import generate_gradcam_and_ensemble_predict  # Import your detection function

# Helper function to handle uploaded files
def handle_uploaded_file(file):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    img_path = os.path.join(upload_dir, file.name)
    with open(img_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return img_path

# API endpoint to upload media (image or video)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_media(request):
    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        return Response({"error": "No file uploaded"}, status=400)

    file_type = uploaded_file.content_type

    if 'video' in file_type:
        # Save video file
        video = VideoUpload(video=uploaded_file)
        video.save()
        return Response({"message": "Video uploaded successfully", "video_id": video.id}, status=201)

    elif 'image' in file_type:
        # Save image and run detection
        image_path = handle_uploaded_file(uploaded_file)

        # Call the deepfake detection function
        prediction, confidence, grad_cam_path = generate_gradcam_and_ensemble_predict(request,image_path)

        # Save result in the database
        deepfake_image = DeepfakeImage(image=uploaded_file, prediction=prediction, confidence=confidence)
        deepfake_image.save()

        return Response({
            "message": "Image uploaded and analyzed successfully",
            "prediction": prediction,
            "confidence": confidence,
            'grad_cam_path': grad_cam_path  # Include the Grad-CAM image path in the response
        }, status=201)

    else:
        return Response({"error": "Unsupported file type. Only image and video files are allowed."}, status=400)

# API to retrieve deepfake detection results for a file
@api_view(['GET'])
def get_results(request, file_id):
    """ API to retrieve deepfake detection results for a file """
    try:
        result = DeepfakeImage.objects.get(id=file_id)  # This can be extended for video results
        return Response({
            "prediction": result.prediction,
            "confidence": result.confidence,
            'grad_cam_path': result.grad_cam_path,  # Include the Grad-CAM image path in the response
        })
    except DeepfakeImage.DoesNotExist:
        return Response({"error": "No results found for the given file ID"}, status=404)

# API endpoint to trigger analysis after file upload (for reuse or after file upload)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_uploaded_file(request):
    """
    API to analyze the uploaded file and return deepfake prediction and confidence.
    This can be used to re-trigger analysis after file upload.
    """
    file_id = request.data.get("file_id")  # The ID of the uploaded file to analyze
    if not file_id:
        return Response({"error": "File ID is required"}, status=400)

    # Fetch the uploaded file based on the ID (for image)
    try:
        deepfake_image = DeepfakeImage.objects.get(id=file_id)
    except DeepfakeImage.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

    # Perform analysis (assuming you've saved the image previously)
    image_path = os.path.join(settings.MEDIA_ROOT, deepfake_image.image.name)
    prediction, confidence, grad_cam_path = generate_gradcam_and_ensemble_predict(request, image_path)

    # Update the result in the database
    deepfake_image.prediction = prediction
    deepfake_image.confidence = confidence
    deepfake_image.save()

    return Response({
        "prediction": prediction,
        "confidence": confidence,
        'grad_cam_path': grad_cam_path,  # Include the Grad-CAM image path in the response
        "message": "Analysis completed successfully."
    })

# ✅ 1. Login / Signup Page
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "message": "Signup successful"})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "Login successful"})
    return Response({"error": "Invalid credentials"}, status=400)

# ✅ 1. User Dashboard - Fetch uploaded videos
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """ Fetch all videos uploaded by the authenticated user """
    user = request.user
    videos = VideoUpload.objects.filter(user=user)
    serializer = VideoUploadSerializer(videos, many=True)
    return Response(serializer.data)

# ✅ 2. Awareness Content - Fetch deepfake awareness articles
@api_view(['GET'])
def awareness_content(request):
    """ Fetch awareness articles on deepfake detection and misinformation """
    content = AwarenessContent.objects.all()
    serializer = AwarenessContentSerializer(content, many=True)
    return Response(serializer.data)

# ✅ 3. User Reports - Fetch past deepfake detection reports
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reports(request):
    """ Fetch all deepfake detection reports for the authenticated user """
    user = request.user
    reports = Report.objects.filter(user=user)
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)

