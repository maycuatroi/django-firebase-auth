from django.conf import settings
from django.test.signals import setting_changed
from supabase import Client, create_client
from supabase.client import SupabaseException

SUPABASE_URL = getattr(settings, "SUPABASE_URL", None)
SUPABASE_KEY = getattr(settings, "SUPABASE_KEY", None)

# Initialize SDK
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except SupabaseException as e:
    raise ValueError(
        "Supabase credentials not work\n "
        "set SUPABASE_URL or SUPABASE_KEY in django settings"
    ) from e


def reload_settings(*args, **kwargs):
    setting_changed.send(
        sender=__name__,
        setting="SUPABASE_URL",
        value=SUPABASE_URL,
    )
    setting_changed.send(
        sender=__name__,
        setting="SUPABASE_KEY",
        value=SUPABASE_KEY,
    )


setting_changed.connect(reload_settings)
