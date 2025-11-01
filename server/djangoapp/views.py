from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# 🔹 Login view to handle sign-in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return JsonResponse({"error": "Invalid request format"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=400)

# 🔹 Logout view to handle sign-out request
@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

# 🔹 Registration view to handle sign-up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"error": "Registration failed"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=400)

# 🔹 Dealership views (to be implemented later)
# def get_dealerships(request):
#     ...

# def get_dealer_reviews(request, dealer_id):
#     ...

# def get_dealer_details(request, dealer_id):
#     ...

# def add_review(request):
#     ...