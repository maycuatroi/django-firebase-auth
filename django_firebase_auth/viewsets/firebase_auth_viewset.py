from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken

from django_firebase_auth.firebase_auth import FirebaseAuthentication
from django_firebase_auth.serializers.firebase_authentication_serializer import (
    FirebaseAuthTokenSerializer,
)


class FirebaseAuthViewSet(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [FirebaseAuthentication]
    serializer_class = FirebaseAuthTokenSerializer

    def get_serializer_context(self):
        user = self.request.user
        return {"user": user}
