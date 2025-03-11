from rest_framework import serializers
from .models import VideoUpload, DetectionResult

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = '__all__'

class DetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = '__all__'
