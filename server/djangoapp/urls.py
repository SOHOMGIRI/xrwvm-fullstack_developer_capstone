from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # 🔹 Login API endpoint
    path('login', views.login_user, name='login'),

    # 🔹 Logout API endpoint
    path('logout', views.logout_request, name='logout'),

    # 🔹 Registration API endpoint
    path('register', views.registration, name='register'),

    # 🔹 Get Cars API endpoint (for CarMake and CarModel)
    path('get_cars', views.get_cars, name='getcars'),

    # 🔹 Proxy: Fetch all dealers
    path('fetch_dealers', views.fetch_dealers, name='fetch_dealers'),

    # 🔹 Proxy: Fetch reviews for a dealer
    path('fetch_reviews/<int:dealer_id>', views.fetch_reviews, name='fetch_reviews'),

    # 🔹 Proxy: Submit a review
    path('submit_review', views.submit_review, name='submit_review'),

    # 🔹 Proxy: Analyze review sentiment
    path('analyze_review', views.analyze_review, name='analyze_review'),

    # 🔹 Coursera: Get dealerships by state or all
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

    # 🔹 Coursera: Get dealer details by ID
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),

    # 🔹 Coursera: Get dealer reviews with sentiment
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),

    # 🔹 Coursera: Add a dealer review (authenticated users only)
    path('add_review', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)