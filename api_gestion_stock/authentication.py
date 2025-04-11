from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
import json

from api_gestion_stock.constants import API_USER_URL, INTITY_API_URL

User = get_user_model()

class ExternalAPIAuthentication(BaseAuthentication):
    """
    Authentication based on an external API.
    """
    def authenticate(self, request):
        token_auth = request.headers.get("Authorization")

        if not token_auth:
            return None
        
        # if not token_auth.startswith('Bearer '):
        #     return JsonResponse(
        #         {"success": False, "error": "Invalid token format. Expected 'Bearer <token>'."},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        
        # Extract the JWT token
        token = token_auth.split(' ')[1]

        url_verify = f"{API_USER_URL}/token/verify/"
        headers_verify = {"Content-Type": "application/json"}
        data = {"token": token}

        url_get_user_info = f"{API_USER_URL}/user_info/"
        headers_user_info = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

        try:
            response = requests.post(url_verify, json=data, headers=headers_verify, timeout=5)

            if response.status_code != 200:
                return None
            

            if response.status_code == 200:
                user_info_request = requests.get(url_get_user_info, headers=headers_user_info, timeout=5)

                user_data = user_info_request.json().get("data", {})

                employee_info = requests.get(INTITY_API_URL, headers=headers_verify, timeout=5)


                # Convert JSON string to Python dictionary
                emmployee_dict = employee_info.json()

                # print(emmployee_dict["data"])

                # Browse and extract the record with the given ID
                filtered_employee = next((item for item in emmployee_dict["data"] if item["userId"] == user_data["id"]), None)

                # print the result
                # print("filtered employee", filtered_employee)
                # print("filtered employee id", filtered_employee["id"])

                user, _ = User.objects.get_or_create(
                    username=user_data["username"], 
                    defaults={
                        "email": user_data["email"],
                        "first_name": user_data['first_name'],
                        "username": user_data['username'],
                        "last_name": user_data['last_name'],
                        "id_employee": filtered_employee["id"],
                    }
                )

                return (user, None)
            
        except requests.RequestException:
            pass 

        raise AuthenticationFailed("Not authentified")
