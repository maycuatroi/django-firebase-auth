import abc

from django.contrib.auth.models import UserManager as DefaultUserManager


class AbstractUserManager(DefaultUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        phone_number = extra_fields.get("phone_number", None)
        display_name = extra_fields.get("display_name", None)
        auth_user = self._service_create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            display_name=display_name,
        )
        user = self.model(id=auth_user.uid, email=email, **extra_fields)
        user.save(using=self._db)
        return user

    @abc.abstractmethod
    def _service_create_user(
        self, email, password, phone_number=None, display_name=None
    ):
        raise NotImplementedError("This method should be implemented in child class")

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
