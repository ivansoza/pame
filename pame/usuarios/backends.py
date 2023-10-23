from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)

        if user and user.has_active_session:
            return None  

        if user:
            user.has_active_session = True 
            user.save()

        return None


