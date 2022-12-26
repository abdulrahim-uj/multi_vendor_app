from django.shortcuts import get_object_or_404

from accounts.models import UserProfile


def get_user(request):
    try:
        user = UserProfile.objects.get(user=request.user)
    except:
        user = None
    return {
        "user_data": user,
    }
