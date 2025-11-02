from django.urls import path
from . import views

urlpatterns = [
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealer/<int:dealer_id>/', views.get_dealer, name='get_dealer'),
    path('get_reviews/<int:dealer_id>/', views.get_reviews, name='get_reviews'),
    path('post_review/', views.post_review, name='post_review'),
]