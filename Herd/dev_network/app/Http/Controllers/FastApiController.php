<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\FastApiService;

class FastApiController extends Controller
{
    protected $fastApiService;

    public function __construct(FastApiService $fastApiService)
    {
        $this->fastApiService = $fastApiService;
    }

    /**
     * 🔍 Buscar registros na API FastAPI
     */
    public function search(Request $request)
    {
        $ticker = $request->query('ticker');
        $date = $request->query('date');

        $records = $this->fastApiService->searchRecords($ticker, $date);

        return response()->json($records);
    }

    /**
     * 📂 Fazer Upload de Arquivo para a API FastAPI
     */
    public function uploadFile(Request $request)
    {
        $request->validate([
            'file' => 'required|file|mimes:csv,xlsx,xls|max:2048',
        ]);

        $result = $this->fastApiService->uploadFile($request->file('file'));

        return response()->json($result);
    }

    /**
     * 📜 Buscar Histórico de Uploads
     */
    public function getUploadHistory(Request $request)
    {
        $fileName = $request->query('file_name');
        $referenceDate = $request->query('reference_date');

        $history = $this->fastApiService->getUploadHistory($fileName, $referenceDate);

        return response()->json($history);
    }
}
