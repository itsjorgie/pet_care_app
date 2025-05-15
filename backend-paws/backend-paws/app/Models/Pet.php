<?php 

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Pet extends Model
{
    use HasFactory; 

    protected $fillable = [
        'name', 
        'species', 
        'breed', 
        'user_id',
    ];

    // Each pet belongs to one user
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    // Each pet can have many appointments
    public function appointments()
    {
        return $this->hasMany(Appointment::class);
    }
}
