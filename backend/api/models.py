from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ProcessedData(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)
    inferred_type = models.CharField(max_length=255)
