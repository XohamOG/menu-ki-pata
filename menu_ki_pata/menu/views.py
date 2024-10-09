from django.shortcuts import render, get_object_or_404, redirect
from .models import Meal, Feedback
from .forms import FeedbackForm
from datetime import date
from django.utils import timezone
from datetime import timedelta

# Show today's menu with filtering by meal type
# views.py
from django.shortcuts import render, redirect
from .models import Meal
from datetime import timedelta, datetime

def today_menu(request):
    # Get the current date or the date from the query parameters
    current_date = request.GET.get('date', datetime.now().date())
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    
    # Get meals for today
    meals = Meal.objects.filter(date=current_date)
    meal_type = 'lunch'  # Or dynamically determine based on the current time
    
    # Prepare the context
    context = {
        'meals': meals,
        'meal_type': meal_type,
        'current_date': current_date,
    }
    
    return render(request, 'menu/today_menu.html', context)

def next_day_menu(request):
    # Navigate to the next day
    current_date = request.GET.get('date', datetime.now().date())
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    next_date = current_date + timedelta(days=1)
    
    return redirect('today_menu', date=next_date)



# View for a single meal, showing details and feedback
def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    feedback_list = meal.feedback.all()  # Get all feedback for this meal
    return render(request, 'menu/meal_detail.html', {'meal': meal, 'feedback_list': feedback_list})

# Collect feedback for a specific meal
def add_feedback(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.meal = meal
            feedback.save()
            return redirect('meal_detail', meal_id=meal.id)
    else:
        form = FeedbackForm()
    return render(request, 'menu/add_feedback.html', {'form': form, 'meal': meal})
