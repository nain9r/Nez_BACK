from django.urls import path
from .views import AudioFileUploadView, TextUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', AudioFileUploadView.as_view(), name='upload-audio-file'),
    path('uploadText/', TextUploadView.as_view(), name='upload-text'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
