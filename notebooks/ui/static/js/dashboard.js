// Conexión Socket.IO
const socket = io();

// Referencias DOM
const btnStart = document.getElementById('btn-start');
const btnStop = document.getElementById('btn-stop');
const channelSelect = document.getElementById('channel-select');
const statusBadge = document.getElementById('status-badge');
const intentText = document.getElementById('intent-text');
const intentProbBar = document.getElementById('intent-prob-bar');
const agiResponseDiv = document.getElementById('agi-response');
const icpValue = document.getElementById('icp-value');

// Configuración del gráfico EEG
let eegChart;
const ctx = document.getElementById('eeg-chart').getContext('2d');

// Buffer de datos para gráfico (últimos 300 puntos)
let timeData = [];
let eegData = [];

function initChart() {
    eegChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'EEG (μV)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1,
                fill: false,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                x: { title: { display: true, text: 'Tiempo (muestras)' } },
                y: { title: { display: true, text: 'Amplitud (μV)' } }
            }
        }
    });
}

// Actualizar gráfico con nueva muestra
function updateChart(timestamp, channelData, selectedChannel) {
    const value = channelData[selectedChannel];
    eegData.push(value);
    if (eegData.length > 300) eegData.shift();
    
    // Actualizar etiquetas (índice)
    const labels = eegData.map((_, i) => i);
    eegChart.data.labels = labels;
    eegChart.data.datasets[0].data = [...eegData];
    eegChart.update('none'); // actualización silenciosa para performance
}

// Socket event handlers
socket.on('connect', () => {
    console.log('Conectado al servidor');
    statusBadge.textContent = 'Conectado';
    statusBadge.className = 'badge bg-success';
});

socket.on('eeg_update', (data) => {
    const selectedChannel = parseInt(channelSelect.value);
    updateChart(data.timestamp, data.channels, selectedChannel);
    
    // Actualizar intent
    intentText.textContent = data.intent.toUpperCase();
    const probPercent = (data.intent_prob * 100).toFixed(0);
    intentProbBar.style.width = `${probPercent}%`;
    intentProbBar.textContent = `${probPercent}%`;
});

socket.on('agi_update', (data) => {
    agiResponseDiv.textContent = data.response;
    icpValue.textContent = data.icp.toFixed(3);
});

socket.on('stream_started', (data) => {
    if (data.status) {
        btnStart.disabled = true;
        btnStop.disabled = false;
        statusBadge.textContent = 'Streaming activo';
        statusBadge.className = 'badge bg-success';
    } else {
        alert('No se pudo iniciar el stream: ' + (data.message || ''));
    }
});

socket.on('stream_stopped', () => {
    btnStart.disabled = false;
    btnStop.disabled = true;
    statusBadge.textContent = 'Detenido';
    statusBadge.className = 'badge bg-secondary';
});

// Eventos UI
btnStart.addEventListener('click', () => {
    socket.emit('start_stream');
});

btnStop.addEventListener('click', () => {
    socket.emit('stop_stream');
});

channelSelect.addEventListener('change', () => {
    // No necesita acción extra, el gráfico usa el canal seleccionado al actualizar
    console.log('Canal cambiado a', channelSelect.value);
});

// Inicializar
initChart();
