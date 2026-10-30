from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GoogleAuthSerializer
from .services import get_google_access_token, get_google_user_info

User = get_user_model()

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]
    

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        access_token = get_google_access_token(code)
        google_user = get_google_user_info(access_token)

        email = google_user["email"]
        name = google_user["name"]

        user = User.objects.filter(email__iexact=email).first()
        is_new_user = user is None

        if is_new_user:
            username = email.split("@")[0]

            if User.objects.filter(username=username).exists():
                username = f"{username}_{get_random_string(6).lower()}"

            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,
            )
            user.set_unusable_password()
            user.save()

        if not user.is_active:
            raise AuthenticationFailed("Учётная запись пользователя отключена.")

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["role"] = getattr(user, "role", "user")

        return Response(
        {
            "user": {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
                "name": name,
                "role": getattr(user, "role", "user"),
            },
            "is_new_user": is_new_user,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        },
        status=status.HTTP_200_OK,
    )

