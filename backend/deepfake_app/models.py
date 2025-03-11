from django.db import models
from django.contrib.auth.models import User

# Video Upload Model
class VideoUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values temporarily
    video = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Deepfake Detection Result Model
class DetectionResult(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    is_fake = models.BooleanField()
    confidence_score = models.FloatField()
    heatmap_image = models.ImageField(upload_to="heatmaps/", null=True, blank=True)

# Awareness Content Model
class AwarenessContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# History & Report Storage
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to="reports/")
    created_at = models.DateTimeField(auto_now_add=True)
