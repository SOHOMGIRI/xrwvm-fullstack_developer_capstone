import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    try:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
        request_url = f"{backend_url}{endpoint}"
        if params:
            request_url += f"?{params}"
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return []

def analyze_review_sentiments(text):
    try:
        request_url = f"{sentiment_analyzer_url}analyze/{text}"
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return {"sentiment": "unknown"}

def post_review(data_dict):
    try:
        request_url = f"{backend_url}/insert_review"
        dealership = int(data_dict.get("dealership", 0))
        car_year = str(data_dict.get("car_year", "2023")).strip()
        purchase = bool(data_dict.get("purchase", False))
        purchase_date = str(data_dict.get("purchase_date", "")).strip()
        if not is_valid_date(purchase_date):
            purchase_date = ""

        timestamp = datetime.utcnow().isoformat()
        review_id = int(data_dict.get("id", 12345))
        sentiment = analyze_review_sentiments(data_dict.get("review", "")).get("sentiment", "neutral")

        payload = {
            "id": review_id,
            "name": data_dict.get("name", ""),
            "dealership": dealership,
            "review": data_dict.get("review", ""),
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_make": data_dict.get("car_make", ""),
            "car_model": data_dict.get("car_model", ""),
            "car_year": car_year,
            "time": timestamp,
            "sentiment": sentiment
        }

        response = requests.post(request_url, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "message": "HTTP error during review submission"}
    except Exception as e:
        return {"status": "error", "message": "Review submission failed"}

def is_valid_date(date_str):
    if len(date_str) != 10:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False