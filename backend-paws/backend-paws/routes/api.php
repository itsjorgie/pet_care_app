<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PetController;
use App\Http\Controllers\AppointmentController;
use Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful;

/*
|---------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

// Public Routes
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Protected Routes (Require Authentication via Sanctum)
Route::middleware('auth:sanctum')->group(function () {

    Route::post('/logout', [AuthController::class, 'logout']);

    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    // Pets Routes (CRUD)
    Route::middleware('role:admin')->group(function () {
        Route::get('/pets', [PetController::class, 'index']);  // Get all pets (Admin only)
    });
    
    // Users can only see their own pets
    Route::middleware('role:user|admin')->group(function () {
        Route::post('/pets', [PetController::class, 'store']);
        Route::get('/pets/{id}', [PetController::class, 'show']); 
        Route::put('/pets/{id}', [PetController::class, 'update']);
        Route::delete('/pets/{id}', [PetController::class, 'destroy']);
    });

    // Appointment Routes (CRUD)
    Route::middleware('role:admin')->group(function () {
        Route::get('/appointments', [AppointmentController::class, 'index']);  // Get all appointments (Admin only)
    });

    // Users can only see their own appointments
    Route::middleware('role:user|admin')->group(function () {
        Route::post('/appointments', [AppointmentController::class, 'store']);
        Route::get('/appointments/{id}', [AppointmentController::class, 'show']); 
        Route::put('/appointments/{id}', [AppointmentController::class, 'update']); 
        Route::delete('/appointments/{id}', [AppointmentController::class, 'destroy']); 
    });

    // Only authenticated users can access
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/my-pets', [PetController::class, 'myPets']);
        Route::get('/my-appointments', [AppointmentController::class, 'myAppointments']);
    });
});
