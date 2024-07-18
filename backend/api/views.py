from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedFile, ProcessedData
from .serializers import UploadedFileSerializer, ProcessedDataSerializer
from api.file_reader import read_file
from api.type_infer import infer_data_types
from .exceptions import UnsupportedFileFormatError
import pandas as pd


class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_path = file_serializer.instance.file.path
            try:
                df = read_file(file_path)
                inferred_types = {}
                for col in df.columns:
                    inferred_types[col] = str(infer_data_types(df[col]))
                return Response(
                    {"inferred_types": inferred_types}, status=status.HTTP_201_CREATED
                )
            except UnsupportedFileFormatError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessedDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProcessedData.objects.all()
    serializer_class = ProcessedDataSerializer
