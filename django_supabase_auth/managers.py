import supabase

from abstract_auth.abstract_user_manager import AbstractUserManager


class SupabaseUserManager(AbstractUserManager):
    def _service_create_user(
        self, email, password, phone_number=None, display_name=None
    ):
        res = supabase.auth.signup({"email": email, "password": password})
        return res
