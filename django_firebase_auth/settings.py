import firebase_admin
from django.conf import settings
from django.test.signals import setting_changed

FIREBASE_CREDENTIALS_FILE = getattr(settings, "FIREBASE_CREDENTIALS_FILE", None)
FIREBASE_CREDENTIALS_DICT = getattr(settings, "FIREBASE_CREDENTIALS_DICT", None)

# Initialize Firebase Admin SDK
if FIREBASE_CREDENTIALS_FILE or FIREBASE_CREDENTIALS_DICT:
    cert = FIREBASE_CREDENTIALS_FILE or FIREBASE_CREDENTIALS_DICT
    firebase_admin.initialize_app(
        credential=firebase_admin.credentials.Certificate(cert=cert)
    )
else:
    try:
        firebase_admin.initialize_app()
    except ValueError as e:
        raise ValueError(
            "Firebase credentials not found\n "
            "set FIREBASE_CREDENTIALS_FILE or FIREBASE_CREDENTIALS_JSON in django settings"
        ) from e


def reload_settings(*args, **kwargs):
    setting_changed.send(
        sender=__name__,
        setting="FIREBASE_CREDENTIALS_FILE",
        value=FIREBASE_CREDENTIALS_FILE,
    )
    setting_changed.send(
        sender=__name__,
        setting="FIREBASE_CREDENTIALS_DICT",
        value=FIREBASE_CREDENTIALS_DICT,
    )


setting_changed.connect(reload_settings)
