from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),  # Include the viewset routes
    path('clients/<int:client_id>/projects/', ProjectViewSet.as_view({'post': 'create'})),
]
