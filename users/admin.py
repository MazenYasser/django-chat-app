from django.contrib import admin
from users.models import User, Friend, FriendRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "date_joined", "is_online", "is_active", "is_staff", "is_superuser"]

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["__str__", "accepted"]
    list_editable = ["accepted"]
    
    