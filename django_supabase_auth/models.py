from django.db import models

from abstract_auth.abstract_user_profile import AbstractUserProfile


class SupabaseUserProfile(models.Model, AbstractUserProfile):
    pass
