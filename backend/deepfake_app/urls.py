from django.urls import path
from .views import upload_video, get_results

urlpatterns = [
    path('upload/', upload_video, name="upload_video"),
    path('results/<int:video_id>/', get_results, name="get_results"),
]
