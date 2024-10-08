from django.shortcuts import render, HttpResponse, redirect
import base64
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .utils import detect_sleep_from_frame
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def home_page(request):
    return render(request, "Home.html")

def myprofile(request):
    return HttpResponse("This is my pfp")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def guest_login(request):
    # Maybe implement any guest-specific logic
    # For now, we'll just redirect to the home page
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def detection(request):
    if request.method == 'POST':
        logger.info("Received request data: %s", request.body)
        data = request.body.decode('utf-8')
        try:
            image_data = re.search(r'base64,(.*)', data).group(1)
            # Call the sleep detection function
            detection_result = detect_sleep_from_frame(image_data)

            # Return the results as JSON
            return JsonResponse({
                "status": detection_result["status"],
                "ear": detection_result["ear"],  # Return the EAR
                "left_eye": detection_result["left_eye"],  # Return left eye coordinates
                "right_eye": detection_result["right_eye"],  # Return right eye coordinates
            })
        except Exception as e:
            # Handle exceptions (e.g., if image_data is not found)
            return HttpResponseBadRequest("Invalid image data")

    else:
        # Handle GET request - redirect to the detection page or show a friendly message
        return render(request, 'detection_page.html')  # Redirect to the detection page
