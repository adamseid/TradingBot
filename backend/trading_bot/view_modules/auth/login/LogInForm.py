
from rest_framework.views import APIView
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from ....models import UserProfile 
from django.middleware.csrf import rotate_token


class LogInForm(APIView):
    def post(self, request):
        body = request.body.decode('utf-8')  # Decode the request body
        data = json.loads(body)  # Parse the JSON data
        return self.log_in(request, data)


    def log_in(self, request, data):
        username = data.get('username')
        password = data.get('password')
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated, create a session or token if needed
            # Return a success response
            # Authenticate the user
            login(request, user)
            # Rotate CSRF token
            rotate_token(request)
            user_profile = UserProfile.objects.get(user=user)
            api_key = user_profile.api_key
            api_secret = user_profile.api_secret
            return HttpResponse(f"User signed in successfully\nAPI Key: {api_key}\nAPI Secret: {api_secret}")
        else:
            return HttpResponse("Invalid credentials")
