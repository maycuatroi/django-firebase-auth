from abstract_auth.abstract_user_profile import AbstractAuthProfile


class UserFirebaseProfile(AbstractAuthProfile):
    class Meta:
        app_label = "django_firebase_auth"
        abstract = False
