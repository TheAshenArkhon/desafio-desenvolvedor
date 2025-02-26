<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\FastApiController;

Route::get('/search', [FastApiController::class, 'search']);
Route::post('/upload', [FastApiController::class, 'uploadFile']);
Route::get('/history', [FastApiController::class, 'getUploadHistory']);
