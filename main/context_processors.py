import datetime

from main.functions import get_client_ip
from main.functions import get_timezone


def main_context(request):
    today = datetime.date.today()
    client_location = get_client_ip(request)
    timezone_user = get_timezone(request)
    return {
        "app_title": "Online Food App",
        'domain': request.META['HTTP_HOST'],
        "today": today,
        'user_zone': timezone_user,
        'user_location': client_location,
    }
