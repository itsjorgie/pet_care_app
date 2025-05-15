from django.urls import path
from main import views

urlpatterns = [
    # Landing & Authentication Pages
    path('', views.landing_page, name='landing'),
    path('auth/register/', views.register_page, name='register'),
    path('auth/login/', views.login_page, name='login'),
    path('auth/logout/', views.logout_page, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('user-dashboard/', views.user_dashboard_page, name='user_dashboard'),

    # Pet Management (Frontend Pages)
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pet_id>/edit/', views.pet_edit, name='pet_edit'),
    path('pets/delete/<int:pet_id>/', views.pet_delete, name='pet_delete'),

    # Appointment Management (Frontend Pages)
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/edit/<int:appointment_id>/', views.appointment_edit, name='appointment_edit'),
    path('appointments/delete/<int:appointment_id>/', views.appointment_delete, name='appointment_delete'),

    # View all my appointments or pets (user view)
    path('my-appointments/', views.user_dashboard_page, name='my_appointments'),
    path('my-pets/', views.user_dashboard_page, name='my_pets'),
    
]
