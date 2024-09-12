# quotation/decorators.py

from django.contrib.auth.decorators import user_passes_test

def super_admin_only(function=None):
    """
    Decorator for views that checks that the user is a superadmin,
    redirects to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
