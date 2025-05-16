from django.shortcuts import render, redirect
import requests
from datetime import datetime
from .models import Pet, Appointment
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PetSerializer

API_BASE_URL = 'http://127.0.0.1:8000/api' # Base URL for my backend API

# API endpoint to get pets for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_pets(request):
    pets = Pet.objects.filter(user=request.user)
    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)

# Renders the landing/home page
def landing_page(request):
    return render(request, 'main/landing.html')

# Handles user registration form submission
def register_page(request):
    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'password_confirmation': request.POST['password_confirmation'],
            'role': request.POST.get('role', 'user'), 
        }
        response = requests.post(f'{API_BASE_URL}/register', data=data)
        if response.status_code == 201:
            return redirect('login')
        error = response.json().get('message', 'Registration failed')
        return render(request, 'main/register.html', {'error': error})
    return render(request, 'main/register.html')

# Handles user login
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            response = requests.post(f'{API_BASE_URL}/login', data={
                'email': email,
                'password': password
            })

            if response.status_code == 200:
                data = response.json()
                user = data.get('user')
                token = data.get('token')

                request.session['token'] = token
                request.session['user_id'] = user.get('id')
                request.session['role'] = user.get('role')
                request.session['name'] = user.get('name')

                if user.get('role') == 'admin':
                    return redirect('dashboard') 
                else:
                    return redirect('user_dashboard')
            else:
                error_message = response.json().get('message', 'Invalid credentials.')
                messages.error(request, error_message)

        except requests.exceptions.RequestException:
            messages.error(request, "Server error. Please try again.")

    return render(request, 'main/login.html')

# Clears session data and logs out the user
def logout_page(request):
    request.session.flush()
    return redirect('login')

# Builds headers including token for authenticated API requests
def get_auth_headers(request):
    token = request.session.get('token')
    return {'Authorization': f'Bearer {token}'} if token else {}

# Fetches pets and appointments for either admin or user
def fetch_dashboard_data(headers, role):
    if role == 'admin':
        pets_res = requests.get(f'{API_BASE_URL}/pets', headers=headers)
        appt_res = requests.get(f'{API_BASE_URL}/appointments', headers=headers)
    else:
        pets_res = requests.get(f'{API_BASE_URL}/my-pets', headers=headers)
        appt_res = requests.get(f'{API_BASE_URL}/my-appointments', headers=headers)

    pets = pets_res.json() if pets_res.status_code == 200 else []
    appointments = appt_res.json() if appt_res.status_code == 200 else []
    return pets, appointments

# Admin dashboard view
def dashboard_page(request):
    headers = get_auth_headers(request)
    if not headers:
        return redirect('login')

    pets, appointments = [], []

    try:
        pets, appointments = fetch_dashboard_data(headers, request.session.get('role'))
    except requests.exceptions.RequestException as e:
        print('API error:', e)

    return render(request, 'main/dashboard.html', {
        'pets': pets,
        'appointments': appointments,
        'role': request.session.get('role'),
    })

# User dashboard view
def user_dashboard_page(request):
    if 'token' not in request.session or 'role' not in request.session:
        return redirect('login_page')

    token = request.session['token']
    role = request.session['role']

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    try:
        pets, appointments = fetch_dashboard_data(headers, role)
    except requests.exceptions.RequestException:
        pets, appointments = [], []

    return render(request, 'main/user_dashboard.html', {
        'pets': pets,
        'appointments': appointments
    })

# Adds pet name/species and formats appointment date
def process_appointments(raw_appointments):
    for a in raw_appointments:
        pet = a.get('pet', {})
        a['pet_name'] = pet.get('name', 'N/A')
        a['pet_species'] = pet.get('species', 'N/A')

        raw_date = a.get('appointment_date')
        if raw_date:
            try:
                dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                a['appointment_date'] = dt.strftime("%m/%d/%Y %I:%M %p")
            except ValueError:
                a['appointment_date'] = raw_date
        else:
            a['appointment_date'] = 'N/A'
    return raw_appointments

# Create a new pet
def pet_create(request):
    headers = get_auth_headers(request)
    if not headers:
        return redirect('login')

    user_id = request.session.get('user_id')

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'species': request.POST.get('species'),
            'breed': request.POST.get('breed'),
            'user_id': user_id,
        }

        try:
            response = requests.post(f'{API_BASE_URL}/pets', headers=headers, json=data)

            if response.status_code in [200, 201]:
                return redirect('user_dashboard')

            error = response.json().get('message', 'Failed to create pet.')
            return render(request, 'main/pet_form.html', {'error': error})

        except requests.RequestException as e:
            return render(request, 'main/pet_form.html', {'error': f'Network error: {e}'})

    return render(request, 'main/pet_form.html')

# Edit existing pet by ID
def pet_edit(request, pet_id):
    headers = get_auth_headers(request)
    try:
        pet_response = requests.get(f'{API_BASE_URL}/pets/{pet_id}', headers=headers)
        if pet_response.status_code != 200:
            return redirect('user_dashboard')
        pet = pet_response.json()
    except requests.RequestException:
        return render(request, 'main/editpet.html', {'error': 'Failed to fetch pet details.'})

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        role = request.session.get('role') 
        data = {
            'name': request.POST.get('name'),
            'species': request.POST.get('species'),
            'breed': request.POST.get('breed'),
            'user_id': user_id,
        }
        try:
            update_response = requests.put(
                f'{API_BASE_URL}/pets/{pet_id}',
                headers={**headers, 'Content-Type': 'application/json'},
                json=data
            )
            if update_response.status_code == 200:
                if role == 'admin':
                    return redirect('dashboard') 
                else:
                    return redirect('user_dashboard')  
            error = update_response.json().get('message', 'Failed to update pet.')
            return render(request, 'main/editpet.html', {'error': error, 'pet': pet})
        except requests.RequestException as e:
            return render(request, 'main/editpet.html', {'error': f'Network error: {e}', 'pet': pet})

    return render(request, 'main/editpet.html', {'pet': pet})

# Delete a pet
def pet_delete(request, pet_id):
    headers = get_auth_headers(request)
    try:
        response = requests.delete(f'{API_BASE_URL}/pets/{pet_id}', headers=headers)
        if response.status_code not in [200, 204]:
            messages.error(request, 'Failed to delete pet.')
    except requests.RequestException as e:
        messages.error(request, f'Network error: {e}')

    return redirect('user_dashboard' if request.session.get('role') != 'admin' else 'dashboard')

# Create an appointment
def appointment_create(request):
    token = request.session.get('token')

    if not token:
        return render(request, 'main/appointment_form.html', {'error': 'Missing or invalid token', 'pets': []})

    pets = []
    headers = {'Authorization': f'Bearer {token}'}
    user_id = request.session.get('user_id')

    try:
        pet_response = requests.get(f'{API_BASE_URL}/my-pets', headers=headers)
        if pet_response.status_code == 200:
            pets = pet_response.json()
    except requests.RequestException:
        pets = []

    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        if not pet_id or not date or not time or not reason:
            return render(request, 'main/appointment_form.html', {'error': 'All fields are required', 'pets': pets})

        data = {'pet_id': pet_id, 'appointment_date': f"{date} {time}", 'reason': reason}

        try:
            response = requests.post(f'{API_BASE_URL}/appointments', headers=headers, data=data)

            if response.status_code == 201:
                return redirect('user_dashboard')
            else:
                error = response.json().get('message', 'Failed to create appointment.')
                return render(request, 'main/appointment_form.html', {'error': error, 'pets': pets})
        except requests.RequestException:
            error = 'Failed to create appointment due to network error.'
            return render(request, 'main/appointment_form.html', {'error': error, 'pets': pets})

    return render(request, 'main/appointment_form.html', {'pets': pets})

# Edit Appointment
def appointment_edit(request, appointment_id=None):
    if 'token' not in request.session or 'role' not in request.session:
        return redirect('login_page')

    token = request.session['token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        # Combine date and time
        appointment_datetime = f"{appointment_date} {appointment_time}"

        data = {
            'appointment_date': appointment_datetime,
            'reason': reason,
        }

        try:
            response = requests.put(
                f'{API_BASE_URL}/appointments/{appointment_id}',
                headers=headers,
                data=data
            )
            if response.status_code == 200:
                messages.success(request, 'Appointment updated successfully.')
                return redirect('user_dashboard')  # ✅ redirect after success
            else:
                messages.error(request, 'Failed to update appointment.')
        except requests.exceptions.RequestException:
            messages.error(request, 'Server error. Please try again later.')

    # GET logic (prepopulate form)
    appointment = {
        'appointment_date': '',
        'appointment_time': '',
        'reason': '',
        'pet_name': '',
        'species': '',
    }

    if appointment_id:
        try:
            response = requests.get(f'{API_BASE_URL}/appointments/{appointment_id}', headers=headers)
            if response.status_code == 200:
                appointment_data = response.json()
                pet = appointment_data.get('pet', {})
                dt = appointment_data.get('appointment_date', '').split(' ')
                appointment['appointment_date'] = dt[0]
                appointment['appointment_time'] = dt[1] if len(dt) > 1 else ''
                appointment['reason'] = appointment_data.get('reason', '')
                appointment['pet_name'] = pet.get('name', 'N/A')
                appointment['species'] = pet.get('species', 'N/A')
            else:
                messages.error(request, 'Appointment not found.')
                return redirect('user_dashboard')
        except requests.exceptions.RequestException:
            messages.error(request, 'Server error.')
            return redirect('user_dashboard')

    return render(request, 'main/editappt.html', {'appointment': appointment})

# Delete an appointment 
def appointment_delete(request, appointment_id):
    headers = get_auth_headers(request)
    
    try:

        appointment_response = requests.get(f'{API_BASE_URL}/appointments/{appointment_id}', headers=headers)
        
        if appointment_response.status_code == 200:
            appointment = appointment_response.json()
            pet_id = appointment.get('pet', {}).get('id') 
            
            delete_response = requests.delete(f'{API_BASE_URL}/appointments/{appointment_id}', headers=headers)
            
            if delete_response.status_code in [200, 204]:
                messages.success(request, "Appointment deleted successfully.")
            else:
                messages.error(request, "Failed to delete the appointment.")
        else:
            messages.error(request, "Appointment not found.")
        
    except requests.RequestException as e:
        messages.error(request, f"Network error: {e}")
    
    # Redirect to the correct dashboard based on user role
    return redirect('user_dashboard' if request.session.get('role') != 'admin' else 'dashboard')
