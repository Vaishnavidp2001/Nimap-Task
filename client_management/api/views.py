from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Client ViewSet for handling clients
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Assign the logged-in user as the creator

    # Custom action to fetch projects assigned to logged-in users
    @action(detail=False, methods=['get'], url_path='assigned-projects')
    def get_assigned_projects(self, request):
        user_projects = Project.objects.filter(users=request.user)
        serializer = ProjectSerializer(user_projects, many=True)
        return Response(serializer.data)

# Project ViewSet for handling projects within clients
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client = Client.objects.get(id=self.kwargs['client_id'])
        serializer.save(client=client, created_by=self.request.user)  # Assign the client and creator
