from .models import User, Friend, FriendRequest, StatusChoices


def get_pending_friend_requests(user: User):
    return FriendRequest.objects.filter(to_user=user, status=StatusChoices.PENDING)

def get_friend_list(user):
    return User.objects.filter(id__in=Friend.objects.filter(friend_1=user).values_list('friend_2', flat=True))

def get_user_by_username(username: str):
    return User.objects.get(username=username)

def get_friend_request_by_id(friend_request_id: int):
    return FriendRequest.objects.filter(id=friend_request_id).first()

