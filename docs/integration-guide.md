# Integration Guide

This guide explains how to integrate `django-firebase-auth` into an existing Django project.

## 1. Install the Package

```bash
pip install django-firebase-auth
```

## 2. Create Credentials

Generate a Firebase service account or configure Supabase credentials. For Firebase you can download a JSON key from the Firebase console. Supabase requires the project URL and service key.

## 3. Update `settings.py`

Add credentials and apps:

```python
# Firebase
FIREBASE_CREDENTIALS_FILE = '/path/to/service-account.json'
# or
FIREBASE_CREDENTIALS_DICT = { ... }

# Supabase (optional)
SUPABASE_URL = 'https://<project>.supabase.co'
SUPABASE_KEY = '<service-key>'

INSTALLED_APPS = [
    # existing apps
    'django_firebase_auth',
    'django_supabase_auth',  # optional
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'django_firebase_auth.firebase_auth.FirebaseAuthentication',
    ),
}
```

## 4. Include URLs

```python
# urls.py
urlpatterns = [
    # ...
    path('firebase-auth/', include('django_firebase_auth.urls')),
]
```

The login endpoint accepts a POST with `firebase_auth_token` and returns the authenticated user.

## 5. Apply Migrations

Run the migrations to create the user profile models:

```bash
python manage.py migrate
```

## 6. Testing Authentication

Obtain an ID token from your client (Firebase SDK or Supabase) and make a POST request to `/firebase-auth/login/` with the token in the body. The user will be created or updated automatically.

