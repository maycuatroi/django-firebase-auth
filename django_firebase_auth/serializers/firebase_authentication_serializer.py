from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class FirebaseAuthTokenSerializer(serializers.Serializer):
    firebase_auth_token = serializers.CharField()

    def validate(self, attrs):
        firebase_auth_token = attrs.get("firebase_auth_token")
        if firebase_auth_token is None:
            msg = _('Must include "firebase_auth_token".')
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = self.context["user"]
        return attrs
