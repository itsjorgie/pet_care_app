<?php

namespace App\Http\Controllers;

use App\Models\Pet;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class PetController extends Controller
{
    // List of pets
    public function index()
    {
        $user = Auth::user();
        $pets = $user->role === 'admin'
            ? Pet::all()
            : Pet::where('user_id', $user->id)->get();

        return response()->json($pets);
    }

    // Create pet
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|string',
            'species' => 'required|string',
            'breed' => 'required|string',
        ]);

        $pet = Pet::create([
            'name' => $request->name,
            'species' => $request->species,
            'breed' => $request->breed,
            'user_id' => Auth::id(),
        ]);

        return response()->json($pet, 201);
    }

    // View pet
    public function show($id)
    {
        $pet = Pet::findOrFail($id);
        $this->authorizePet($pet);

        return response()->json($pet);
    }

    // Update pet
    public function update(Request $request, $id)
    {
        $pet = Pet::findOrFail($id);
        $this->authorizePet($pet);

        $request->validate([
            'name' => 'sometimes|string',
            'species' => 'sometimes|string',
            'breed' => 'sometimes|string',
        ]);

        $pet->update($request->only('name', 'species', 'breed'));

        return response()->json($pet);
    }

    // Delete pet
    public function destroy($id)
    {
        $pet = Pet::findOrFail($id);
        $this->authorizePet($pet);

        $pet->delete();

        return response()->json(['message' => 'Pet successfully deleted'], 200);
    }

    // Get authenticated user's pets
    public function myPets(Request $request)
    {
        $pets = $request->user()->pets()->select('id', 'name', 'species', 'breed')->get();
        return response()->json($pets);
    }

    // Helper method to authorize access
    private function authorizePet(Pet $pet)
    {
        if (Auth::user()->role !== 'admin' && $pet->user_id !== Auth::id()) {
            abort(403, 'Unauthorized');
        }
    }
}
