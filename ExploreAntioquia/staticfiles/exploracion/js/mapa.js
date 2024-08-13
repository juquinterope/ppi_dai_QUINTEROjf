document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el mapa
    var map = L.map('map').setView([6.251, -75.567], 8);

    // Añadir capa base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    // Datos de los municipios en formato GeoJSON
    var municipios = JSON.parse(document.getElementById('municipios-data').textContent);

    // Añadir los municipios al mapa
    var geojsonLayer = L.geoJSON(municipios);
    geojsonLayer.addTo(map);

    // Evento para cuando se hace clic en un municipio
    geojsonLayer.eachLayer(function(layer) {
        layer.on('click', function(e) {
            const municipioNombre = e.target.feature.properties['Nombre Municipio'];
            fetchMunicipioInfo(municipioNombre);
        });
    });

    function fetchMunicipioInfo(municipioNombre) {
        fetch(`/get-municipio-info/${municipioNombre}/`)
        .then(response => response.json())
        .then(data => {
            displayMunicipioInfo(data);
        });
    }

    function displayMunicipioInfo(data) {
        const infoPanel = document.getElementById('info-panel');
        infoPanel.innerHTML = `
            <h3>${data.nombre}</h3>
            <p>Población: ${data.poblacion}</p>
            <p>Altitud: ${data.altitud}</p>
            <p>Superficie: ${data.superficie} km²</p>
            <p>Descripción: ${data.descripcion}</p>
        `;
    }
});
