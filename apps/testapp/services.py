import requests

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def get_google_access_token(code): 
    url = "https://oauth2.googleapis.com/token"


    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        token_data = response.json()
    except (requests.RequestException, ValueError):
        raise AuthenticationFailed("Не удалось получить токен Google.")

        access_token = token_data.get("access_token")

        if not access_token:
            raise AuthenticationFailed("Google не вернул access_token.")

    return access_token

def get_google_user_info(access_token):
    url = "https://www.googleapis.com/oauth2/v2/userinfo"


    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        user_data = response.json()
    except (requests.RequestException, ValueError):
        raise AuthenticationFailed("Не удалось получить профиль Google.")

    email = user_data.get("email")
    name = user_data.get("name")

    if not email:
        raise AuthenticationFailed("Google не вернул email пользователя.")

    return {
    "email": email,
    "name": name or email.split("@")[0],
}

