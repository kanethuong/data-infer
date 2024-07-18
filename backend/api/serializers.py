from rest_framework import serializers
from .models import UploadedFile, ProcessedData


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"


class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = "__all__"
