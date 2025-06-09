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

## 7. Example React Request

Below is a minimal example showing how a React application can send the ID token
to the backend.

```javascript
import { getAuth } from "firebase/auth";

async function login() {
  const token = await getAuth().currentUser?.getIdToken();
  const res = await fetch("/firebase-auth/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ firebase_auth_token: token })
  });
  return res.json();
}
```

## 8. Example Angular Service

For Angular projects you can create an injectable service that wraps the HTTP
request:

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { getAuth } from 'firebase/auth';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private http: HttpClient) {}

  async login() {
    const token = await getAuth().currentUser?.getIdToken();
    return this.http.post('/firebase-auth/login/', {
      firebase_auth_token: token
    });
  }
}
```

