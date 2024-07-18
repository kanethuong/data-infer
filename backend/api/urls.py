from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet, ProcessedDataViewSet

router = DefaultRouter()
router.register(r'uploaded-files', UploadedFileViewSet, basename='uploadedfile')

urlpatterns = [
    path('', include(router.urls)),
]
