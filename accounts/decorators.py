from django.core.exceptions import PermissionDenied


# RESTRICT THE VENDOR FROM ACCESSING THE CUSTOMER PAGE
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# RESTRICT THE customer FROM ACCESSING THE vendor PAGE
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
