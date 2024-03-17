"""
Handle the authentication of the user.
Using google authentication (with application)
Using firebase authentication (with web)
"""

import abc
import datetime

import httplib2
from django.conf.global_settings import DEBUG
from django.contrib.auth.models import User
from django.utils import timezone
from google.auth import jwt
from google.oauth2.id_token import verify_oauth2_token
from google_auth_httplib2 import Request
from rest_framework import authentication, status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token provided"
    default_code = "invalid_token"


class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authorization token is expired"
    default_code = "token_expired"


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = (
        "The user provided with the auth token is not a "
        "valid Firebase user, it has no Firebase UID"
    )
    default_code = "no_firebase_uid"


def auth_with_application(id_token, decoded_token):
    try:
        decoded_token = verify_oauth2_token(
            id_token,
            request=Request(
                http=httplib2.Http(),
            ),
            audience=decoded_token["aud"],
        )

    except ValueError as e:
        raise InvalidAuthToken() from e
    return decoded_token


def djb2(seed):
    """
    djb2 is a hash function that was created by Dan Bernstein
    and presented in the article "Notes on hashing" in the April 1997
    issue of comp.lang.c.

    The hash function is designed to be very fast,
    and produces a hash value that is almost identical for all strings,
    even those that are very long.
    """
    # http://www.cse.yorku.ca/~oz/hash.html

    hash = 5381
    for c in seed:
        hash = ((hash << 5) + hash) + ord(c)

    return hex(hash & 0xFFFFFFFF)[2:]


class AbstractAuthentication(authentication.BaseAuthentication):
    token_post_index_name = "id_token"

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION") or ""
        id_token = (
            request.data.get(self.token_post_index_name) or auth_header.split(" ").pop()
        )
        if not auth_header and not id_token:
            # return AnonymousUser, None
            return None
        host = request.get_host()
        if (
            host.startswith("localhost")
            and not auth_header.startswith("Bearer ")
            and DEBUG
        ):
            return User.objects.get(username=auth_header), None

        try:
            decoded_token = jwt.decode(id_token, verify=False)
        except ValueError as e:
            raise InvalidAuthToken() from e
        is_expired = (
            datetime.datetime.fromtimestamp(decoded_token["exp"])
            < datetime.datetime.now()
        )
        if is_expired:
            raise InvalidAuthToken("Authorization token is expired")
        try:
            authenticated_user = self._verify_token(id_token)
        except ValueError as e:
            raise InvalidAuthToken() from e

        if not id_token or not decoded_token:
            return None

        striped_user_name = authenticated_user["email"].split("@")[0]
        # Let's add random chars after the stiped username
        # There may be the case where some@email1.com and some@email2.com users register
        # We will generate random string using the email as seed
        defaults = {"username": f"{striped_user_name}#{djb2(decoded_token['email'])}"}
        # There are some instances where the display_name may come as null from firebase
        display_name = authenticated_user.get("name")
        # If we have display_name, let's try and figure the first name and last name
        if display_name:
            first_name, last_name = self.convert_user_display_name(display_name)
            defaults["first_name"] = first_name
            if last_name:
                defaults["last_name"] = last_name
        user: User = User.objects.get_or_create(
            email=decoded_token.get("email"),
            defaults=defaults,
        )[0]
        avatar_url = authenticated_user.get("picture")
        uid = authenticated_user.get("uid")
        full_name = authenticated_user.get("name")
        first_name = full_name.split(" ")[0]
        last_name = (
            " ".join(full_name.split(" ")[1:]) if len(full_name.split(" ")) > 1 else ""
        )
        profile = self._get_or_create_profile(user=user, uid=uid, avatar=avatar_url)

        if user.first_name != first_name or user.last_name != last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=["first_name", "last_name"])

        if decoded_token.get("picture"):
            profile.photo_url = decoded_token.get("picture")
        if decoded_token.get("phone_number"):
            profile.phone_number = decoded_token.get("phone_number")
        if decoded_token.get("name"):
            profile.display_name = decoded_token.get("name")
        profile.save()
        user.last_login = timezone.now()
        profile.save()
        user.save(update_fields=["last_login"])

        return user, None

    @abc.abstractmethod
    def _get_or_create_profile(self, user, uid, avatar):
        raise NotImplementedError("This method should be implemented in child class")

    def convert_user_display_name(self, display_name: str):
        """
        Convert user display name to first name and last name
        :arg:
        display_name(str): user display name
        :return:
        first_name(str): first name of user
        last_name(str): last name of user
        """
        names = display_name.split(" ")
        first_name = names[0]
        last_name = None
        if len(names) > 1:
            last_name = names[1]
        return first_name, last_name

    @abc.abstractmethod
    def _verify_token(self, id_token):
        raise NotImplementedError("This method should be implemented in child class")
