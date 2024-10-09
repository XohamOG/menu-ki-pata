from django.urls import path
from . import views  # Import views from the same directory

urlpatterns = [
    path('', views.today_menu, name='today_menu'),  # Route for today's menu
    path('next/', views.next_day_menu, name='next_day_menu'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),  # Route for meal details
    path('meal/<int:meal_id>/feedback/', views.add_feedback, name='add_feedback'),  # Route for adding feedback
    # urls.py

]
