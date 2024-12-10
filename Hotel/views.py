# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, Customer, Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone
import json
from django.contrib.auth import logout
from .CustomForms import CustomUserCreationForm, UserCreationForm
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404


# @login_required
# @permission_classes([IsAuthenticated])
def room_listing(request):
    if request.method == 'GET':
        print(request.user)
        rooms = Room.objects.filter(available=True)
        available_rooms = Room.objects.filter(available=True).count()
        booked_rooms = Booking.objects.all()

        return render(request, 'hotel/Home.html', {'rooms': rooms,'booked': booked_rooms, 'number': available_rooms})
    return render(request, 'hotel/Home.html')

@login_required
def delete_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('delete_id')
        booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
        booking.delete()
        return JsonResponse({"message": 'Booking deleted successfully'}) 
    
# @login_required
@csrf_exempt
def book_room(request):
    if request.method == 'POST':
        try:
            # Parse the request body for JSON data
            print("Booking")
            data = json.loads(request.body)

            # Extract fields from the data
            name = data.get('name')
            email = data.get('email')
            room_type = data.get('room_type')
            capacity = data.get('persons')
            number_of_rooms = data.get('rooms')
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            price = data.get('price')
            room_number = data.get('room_number')

            # Convert date strings to datetime objects
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')

            # Fetch the room from the database by room number
            room = Room.objects.filter(room_number=room_number, available=True).first()
            print(room, room_number)
            if room:
                # Create a new Reservation
                reservation = Booking.objects.create(
                    customer=request.user,
                    email=email,
                    room=room,
                    check_in=check_in_date,
                    check_out=check_out_date,
                    total_price=price
                )

                # Mark the room as unavailable
                room.available = False
                room.save()

                # Return a success message
                return JsonResponse({
                    'message': 'Booking successful',
                    'room_number': room.room_number,
                    'total_price': reservation.total_price,
                })

            else:
                return JsonResponse({'error': 'Room not available'}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Something went wrong. Please try again later.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def signUp(request):
    if request.method == "POST":
        try:
            # Parse the raw JSON data into a dictionary
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pass the parsed data to the serializer
        print(data)
        serializer = UserSignupSerializer(data=data)
        # Save the new user
        user = serializer.create(data)
        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        response_data = {
            "username": user.username,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        # Render the home page with the data
        return render(request, "hotel/Home.html", {"data": response_data})

    # Render the signup form for GET requests
    return render(request, "auth/signUp.html")

def signIn(request):
    """
    Handle user login via JSON request.
    
    Expects a JSON payload with 'username' and 'password'.
    Returns:
    - 200 OK with user data if login is successful
    - 400 Bad Request if credentials are invalid
    - 401 Unauthorized for authentication failure
    """
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Validate input
            if not username or not password:
                return JsonResponse({
                    'error': 'Username and password are required.'
                }, status=400)

            # Attempt to authenticate the user
            # Note: This allows login with either username or email
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Successfully authenticated
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }, status=200)
            else:
                # Authentication failed
                return JsonResponse({
                    'error': 'Invalid username or password'
                }, status=401)

        except json.JSONDecodeError:
            # Invalid JSON
            return JsonResponse({
                'error': 'Invalid JSON payload'
            }, status=400)
        except Exception as e:
            # Catch any unexpected errors
            return JsonResponse({
                'error': 'An unexpected error occurred'
            }, status=500)
    return render(request, 'auth/signIn.html')        

@login_required
def check_availability(request):
    print("check availability")
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        capacity = request.POST.get('capacity')
        rooms_requested = int(request.POST.get('rooms'))
        print(check_in, check_out, capacity, rooms_requested)   

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        available_rooms = Room.objects.filter(
            available=True,            # Room must be available
            capacity__gte=capacity,       # Room capacity must be greater than or equal to room capacity
            rooms__gte=rooms_requested  # Number of rooms available must match the request
        )

        rooms_data = [
            {
                'room_number': room.room_number,
                'room_type': room.room_type,
                'capacity': room.capacity,
                'rooms': room.rooms,
                'price_per_day': room.price_per_day
            }
            for room in available_rooms
        ]

        return JsonResponse({'available_rooms': rooms_data})


@login_required
def available_rooms(request):
    rooms = Room.objects.filter(available=True)
    room_data = []
    for room in rooms:
        room_data.append({
            'id': room.id,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'capacity': room.capacity,
            'rooms': room.rooms,
            'price_per_day': room.price_per_day,
        })
    print(room_data)
    return JsonResponse({'rooms': room_data})        


@login_required
def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Create and save the message
        new_message = Message(name=name, email=email, message=message)
        new_message.save()

        return JsonResponse({'success': True, 'message': 'Message sent successfully!'})


@login_required
def admin_dashboard(request):
    
    # Total number of rooms
    total_rooms = Room.objects.count()

    # Number of available rooms
    available_rooms = Room.objects.filter(available=True).count()

    # Total bookings
    total_bookings = Booking.objects.count()

    # Total revenue from all bookings
    total_revenue = Booking.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0

    # Total number of guests
    total_guests = Customer.objects.count()

    #messages
    messages = Message.objects.all().order_by('-created_at')  # Get all messages
    
    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_guests': total_guests,
        'messages': messages,
    }
    print(context["total_guests"])
    print(context["total_revenue"])

    return render(request, 'hotel/admin_dashboard.html', context)


def logout(request):
    """
    Log out the user and redirect them to the login page.
    """
    if request.method == 'POST':
        # Log out the user
        logout(request)

        # Return a JSON response indicating success
        return JsonResponse({"message": "Successfully logged out", "redirect_url": "/signIn/"}, status=200)

    # If the method is not POST, redirect to the homepage or another relevant page
    return redirect('/auth/signin/')




