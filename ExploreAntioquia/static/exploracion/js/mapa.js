// Inicializar el mapa
var map = L.map('map').setView([6.251, -75.567], 8);

var bounds = [
    [5.0, -78.0], // Suroeste (aproximado)
    [9.0, -73.5]  // Noreste (aproximado)
];
map.setMaxBounds(bounds);

// Añadir capa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Datos de los municipios en formato GeoJSON,
// desde la etiqueta con id=municipios-data,
// esta etiqueta carga el geojson en el template 'explorar_municipios.html'
var municipiosGeoJSON = JSON.parse(document.getElementById('municipios-data').textContent);

// Añadir los municipios al mapa,
// onEachFeature : funcion para aplicarlo a todos los objetos (municipios)
L.geoJSON(municipiosGeoJSON, {
    onEachFeature: onEachFeature
}).addTo(map);

// Función para manejar la selección de un municipio
// onEachFeature, aqui se define que funcion aplicar
function onEachFeature(feature, layer) {
    layer.on({
        // Al hacer click en un objeto (municipio)
        click: function(e) {
            // Obtener el ID del municipio seleccionado
            var municipioId = feature.properties['Nombre Municipio'];
            // Construir la url para consultar la informacion del municipio
            var url = window.location.origin + '/exploracion/municipio-detalle/' + encodeURIComponent(municipioId) + '/';  // Construye la URL completa
            
            // fetch() hace la consulta http
            fetch(url)
                // Cacheo de errores
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json();
                })
                // En el tag 'info-panel' del template en cuestion (explorar_municipio.html),
                // cargar la informacion consultada del geojson
                .then(data => {
                    var infoHtml = `
                        <h3>${data.nombre}</h3>
                        <p>${data.descripcion}</p>
                    `;
                    document.getElementById('info-panel').innerHTML = infoHtml;
                })
                // Errores
                .catch(error => {
                    console.error('Error al cargar la información del municipio:', error);
                    document.getElementById('info-panel').innerHTML = '<p>Error al cargar la información.</p>';
                });
        }
    });
}
