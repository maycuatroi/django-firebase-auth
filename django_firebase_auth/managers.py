from firebase_admin import auth

from abstract_auth.abstract_user_manager import AbstractUserManager


class FirebaseUserManager(AbstractUserManager):
    def _service_create_user(
        self, email, password, phone_number=None, display_name=None
    ):
        auth_user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            disabled=False,
            **phone_number and {"phone_number": str(phone_number)},
            **display_name and {"display_name": display_name},
        )
        return auth_user
