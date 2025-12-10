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
    
    // Verifica se a div do mapa existe e se os dados do Django foram recebidos
    if (document.getElementById('mapa-entregas') && typeof dadosMapa !== 'undefined') {
        
      
        const limitesNatal = L.latLngBounds(
            L.latLng(-6.0500, -35.4500), // Canto Sul-Oeste (Parnamirim/Macaíba)
            L.latLng(-5.6000, -35.1000)  // Canto Norte-Leste (Extremoz/Oceano)
        );

        
        
        
        const TOMTOM_KEY = TOMTOM_KEY_; 
        
        
        const mapaTomTom = L.tileLayer(`https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=${TOMTOM_KEY}`, {
            maxZoom: 22,
            minZoom: 11,
            bounds: limitesNatal, // Otimização: Só carrega esta área
            attribution: '© TomTom'
        });

        
        const mapaSatelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri',
            maxZoom: 19,
            minZoom: 11,
            bounds: limitesNatal
        });

        
        const centroNatal = [-5.79448, -35.211];
        
        const map = L.map('mapa-entregas', {
            center: centroNatal,
            zoom: 12,
            minZoom: 11,             // Impede zoom out excessivo
            maxBounds: limitesNatal,  // Impede sair da região
            maxBoundsViscosity: 1.0,  // Bloqueio "duro" nas bordas
            layers: [mapaTomTom]      // Inicia com TomTom
        });

        
        const baseMaps = {
            "Mapa de Rua": mapaTomTom,
            "Satélite (Foto)": mapaSatelite
        };
        L.control.layers(baseMaps).addTo(map);


        
        
        const iconPedido = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        
        const limitesDeZoom = L.latLngBounds(); 
        const grupoMarcadores = L.featureGroup();
        let temPedidos = false;

        dadosMapa.forEach(function(pedido) {
            if (pedido.lat && pedido.lon) {
                const marker = L.marker([pedido.lat, pedido.lon], {icon: iconPedido}).addTo(map);

                // Conteúdo do Popup com link direto para o Waze
                const popupContent = `
                    <div style="text-align:center; min-width: 160px;">
                        <strong style="font-size:14px;">${pedido.cliente}</strong><br>
                        <small style="color:#555; display:block; margin: 4px 0;">${pedido.endereco}</small>
                        <hr style="margin: 8px 0; border: 0; border-top: 1px solid #eee;">
                        <a href="https://waze.com/ul?ll=${pedido.lat},${pedido.lon}&navigate=yes" target="_blank" 
                           style="display:block; padding:8px; background-color:#33ccff; color:white; border-radius:6px; text-decoration:none; font-weight:bold; font-size:13px;">
                           <i class="fas fa-location-arrow"></i> Ir com Waze
                        </a>
                    </div>
                `;
                
                marker.bindPopup(popupContent);
                grupoMarcadores.addLayer(marker);
                
                // Adiciona este pedido à área de zoom
                limitesDeZoom.extend([pedido.lat, pedido.lon]);
                temPedidos = true;
            }
        });

        if (temPedidos) {
            map.addLayer(grupoMarcadores);
            // Ajuste inicial (caso o GPS não funcione, pelo menos vemos os pedidos)
            map.fitBounds(limitesDeZoom, {padding: [50, 50]});
        }


        

        if (navigator.geolocation) {
            let userMarker = null;
            let primeiraVezGPS = true;

            navigator.geolocation.watchPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    // 1. Atualiza ou Cria a "Bolinha Azul"
                    if (userMarker) {
                        userMarker.setLatLng([lat, lon]);
                    } else {
                        userMarker = L.circleMarker([lat, lon], {
                            radius: 9,
                            fillColor: "#4285F4", // Azul Google
                            color: "#ffffff",
                            weight: 3,
                            opacity: 1,
                            fillOpacity: 1
                        }).addTo(map).bindPopup("Você está aqui");
                    }

                    
                    if (primeiraVezGPS) {
                        limitesDeZoom.extend([lat, lon]);
                        
                        if (limitesDeZoom.isValid()) {
                            
                            map.fitBounds(limitesDeZoom, {padding: [80, 80]});
                        } else {
                            
                            map.setView([lat, lon], 15);
                        }
                        
                        primeiraVezGPS = false; 
                    }
                },
                function(error) {
                    console.warn("GPS indisponível ou permissão negada:", error.message);
                },
                {
                    enableHighAccuracy: true, // Usa GPS real (melhor precisão)
                    maximumAge: 10000,        // Aceita posições cacheadas de 10s atrás
                    timeout: 10000            // Espera até 10s por uma leitura
                }
            );
        }
    }
});


function gerarRotaGoogle() {
    
    const listaPedidos = (typeof window.dadosEntregas !== 'undefined') ? window.dadosEntregas : ((typeof dadosMapa !== 'undefined') ? dadosMapa : []);

    if (listaPedidos.length === 0) {
        alert("Não há pedidos para criar uma rota.");
        return;
    }

    
    const limiteGoogle = 9;
    const pedidosParaRota = listaPedidos.slice(0, limiteGoogle);

    if (listaPedidos.length > limiteGoogle) {
        alert(`Atenção: O Google Maps aceita no máximo ${limiteGoogle} paradas. Gerando rota para os primeiros pedidos.`);
    }

    
    const ultimoPedido = pedidosParaRota[pedidosParaRota.length - 1];
    const destinoFinal = `${ultimoPedido.lat},${ultimoPedido.lon}`;

    
    let waypoints = "";
    if (pedidosParaRota.length > 1) {
        const intermediarios = pedidosParaRota.slice(0, pedidosParaRota.length - 1);
        
        
        waypoints = intermediarios.map(p => `${p.lat},${p.lon}`).join('|');
    }

    let urlGoogle = `https://www.google.com/maps/dir/?api=1&origin=My+Location&destination=${destinoFinal}&travelmode=driving`;

    if (waypoints) {
        urlGoogle += `&waypoints=${waypoints}`;
    }

    // 4. Abrir
    window.open(urlGoogle, '_blank');
}