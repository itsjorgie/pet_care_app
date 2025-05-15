<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class RoleMiddleware
{
    public function handle(Request $request, Closure $next, $role)
    {
        $user = Auth::user();

        // Check if the user has the correct role
        if ($role === 'admin' && $user->role !== 'admin') {
            return response()->json(['message' => 'Unauthorized'], 403);
        }

        if ($role === 'user' && $user->role !== 'user') {
            return response()->json(['message' => 'Unauthorized'], 403);
        }

        return $next($request);
    }
}
