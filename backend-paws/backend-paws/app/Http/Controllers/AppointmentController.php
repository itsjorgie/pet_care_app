<?php

namespace App\Http\Controllers;

use App\Models\Appointment;
use App\Models\Pet;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Carbon\Carbon;

class AppointmentController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        $appointments = $user->role === 'admin'
            ? Appointment::with('pet')->get()
            : Appointment::with('pet')->whereHas('pet', fn($q) => $q->where('user_id', $user->id))->get();

        return response()->json($appointments->map(function ($a) {
            return [
                'id' => $a->id,
                'appointment_date' => $a->appointment_date,
                'reason' => $a->reason,
                'status' => $a->status,
                'pet_id' => $a->pet->id ?? null,
                'pet' => [
                    'name' => $a->pet->name ?? 'N/A',
                    'species' => $a->pet->species ?? 'N/A',
                ],
            ];
        }));
    }

    // Create appointment
    public function store(Request $request)
    {
        $request->validate([
            'pet_id' => 'required|exists:pets,id',
            'appointment_date' => 'required|date',
            'reason' => 'nullable|string',
        ]);

        $user = Auth::user();
        $pet = Pet::findOrFail($request->pet_id);

        if ($user->role !== 'admin' && $pet->user_id !== $user->id) {
            return response()->json(['message' => 'Unauthorized'], 403);
        }

        $appointment = Appointment::create([
            'pet_id' => $pet->id,
            'appointment_date' => $request->appointment_date,
            'reason' => $request->reason,
            'user_id' => $user->id,
        ]);

        return response()->json([
            'pet_id' => $pet->id,
            'petname' => $pet->name,
            'species' => $pet->species,
            'date' => Carbon::parse($appointment->appointment_date)->format('m/d/Y h:i A'),
            'reason' => $appointment->reason,
        ], 201);
    }

    // View appointment
    public function show($id)
    {
        $appointment = Appointment::with('pet')->findOrFail($id);
        $this->authorizeAppointment($appointment);

        return response()->json([
            'id' => $appointment->id,
            'pet_id' => $appointment->pet->id ?? 'Unknown',  // Include pet_id in the response
            'petname' => $appointment->pet->name ?? 'Unknown',
            'species' => $appointment->pet->species ?? 'Unknown',
            'date' => $appointment->appointment_date,
            'reason' => $appointment->reason,
        ]);
    }

    // Update appointment
    public function update(Request $request, $id)
    {
        $appointment = Appointment::with('pet')->findOrFail($id);
        $this->authorizeAppointment($appointment);

        // If you want to update the pet as well, you need to include it in the request
        if ($request->has('pet_id')) {
            $appointment->pet_id = $request->pet_id;
        }

        // Update the appointment details
        $appointment->update($request->only('appointment_date', 'reason'));

        // Return the updated appointment data with pet details
        return response()->json([
            'id' => $appointment->id,
            'pet_id' => $appointment->pet->id ?? 'Unknown',
            'pet_name' => $appointment->pet->name,
            'pet_species' => $appointment->pet->species,
            'appointment_date' => $appointment->appointment_date,
            'reason' => $appointment->reason,
        ]);
    }

    // Delete appointment
    public function destroy($id)
    {
        $appointment = Appointment::with('pet')->findOrFail($id);
        $this->authorizeAppointment($appointment);

        $appointment->delete();

        return response()->json(['message' => 'Appointment successfully deleted'], 200);
    }

    // Appointments of current user
    public function myAppointments(Request $request)
    {
        $appointments = Appointment::with('pet')
            ->whereHas('pet', fn($q) => $q->where('user_id', $request->user()->id))
            ->get();

        return response()->json($appointments->map(function ($a) {
            return [
                'id' => $a->id,
                'pet_id' => $a->pet->id ?? 'Unknown',
                'pet_name' => $a->pet->name ?? 'Unknown',
                'species' => $a->pet->species ?? 'Unknown',
                'appointment_date' => $a->appointment_date,
                'reason' => $a->reason,
            ];
        }));
    }

    // Helper method to authorize access
    private function authorizeAppointment(Appointment $appointment)
    {
        $user = Auth::user();
        if ($user->role !== 'admin' && $appointment->pet->user_id !== $user->id) {
            abort(403, 'Unauthorized');
        }
    }
}
