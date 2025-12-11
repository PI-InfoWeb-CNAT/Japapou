function toggleDetalhes(button) {
	const detalhes = button.nextElementSibling;
	if (detalhes.style.display === "block") {
		detalhes.style.display = "none";
	} else {
		detalhes.style.display = "block";
	}
}

// Lightbox funcional
const images = document.querySelectorAll(".pedido-imagens img");
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

images.forEach((img) => {
	img.addEventListener("click", () => {
		lightboxImg.src = img.src;
		lightbox.classList.add("active");
	});
});

lightbox.addEventListener("click", () => {
	lightbox.classList.remove("active");
	lightboxImg.src = "";
});


document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se a div do mapa existe e se temos dados
    if (document.getElementById('mapa-entregas') && typeof dadosMapa !== 'undefined') {
        
        // Definição da Área (Natal)
        const limitesNatal = L.latLngBounds(
            L.latLng(-6.0500, -35.4500), 
            L.latLng(-5.6000, -35.1000)
        );

        
        // CHAVE DA API TOMTOM
        const TOMTOM_KEY = TOMTOM_KEY_; 

        const mapaTomTom = L.tileLayer(`https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=${TOMTOM_KEY}`, {
            maxZoom: 22, minZoom: 11, bounds: limitesNatal, attribution: '© TomTom'
        });

        const mapaSatelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri', maxZoom: 19, minZoom: 11, bounds: limitesNatal
        });

        // C. Inicializar Mapa
        const map = L.map('mapa-entregas', {
            center: [-5.79448, -35.211],
            zoom: 12,
            minZoom: 11,
            maxBounds: limitesNatal,
            maxBoundsViscosity: 1.0,
            layers: [mapaTomTom]
        });

        L.control.layers({ "Mapa de Rua": mapaTomTom, "Satélite": mapaSatelite }).addTo(map);

        // D. Pinos e Popups (Aqui aplicamos a lógica de Endereço)
        const iconPedido = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });

        const limitesZoom = L.latLngBounds();
        const grupoPinos = L.featureGroup();
        let temPedidos = false;

        dadosMapa.forEach(function(item) {
            if (item.lat && item.lon) {
                
                const marker = L.marker([item.lat, item.lon], {icon: iconPedido}).addTo(map);

               
                const enderecoGoogle = encodeURIComponent(`${item.endereco}, Natal - RN`);
                
                
                const linkWaze = `https://waze.com/ul?ll=${item.lat},${item.lon}&navigate=yes`;
                
                
                const linkGoogle = `https://www.google.com/maps/dir/?api=1&destination=${enderecoGoogle}&travelmode=driving`;

                const htmlPopup = `
                    <div style="text-align:center; min-width: 180px;">
                        <strong style="font-size:1.1em;">${item.cliente}</strong><br>
                        <span style="font-size:0.9em; color:#555;">${item.endereco}</span>
                        <hr style="margin:8px 0; border:0; border-top:1px solid #eee;">
                        
                        <a href="${linkWaze}" target="_blank" class="btn-popup btn-waze"
                           style="display:block; margin-bottom:5px; padding:10px; background:#33ccff; color:white; border-radius:6px; text-decoration:none; font-weight:bold;">
                           <i class="fa-brands fa-waze"></i> Waze
                        </a>

                        <a href="${linkGoogle}" target="_blank" class="btn-popup btn-google"
                           style="display:block; padding:10px; background:#4285F4; color:white; border-radius:6px; text-decoration:none; font-weight:bold;">
                           <i class="fa-brands fa-google"></i> Google Maps
                        </a>
                    </div>
                `;

                marker.bindPopup(htmlPopup);
                grupoPinos.addLayer(marker);
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

                if (userMarker) userMarker.setLatLng([lat, lon]);
                else {
                    userMarker = L.circleMarker([lat, lon], {
                        radius: 9, fillColor: "#3388ff", color: "#fff", weight: 3, opacity: 1, fillOpacity: 1
                    }).addTo(map).bindPopup("Você está aqui");
                }

                if (primeiraVezGPS) {
                    limitesZoom.extend([lat, lon]);
                    if (limitesZoom.isValid()) map.fitBounds(limitesZoom, {padding: [80, 80]});
                    else map.setView([lat, lon], 15);
                    primeiraVezGPS = false;
                }
            }, 
            function(error) { console.warn("Erro GPS:", error); }, 
            { enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 });
        }
    }
});



window.gerarRotaGoogle = function() {
    const lista = (typeof dadosMapa !== 'undefined') ? dadosMapa : [];

    if (lista.length === 0) {
        alert("Não há pedidos para criar rota.");
        return;
    }

    const limite = 9; // Limite do Google
    const rota = lista.slice(0, limite);
    
    if (lista.length > limite) alert(`A rota será gerada para os primeiros ${limite} pedidos.`);

    // último item para ser o Destino Final
    const ultimo = rota[rota.length - 1];
    
    // Essa função substitui os caracteres especiais de forma que fique adaptado para a internet
    const destinoTexto = encodeURIComponent(`${ultimo.endereco}, Natal - RN`);

    let waypoints = "";
    if (rota.length > 1) {
        // Pega todos menos o último
        const meios = rota.slice(0, rota.length - 1);
        
        // Mapeamos para o ENDEREÇO
        waypoints = meios.map(p => encodeURIComponent(`${p.endereco}, Natal - RN`)).join('|');
    }

    // Monta URL Oficial da API de Directions do Google
    // origin=My+Location: Usa o GPS do celular
    // destination: Endereço do último pedido
    // waypoints: Endereços dos pedidos intermediários
    let url = `https://www.google.com/maps/dir/?api=1&origin=My+Location&destination=${destinoTexto}&travelmode=driving`;
    
    if (waypoints) {
        url += `&waypoints=${waypoints}`;
    }

    window.open(url, '_blank');
};