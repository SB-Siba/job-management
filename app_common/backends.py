# your_app/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import User  # Adjust this import based on your project structure

class EmailOrContactBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Determine if the username is an email or contact number
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(contact=username)
        except User.DoesNotExist:
            return None

        # Check if the password is correct
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
