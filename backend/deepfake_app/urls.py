from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('dashboard/', user_dashboard, name="user_dashboard"),
<<<<<<< HEAD
    path('upload/', upload_video, name="upload_video"),
    path('results/<int:video_id>/', get_results, name="get_results"),
    path('awareness/', awareness_content, name="awareness_content"),
    path('history/', user_reports, name="user_reports"),
]
=======
    path('upload/', upload_media, name='upload_media'),
    path('results/<int:video_id>/', get_results, name="get_results"),
    path('awareness/', awareness_content, name="awareness_content"),
    path('history/', user_reports, name="user_reports"),
]   

>>>>>>> c7dfa4cfcdede1fcd2066c566de0bca809c29666
