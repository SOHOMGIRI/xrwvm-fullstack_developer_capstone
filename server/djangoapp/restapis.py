import os
import requests
from dotenv import load_dotenv

# 🔹 Load environment variables from .env file
load_dotenv()

# 🔹 Backend and sentiment analyzer URLs
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# 🔹 GET request to backend with optional query parameters
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

# 🔹 Analyze review sentiment using external sentiment analyzer
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"Analyzing sentiment from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return None

# 🔹 POST review data to backend
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url} with data: {data_dict}")
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Review post failed: {e}")
        return None