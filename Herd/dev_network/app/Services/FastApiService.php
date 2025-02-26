<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class FastApiService
{
    protected $baseUrl;

    public function __construct()
    {
        $this->baseUrl = config('services.fastapi.base_url');
    }

    
     # Buscar registros (Search)
     
    public function searchRecords($ticker = null, $date = null)
    {
        $params = [];

        if ($ticker) {
            $params['TckrSymb'] = $ticker;
        }

        if ($date) {
            $params['RptDt'] = $date;
        }

        $response = Http::get("{$this->baseUrl}/search", $params);

        return $response->successful() ? $response->json() : ['error' => 'Erro ao buscar registros'];
    }

    # Fazer Upload de Arquivo
    
    public function uploadFile($file)
    {
        $response = Http::attach(
            'file', file_get_contents($file->getRealPath()), $file->getClientOriginalName()
        )->post("{$this->baseUrl}/upload");

        return $response->successful() ? $response->json() : ['error' => 'Erro ao enviar arquivo'];
    }
    # Buscar Histórico de Uploads

    public function getUploadHistory($fileName = null, $referenceDate = null)
    {
        $params = [];

        if ($fileName) {
            $params['file_name'] = $fileName;
        }

        if ($referenceDate) {
            $params['reference_date'] = $referenceDate;
        }

        $response = Http::get("{$this->baseUrl}/history", $params);

        return $response->successful() ? $response->json() : ['error' => 'Erro ao buscar histórico'];
    }
}
