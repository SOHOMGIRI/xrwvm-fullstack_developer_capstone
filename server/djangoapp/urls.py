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

    # 🔹 Future endpoints (uncomment when implemented)
    # path('dealer/<int:dealer_id>/reviews', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add_review', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)