"""
Handle the authentication of the user.
Using google authentication (with application)
Using firebase authentication (with web)
"""

import firebase_admin.auth

from abstract_auth.abstract_auth import AbstractAuthentication
from django_firebase_auth.models import UserFirebaseProfile


class FirebaseAuthentication(AbstractAuthentication):
    def _get_or_create_profile(self, user, uid):
        return UserFirebaseProfile.objects.get_or_create(
            user=user,
        )[0]

    def _verify_token(self, id_token):
        return firebase_admin.auth.verify_id_token(id_token)
