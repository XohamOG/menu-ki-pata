from django.shortcuts import render, get_object_or_404, redirect
from .models import Meal, Feedback
from .forms import FeedbackForm
from datetime import date
from django.utils import timezone
from datetime import timedelta, datetime

def today_menu(request):
    # Get the current date from the request or default to today
    current_date_str = request.GET.get('date', timezone.now().date())
    
    # If current_date_str is a date, convert it to a string
    if isinstance(current_date_str, str):
        current_date = timezone.datetime.strptime(current_date_str, '%Y-%m-%d').date()
    else:
        current_date = current_date_str  # It is already a date

    # Get meals for today (or whatever logic you want)
    meals = Meal.objects.filter(date=current_date)  # Adjust this based on your model
    meal_type = "Lunch"  # Or whatever meal type you want

    return render(request, 'menu/today_menu.html', {
        'meals': meals,
        'meal_type': meal_type,
        'current_date': current_date,
    })


def next_day_menu(request):
    date_str = request.GET.get('date', None)  # Retrieve the date from the request
    if date_str:
        # Attempt to parse the date with the known formats
        try:
            current_date = datetime.strptime(date_str, '%b. %d, %Y')  # For 'Oct. 9, 2024'
        except ValueError:
            # Handle the case where the parsing fails (optional)
            return render(request, 'menu/error.html', {'error': 'Invalid date format.'})
    else:
        current_date = datetime.now()  # Default to current date if no date provided

    # Calculate the next day
    next_date = current_date + timedelta(days=1)

    # Your logic to retrieve meals for the next day here
    meals = []  # Replace with your actual meal retrieval logic

    return render(request, 'menu/today_menu.html', {
        'meals': meals,
        'meal_type': 'Next Day',
        'current_date': next_date.strftime('%Y-%m-%d'),  # Format the date as needed
    })



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
