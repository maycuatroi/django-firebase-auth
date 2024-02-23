from supabase import Client

from abstract_auth.abstract_auth import AbstractAuthentication
from django_supabase_auth import SUPABASE_KEY, SUPABASE_URL
from django_supabase_auth.models import SupabaseAuthProfile


class SupabaseAuth(AbstractAuthentication):
    def _get_or_create_profile(self, user, uid, avatar):
        return SupabaseAuthProfile.objects.get_or_create(
            user=user,
            defaults={"uid": uid, "photo_url": avatar},
        )[0]

    def _verify_token(self, id_token):
        client = Client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
        user = client.auth.get_user(id_token)
        return user
