from django.shortcuts import render
from rest_framework import viewsets
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated

class RatingViewSet(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer
    permission_classes = [IsAuthenticated]

    