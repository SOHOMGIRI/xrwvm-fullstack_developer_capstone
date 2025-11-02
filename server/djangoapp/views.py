from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .restapis import get_request, post_review
import json

def get_dealerships(request):
    state = request.GET.get("state")
    if state:
        data = get_request("/fetchDealers", state=state)
    else:
        data = get_request("/fetchDealers")
    return JsonResponse(data, safe=False)

def get_dealer(request, dealer_id):
    data = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse(data, safe=False)

def get_reviews(request, dealer_id):
    data = get_request(f"/fetchReviews/dealer/{dealer_id}")
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = post_review(data)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})