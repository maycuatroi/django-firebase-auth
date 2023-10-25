from django.db import models

from abstract_auth.abstract_user_profile import AbstractUserProfile


class UserFirebaseProfile(models.Model, AbstractUserProfile):
    class Meta:
        app_label = 'django_firebase_auth'
