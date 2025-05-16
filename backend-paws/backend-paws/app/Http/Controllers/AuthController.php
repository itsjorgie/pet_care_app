<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    /**
     * Register a new user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function register(Request $request)
    {
        // Validate the incoming request data
        $validator = Validator::make($request->all(), [
            'name' => 'required|string|max:255',
            'email' => 'required|email:dns|unique:users,email', 
            'password' => 'required|string|min:8|confirmed', 
            'role' => 'required|in:user,admin',
        ]);

        // If validation fails, return a structured error response
        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Validation failed',
                'errors' => $validator->errors()
            ], 400);
        }

        // Check if the user is an admin and create accordingly
        $role = $request->role === 'admin' ? 'admin' : 'user';

        // Create the user with the correct role
        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
            'role' => $role,
        ]);

        // Return a success response with the created user data
        return response()->json([
            'status' => 'success',
            'message' => 'User registered successfully',
            'data' => $user
        ], 201);
    }


    /**
     * Login a user and return an API token.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function login(Request $request)
    {
        // Validate login input
        $request->validate([
            'email' => 'required|email',
            'password' => 'required|string',
        ]);

        // Check if user with the provided email exists
        $user = User::where('email', $request->email)->first();

        if (!$user) {
            return response()->json([
                'status' => 'error',
                'message' => 'Email not found',
            ], 404);
        }

        // Check if password matches
        if (!Hash::check($request->password, $user->password)) {
            return response()->json([
                'status' => 'error',
                'message' => 'Incorrect password',
            ], 401);
        }

        // Login the user
        Auth::login($user);

        $token = $user->createToken('LoginToken')->plainTextToken;

        if ($user->role === 'admin') {
            return response()->json([
                'message' => 'Login successful as admin',
                'role' => 'admin',
                'user' => $user,
                'token' => $token,
            ]);
        }

        return response()->json([
            'message' => 'Login successful as user',
            'role' => 'user',
            'user' => $user,
            'token' => $token,
        ]);
    }


    /**
     * Logout the user and revoke the API token.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete(); 

        return response()->json([
            'status' => 'success',
            'message' => 'Logged out successfully'
        ]);
    }
}
