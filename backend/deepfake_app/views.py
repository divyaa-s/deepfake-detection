from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from .models import VideoUpload, DetectionResult
from .serializers import VideoUploadSerializer, DetectionResultSerializer
import os

@api_view(['POST'])
def upload_video(request):
    """ API to upload a video for deepfake detection """
    video_file = request.FILES.get('video')
    if not video_file:
        return Response({"error": "No video uploaded"}, status=400)

    video_instance = VideoUpload(video=video_file)
    video_instance.save()
    
    return Response({"message": "Video uploaded successfully", "video_id": video_instance.id})

@api_view(['GET'])
def get_results(request, video_id):
    """ API to retrieve deepfake detection results for a video """
    try:
        results = DetectionResult.objects.filter(video_id=video_id)
        serializer = DetectionResultSerializer(results, many=True)
        return Response(serializer.data)
    except DetectionResult.DoesNotExist:
        return Response({"error": "No results found"}, status=404)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import VideoUpload, DetectionResult, AwarenessContent, Report
from .serializers import VideoUploadSerializer, DetectionResultSerializer, AwarenessContentSerializer, ReportSerializer

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


from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import VideoUpload, DetectionResult, AwarenessContent, Report
from .serializers import VideoUploadSerializer, DetectionResultSerializer, AwarenessContentSerializer, ReportSerializer

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
