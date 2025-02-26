<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Desafio OT</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-6">

  <div class="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-lg">
    <h1 class="text-2xl font-bold text-center mb-6">Desafio OT</h1>

    <!-- Seção de Upload -->
    <div class="mb-6">
      <h2 class="text-lg font-semibold mb-2">Upload de Arquivo</h2>
      <input type="file" id="fileInput" class="border p-2 w-full mb-2">
      <button onclick="uploadFile()" class="bg-blue-500 text-white px-4 py-2 rounded">Enviar</button>

      <!-- Barra de progresso -->
      <div class="w-full bg-gray-200 rounded-full mt-3 hidden" id="progressContainer">
        <div id="progressBar" class="bg-blue-500 text-xs font-medium text-white text-center p-1 leading-none rounded-full" style="width: 0%;">0%</div>
      </div>

      <p id="uploadResult" class="text-sm mt-2"></p>
    </div>

    <!-- Seção de Busca no Histórico -->
    <div class="mb-6">
      <h2 class="text-lg font-semibold mb-2">Buscar Histórico de Uploads</h2>
      <input type="text" id="searchFileName" placeholder="Nome do arquivo" class="border p-2 w-full mb-2">
      <input type="date" id="searchDate" class="border p-2 w-full mb-2">
      <button onclick="searchHistory()" class="bg-blue-500 text-white px-4 py-2 rounded">Buscar</button>
      <p id="historyMsg" class="text-sm mt-2"></p>
      <ul id="historyResults" class="mt-4 text-sm"></ul>
    </div>

    <!-- Seção de Busca de Registros -->
    <div class="mb-6">
      <h2 class="text-lg font-semibold mb-2">Buscar Informações</h2>
      <input type="text" id="searchTicker" placeholder="Símbolo do Ticker" class="border p-2 w-full mb-2">
      <input type="date" id="searchRecordDate" class="border p-2 w-full mb-2">
      <button onclick="searchRecords()" class="bg-blue-500 text-white px-4 py-2 rounded">Buscar</button>
      <p id="recordMsg" class="text-sm mt-2"></p>
      <ul id="recordResults" class="mt-4 text-sm"></ul>
    </div>
  </div>

  <script>
    const API_BASE_URL = "https://dev_network.test/api";

    async function uploadFile() {
      const fileInput = document.getElementById("fileInput");
      const resultMsg = document.getElementById("uploadResult");
      const progressBar = document.getElementById("progressBar");
      const progressContainer = document.getElementById("progressContainer");

      if (!fileInput.files.length) {
        resultMsg.textContent = "Selecione um arquivo antes de enviar.";
        resultMsg.className = "text-red-500";
        return;
      }

      let formData = new FormData();
      formData.append("file", fileInput.files[0]);

      // Exibir a barra de progresso
      progressContainer.classList.remove("hidden");
      progressBar.style.width = "0%";
      progressBar.textContent = "0%";

      try {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", `${API_BASE_URL}/upload`, true);

        // Atualizar a barra de progresso durante o upload
        xhr.upload.onprogress = function(event) {
          if (event.lengthComputable) {
            let percentComplete = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percentComplete + "%";
            progressBar.textContent = percentComplete + "%";
          }
        };

        // Lidar com a resposta do servidor
        xhr.onload = function() {
          progressContainer.classList.add("hidden"); // Esconder a barra de progresso
          let response;
          try {
            response = JSON.parse(xhr.responseText);
          } catch (error) {
            resultMsg.textContent = "Erro: Resposta inválida.";
            resultMsg.className = "text-red-500";
            return;
          }
          // Sempre exibe a mensagem do campo detail, se existir
          if (response.detail) {
            resultMsg.textContent = response.detail;
            resultMsg.className = "text-green-500";
          } else {
            resultMsg.textContent = "Erro: Resposta sem 'detail'.";
            resultMsg.className = "text-red-500";
          }
        };

        xhr.onerror = function() {
          progressContainer.classList.add("hidden"); // Esconder a barra de progresso
          resultMsg.textContent = "Erro de conexão com a API.";
          resultMsg.className = "text-red-500";
        };

        xhr.send(formData);
      } catch (error) {
        progressContainer.classList.add("hidden"); // Esconder a barra de progresso
        resultMsg.textContent = "Erro ao enviar arquivo.";
        resultMsg.className = "text-red-500";
        console.error("Erro ao enviar arquivo:", error);
      }
    }

    async function searchHistory() {
      const fileName = document.getElementById("searchFileName").value;
      const date = document.getElementById("searchDate").value;
      const historyMsg = document.getElementById("historyMsg");
      const historyList = document.getElementById("historyResults");

      historyMsg.textContent = "Buscando histórico...";
      historyList.innerHTML = "";

      let url = `${API_BASE_URL}/history`;
      let params = [];
      if (fileName) params.push(`file_name=${encodeURIComponent(fileName)}`);
      if (date) params.push(`reference_date=${encodeURIComponent(date)}`);
      if (params.length) url += "?" + params.join("&");

      try {
        let response = await fetch(url);
        let data = await response.json();

        // Exibe sempre a mensagem "detail", se existir
        if (data.detail) {
          historyMsg.textContent = data.detail;
        } else {
          historyMsg.textContent = "Resposta recebida.";
        }

        if (Array.isArray(data) && data.length > 0) {
          data.forEach(item => {
            let li = document.createElement("li");
            li.textContent = `${item.file_name} - ${item.upload_date}`;
            historyList.appendChild(li);
          });
        } else if (!data.detail) {
          historyMsg.textContent = "Nenhum resultado encontrado.";
        }
      } catch (error) {
        historyMsg.textContent = "Erro ao buscar histórico.";
        historyMsg.className = "text-red-500";
        console.error("Erro ao buscar histórico:", error);
      }
    }

    async function searchRecords() {
      const ticker = document.getElementById("searchTicker").value;
      const date = document.getElementById("searchRecordDate").value;
      const recordMsg = document.getElementById("recordMsg");
      const recordList = document.getElementById("recordResults");

      recordMsg.textContent = "Buscando registros...";
      recordList.innerHTML = "";

      let url = `${API_BASE_URL}/search/search`;
      let params = [];
      if (ticker) params.push(`ticker=${encodeURIComponent(ticker)}`);
      if (date) params.push(`date=${encodeURIComponent(date)}`);
      if (params.length) url += "?" + params.join("&");

      try {
        let response = await fetch(url);
        let data = await response.json();

        // Exibe a mensagem "detail" sempre que houver
        if (data.detail) {
          recordMsg.textContent = data.detail;
        } else {
          recordMsg.textContent = "Resposta recebida.";
        }

        if (Array.isArray(data) && data.length > 0) {
          data.forEach(record => {
            let li = document.createElement("li");
            li.textContent = `${record.TckrSymb} - ${record.RptDt} - ${record.CrpnNm}`;
            recordList.appendChild(li);
          });
        } else if (!data.detail) {
          recordMsg.textContent = "Nenhum registro encontrado.";
        }
      } catch (error) {
        recordMsg.textContent = "Erro ao buscar registros.";
        recordMsg.className = "text-red-500";
        console.error("Erro ao buscar registros:", error);
      }
    }
  </script>

</body>
</html>
