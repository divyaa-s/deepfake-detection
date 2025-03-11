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
