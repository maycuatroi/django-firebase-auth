# Guidelines

This document provides general guidance for using `django-firebase-auth` in your projects.

## Requirements

- Python 3.8+
- Django and Django REST Framework
- Either Firebase or Supabase credentials

## Setting up Credentials

1. **Firebase**
   - Store the service account JSON locally and define `FIREBASE_CREDENTIALS_FILE` in `settings.py`.
   - Alternatively place the JSON content in a dictionary and assign it to `FIREBASE_CREDENTIALS_DICT`.

2. **Supabase**
   - Set `SUPABASE_URL` and `SUPABASE_KEY` in `settings.py` to enable Supabase authentication.

## Installed Apps

Add the provided apps to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django_firebase_auth",
    "django_supabase_auth",  # optional for Supabase
]
```

Run `python manage.py migrate` to create the profile tables.

## Authentication Classes

`FirebaseAuthentication` is a subclass of `rest_framework.authentication.BaseAuthentication`. To use it with Django REST Framework, configure:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "django_firebase_auth.firebase_auth.FirebaseAuthentication",
    ),
}
```

## Login Endpoint

The package exposes a login endpoint via `django_firebase_auth.urls`. Include it in your project urls:

```python
urlpatterns = [
    # ...
    path("firebase-auth/", include("django_firebase_auth.urls")),
]
```

The login view expects a `firebase_auth_token` in the request body and returns the authenticated user.

