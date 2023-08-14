
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from ....models import UserProfile 

class RegistrationForm(APIView):
    def post(self, request):
        body = request.body.decode('utf-8')  # Decode the request body
        data = json.loads(body)  # Parse the JSON data
        return self.register(data)


    def register(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,  # Set as superuser
                is_staff=True       # Set as staff member
            )

            # Create UserProfile instance and associate with the user
            user_profile = UserProfile.objects.create(user=user, api_key=api_key, api_secret=api_secret)

            return HttpResponse("User registered successfully")
        except Exception as e:
            return HttpResponse("Invalid format")
