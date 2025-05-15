<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Carbon\Carbon;

class Appointment extends Model
{
    use HasFactory;

    protected $fillable = [
        'pet_id',
        'user_id',
        'appointment_date',
        'reason',
    ];

    public function setAppointmentDateAttribute($value)
    {
        $this->attributes['appointment_date'] = Carbon::createFromFormat('m/d/Y h:i A', $value)->format('Y-m-d H:i:s');
    }

    // Each appointment belongs to one pet
    public function pet()
    {
        return $this->belongsTo(Pet::class);
    }

    // Each appointment belongs to one user
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}