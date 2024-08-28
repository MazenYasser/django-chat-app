from django.urls import path
from .views import UserViewSet, FriendRequestViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
router.register("friend-requests", FriendRequestViewset, basename="friend-requests")

urlpatterns = [
    
] + router.urls


