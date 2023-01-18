from django.db import models


class UserFirebaseProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
