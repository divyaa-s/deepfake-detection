from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login, name="login"),
    path('dashboard/', user_dashboard, name="user_dashboard"),

    path('upload/', upload_media, name='upload_media'),
    path('results/<int:video_id>/', get_results, name="get_results"),
    path('awareness/', awareness_content, name="awareness_content"),
    path('history/', user_reports, name="user_reports"),
]   

