from django.urls import path
from django_firebase_auth.viewsets.firebase_auth_viewset import FirebaseAuthViewSet

app_name = "firebase_auth"
urlpatterns = [
    path("login/", FirebaseAuthViewSet.as_view(), name="login"),
    # path('logout/', FirebaseAuthLogoutViewSet.as_view(), name='logout'),
]
