from .models import User, Friend, FriendRequest

def get_pending_friend_requests(user: User):
    return FriendRequest.objects.filter(from_user=user, accepted=False)

def get_friend_list(user):
    return User.objects.filter(id__in=Friend.objects.filter(friend_1=user).values_list('friend_2', flat=True))

def get_user_by_username(username: str):
    return User.objects.get(username=username)
