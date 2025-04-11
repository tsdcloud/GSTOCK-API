from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .constants import API_USER_URL

class JWTUserMiddleware(MiddlewareMixin):
    """
    Middleware to support both session-based and JWT authentication.
    """

    def process_request(self, request):

        # Extract the Authorization header
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            request.user = AnonymousUser()
            return
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse(
                {"success": False, "error": "Invalid token format. Expected 'Bearer <token>'."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Extract the JWT token
        token = auth_header.split(' ')[1]

        try:
            url_verify = f"{API_USER_URL}/token/verify/"
            headers_verify = {"Content-Type": "application/json"}
            data = {"token": token}

            url_get_user_info = f"{API_USER_URL}/user_info/"
            headers_user_info = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

            response = requests.post(url_verify, json=data, headers=headers_verify, timeout=5)

            if response.status_code != 200:
                return JsonResponse(
                    {"success": False, "error": "Invalid or expired token."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if response.status_code == 200:
                user_info_response = requests.get(url_get_user_info, headers=headers_user_info, timeout=5)

                user_info = user_info_response.json().get("data", {})

                incomming_user_exist = User.objects.filter(email=user_info.get('email')).first()

                # print("this is the user incomming" , incomming_user_exist)

                if incomming_user_exist:
                    request.user = incomming_user_exist
                    print(request.user)
                    return

                id = user_info.get("id")

                user_detail = self.get_user_info_from_external_backend(token, id)
                user_data = user_detail.get('data', {})
                # print("the user info", user_detail)

                user = self.get_or_create_user(user_data)

                # users = User.objects.all()

                # for user in users:
                #     print(user.email)

                # print("this is the user", user.email)
                request.user = user

                return 

        except (InvalidToken, TokenError):
            return JsonResponse(
                {"success": False, "error": "Invalid or expired token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def get_user_info_from_external_backend(self, token, userId):
        url = f"{API_USER_URL}/api/users/{userId}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return JsonResponse(
                {"success": False, "error": "No users found with the given id."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def get_or_create_user(self, user_info):
        try:
            user = User.objects.get(email=user_info['email'])
        except User.DoesNotExist:
            user = User.objects.create(
                username=user_info['username'],
                email=user_info['email'],
                first_name=user_info['first_name'],
                last_name=user_info['last_name'],
            )
        
        return user
