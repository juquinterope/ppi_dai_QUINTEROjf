// Inicializar el mapa
var map = L.map('map').setView([6.251, -75.567], 8);

// Añadir capa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

// Datos de los municipios en formato GeoJSON
var municipiosGeoJSON = JSON.parse(document.getElementById('municipios-data').textContent);

// Añadir los municipios al mapa
L.geoJSON(municipiosGeoJSON, {
    onEachFeature: onEachFeature
}).addTo(map);

// Función para manejar la selección de un municipio
function onEachFeature(feature, layer) {
    layer.on({
        click: function(e) {
            var municipioId = feature.properties['Nombre Municipio'];

            // Actualizar el recuadro de información
            fetch('/municipio-detalle/' + municipioId + '/')
                .then(response => response.json())
                .then(data => {
                    var infoHtml = `
                        <h3>${data.nombre}</h3>
                        <p>${data.descripcion}</p>
                    `;
                    document.getElementById('info-panel').innerHTML = infoHtml;
                })
                .catch(error => {
                    console.error('Error al cargar la información del municipio:', error);
                    document.getElementById('info-panel').innerHTML = '<p>Error al cargar la información.</p>';
                });
        }
    });
}
