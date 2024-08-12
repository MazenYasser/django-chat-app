from django.contrib import admin
from users.models import User, Friend, FriendRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass