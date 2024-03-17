"""
Handle the authentication of the user.
Using google authentication (with application)
Using firebase authentication (with web)
"""

import firebase_admin.auth

from abstract_auth.abstract_auth import AbstractAuthentication
from django_firebase_auth.models import UserFirebaseProfile


class FirebaseAuthentication(AbstractAuthentication):
    token_post_index_name = "firebase_auth_token"

    def _get_or_create_profile(self, user, uid, avatar: str):
        return UserFirebaseProfile.objects.update_or_create(
            user=user,
            defaults={
                "uid": uid,
                "photo_url": avatar,
            },
        )[0]

    def _verify_token(self, id_token):
        return firebase_admin.auth.verify_id_token(
            id_token, check_revoked=True, clock_skew_seconds=5
        )
