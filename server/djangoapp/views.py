from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# 🔹 Models for car data
from .models import CarMake, CarModel

# 🔹 Populate function to seed car data
from .populate import initiate

# 🔹 Proxy service functions
from .restapis import get_request, post_review, analyze_review_sentiments

# 🔹 Logger setup
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

# 🔹 Get Cars view for CarMake and CarModel
def get_cars(request):
    count = CarModel.objects.count()
    print(f"CarModel count: {count}")
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})

# 🔹 Proxy: Fetch dealers from Express API
def fetch_dealers(request):
    dealers = get_request("/dealers")
    return JsonResponse({"dealers": dealers})

# 🔹 Proxy: Fetch reviews for a dealer
def fetch_reviews(request, dealer_id):
    reviews = get_request("/reviews", dealerId=str(dealer_id))
    return JsonResponse({"reviews": reviews})

# 🔹 Proxy: Submit a review to Express API
@csrf_exempt
def submit_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = post_review(data)
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Review submission error: {e}")
            return JsonResponse({"error": "Review submission failed"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=400)

# 🔹 Proxy: Analyze sentiment of a review
def analyze_review(request):
    text = request.GET.get("text", "")
    if not text:
        return JsonResponse({"error": "Missing text"}, status=400)
    sentiment = analyze_review_sentiments(text)
    return JsonResponse({"sentiment": sentiment})

# 🔹 Coursera: Get dealerships by state or all
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# 🔹 Coursera: Get dealer details by ID
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# 🔹 Coursera: Get dealer reviews with sentiment
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# 🔹 Coursera: Add a dealer review (only for authenticated users)
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})