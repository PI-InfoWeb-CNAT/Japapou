document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se temos os dados passados pelo HTML
    if (typeof window.dadosEntregas !== 'undefined') {
        
        const entregas = window.dadosEntregas;
        
        // Atualiza o contador no cabeçalho
        const statusEl = document.getElementById('status-qtd');
        if(statusEl) statusEl.innerText = entregas.length + " entregas pendentes";

        
        const limitesNatal = L.latLngBounds(
            L.latLng(-6.0500, -35.4500), // Sul-Oeste
            L.latLng(-5.6000, -35.1000)  // Norte-Leste
        );

        
        const TOMTOM_KEY = TOMTOM_KEY_; 

        
        const mapaTomTom = L.tileLayer(`https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=${TOMTOM_KEY}`, {
            maxZoom: 22,
            minZoom: 11,
            bounds: limitesNatal,
            attribution: '© TomTom'
        });

        
        const mapaSatelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri',
            maxZoom: 19,
            minZoom: 11,
            bounds: limitesNatal
        });

        
        const centroNatal = [-5.79448, -35.211];
        
        const map = L.map('map', {
            center: centroNatal,
            zoom: 12,
            minZoom: 11,
            maxBounds: limitesNatal,
            maxBoundsViscosity: 1.0,
            layers: [mapaTomTom] // Começa com TomTom
        });

        
        const baseMaps = {
            "Mapa de Rua": mapaTomTom,
            "Satélite (Foto)": mapaSatelite
        };
        L.control.layers(baseMaps).addTo(map);

        
        
        const iconEntrega = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        const limitesZoom = L.latLngBounds();
        const grupoPinos = L.featureGroup();
        let temPedidos = false;

        entregas.forEach(function(item) {
            if (item.lat && item.lon) {
                const marker = L.marker([item.lat, item.lon], {icon: iconEntrega}).addTo(map);
                
                // Popup Bonito
                const htmlPopup = `
                    <div style="text-align:center; min-width: 180px;">
                        <strong style="font-size:1.1em;">${item.cliente}</strong><br>
                        <span style="font-size:0.9em; color:#555;">${item.logradouro}, ${item.numero}</span><br>
                        <small style="color:#777;">(${item.bairro})</small>
                        <hr style="margin:8px 0; border:0; border-top:1px solid #eee;">
                        
                        <a href="https://waze.com/ul?ll=${item.lat},${item.lon}&navigate=yes" 
                           target="_blank"
                           style="display:block; margin-bottom:5px; padding:8px; background-color:#33ccff; color:white; border-radius:5px; text-decoration:none; font-weight:bold;">
                           <i class="fa-brands fa-waze"></i> Ir com Waze
                        </a>

                        <a href="https://www.google.com/maps/dir/?api=1&destination=${item.lat},${item.lon}" 
                           target="_blank"
                           style="display:block; padding:8px; background-color:#4285F4; color:white; border-radius:5px; text-decoration:none; font-weight:bold;">
                           <i class="fa-brands fa-google"></i> Ir com Maps
                        </a>
                    </div>
                `;

                marker.bindPopup(htmlPopup);
                grupoPinos.addLayer(marker);
                
                // Adiciona coordenadas ao cálculo de zoom
                limitesZoom.extend([item.lat, item.lon]);
                temPedidos = true;
            }
        });

        
        if (temPedidos) {
            map.addLayer(grupoPinos);
            map.fitBounds(limitesZoom, {padding: [50, 50]});
        }

        
        
        if (navigator.geolocation) {
            let userMarker = null;
            let primeiraVezGPS = true;

            navigator.geolocation.watchPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Atualiza ou cria a bolinha azul
                if (userMarker) {
                    userMarker.setLatLng([lat, lon]);
                } else {
                    userMarker = L.circleMarker([lat, lon], {
                        radius: 9,
                        fillColor: "#3388ff",
                        color: "#fff",
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 1
                    }).addTo(map).bindPopup("Você está aqui");
                }

                
                if (primeiraVezGPS) {
                    limitesZoom.extend([lat, lon]);
                    
                    if (limitesZoom.isValid()) {
                        map.fitBounds(limitesZoom, {padding: [80, 80]});
                    } else {
                        map.setView([lat, lon], 15);
                    }
                    primeiraVezGPS = false;
                }
            }, 
            function(error) {
                console.warn("Erro GPS:", error);
            }, 
            {
                enableHighAccuracy: true,
                maximumAge: 10000,
                timeout: 10000
            });
        }
    }
});