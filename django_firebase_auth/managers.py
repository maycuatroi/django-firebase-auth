from django.contrib.auth.models import UserManager as DefaultUserManager
from firebase_admin import auth


class UserManager(DefaultUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        phone_number = extra_fields.get("phone_number", None)
        display_name = extra_fields.get("display_name", None)
        auth_user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            disabled=False,
            **phone_number and {"phone_number": str(phone_number)},
            **display_name and {"display_name": display_name},
        )
        user = self.model(id=auth_user.uid, email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
