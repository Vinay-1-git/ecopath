const API_URL = 'http://localhost:5000/api';
let map;
let shortestRoute = null;
let ecoRoute = null;
let aqiMarkers = [];
let routeMarkers = []; // New array to manage Start/End and pollution markers

// Global Map Layers for robust switching
const standardLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
});
const greeneryLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '© Esri'
});

// Check authentication
function checkDashboardAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        document.getElementById('userName').textContent = `Welcome, ${user.name}`;
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Initialize Map
function initMap() {
    // Center on Mysore, Karnataka
    map = L.map('map').setView([12.2958, 76.6394], 13);
    
    // Add the default standard layer
    standardLayer.addTo(map);
}

// Toggle map view (Takes the button element and view type)
function toggleMapView(button, view) {
    // Update button states
    document.querySelectorAll('.map-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active'); 
    
    // Remove existing tile layers for clean switching
    if (map.hasLayer(standardLayer)) {
        map.removeLayer(standardLayer);
    }
    if (map.hasLayer(greeneryLayer)) {
        map.removeLayer(greeneryLayer);
    }
    
    // Add appropriate layer
    if (view === 'standard') {
        standardLayer.addTo(map);
    } else if (view === 'greenery') {
        greeneryLayer.addTo(map);
    }
}

// Helper to clear all route-specific elements
function clearMapFeatures() {
    if (shortestRoute) map.removeLayer(shortestRoute);
    if (ecoRoute) map.removeLayer(ecoRoute);
    
    routeMarkers.forEach(marker => map.removeLayer(marker));
    routeMarkers = []; // Reset the marker array
}

// Handle route form submission
document.getElementById('routeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fromLocation = document.getElementById('fromLocation').value;
    const toLocation = document.getElementById('toLocation').value;
    const token = localStorage.getItem('token');

    clearMapFeatures();
    
    // Update UI to show loading state
    document.getElementById('avgAQI').textContent = '...';
    document.getElementById('avgAQI').style.color = '#6b7280'; 
    document.getElementById('co2Level').textContent = '...';
    document.getElementById('ecoScore').textContent = '...';
    document.getElementById('distance').textContent = '...';

    
    try {
        const response = await fetch(`${API_URL}/route`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                from: fromLocation,
                to: toLocation
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayRoutes(data);
            updateStats(data);
        } else {
            alert(data.message || 'Failed to find route');
            // Reset stats on failure
            updateStats({ eco_route: { avg_aqi: '--', avg_co2: '--', eco_score: '--', distance: '--' } });
        }
    } catch (error) {
        console.error('Route error:', error);
        alert('Connection error. Please try again.');
        // Reset stats on connection error
        updateStats({ eco_route: { avg_aqi: '--', avg_co2: '--', eco_score: '--', distance: '--' } });
    }
});

// Display routes on map
function displayRoutes(data) {
    clearMapFeatures(); // Ensure everything is clear before drawing

    const startCoord = data.shortest_route.coordinates[0];
    const endCoord = data.shortest_route.coordinates[data.shortest_route.coordinates.length - 1];

    // --- 1. ADD START AND END MARKERS ---
    
    // Add Start Marker (Blue/Standard Pin)
    const startMarker = L.marker(startCoord)
        .bindPopup(`<strong>START:</strong> ${document.getElementById('fromLocation').value}`)
        .addTo(map);
    routeMarkers.push(startMarker);

    // Add End Marker (Custom Green Circle)
    const endMarker = L.marker(endCoord, {
        icon: L.divIcon({
            className: 'custom-end-marker',
            html: '<div style="background-color:#059669; color:white; padding: 5px; border-radius: 50%; font-weight: bold; width: 30px; height: 30px; text-align: center; line-height: 20px; border: 3px solid white;">E</div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15] // Centered anchor
        })
    }).bindPopup(`<strong>END:</strong> ${document.getElementById('toLocation').value}`)
      .addTo(map);
    routeMarkers.push(endMarker);
    
    // --- 2. DRAW SHORTEST ROUTE (RED) ---
    if (data.shortest_route && data.shortest_route.coordinates) {
        shortestRoute = L.polyline(data.shortest_route.coordinates, {
            color: '#ef4444',
            weight: 5,
            opacity: 0.7
        }).addTo(map);
        
        // Add markers for high pollution areas
        if (data.shortest_route.high_aqi_points) {
            data.shortest_route.high_aqi_points.forEach(point => {
                const marker = L.circleMarker(point.coordinates, {
                    radius: 8,
                    fillColor: '#dc2626',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).bindPopup(`<strong>High AQI Zone</strong><br>AQI: ${point.aqi}<br>CO2: ${point.co2} g/km`)
                  .addTo(map);
                routeMarkers.push(marker);
            });
        }
    }
    
    // --- 3. DRAW ECO-FRIENDLY ROUTE (GREEN) ---
    if (data.eco_route && data.eco_route.coordinates) {
        ecoRoute = L.polyline(data.eco_route.coordinates, {
            color: '#10b981',
            weight: 5,
            opacity: 0.7
        }).addTo(map);
        
        // Add markers for low pollution areas
        if (data.eco_route.low_aqi_points) {
            data.eco_route.low_aqi_points.forEach(point => {
                const marker = L.circleMarker(point.coordinates, {
                    radius: 8,
                    fillColor: '#059669',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).bindPopup(`<strong>Clean Air Zone</strong><br>AQI: ${point.aqi}<br>CO2: ${point.co2} g/km`)
                  .addTo(map);
                routeMarkers.push(marker);
            });
        }
    }
    
    // Fit map to show all routes
    const bounds = L.latLngBounds([startCoord, endCoord]);
    map.fitBounds(bounds, { padding: [50, 50] });
}

// Update statistics
function updateStats(data) {
    // Safely assign text content
    document.getElementById('avgAQI').textContent = data.eco_route.avg_aqi;
    document.getElementById('co2Level').textContent = data.eco_route.avg_co2;
    document.getElementById('ecoScore').textContent = data.eco_route.eco_score;
    
    // Handle distance formatting only if it's a number
    const distanceVal = data.eco_route.distance;
    document.getElementById('distance').textContent = typeof distanceVal === 'number' ? distanceVal.toFixed(2) : distanceVal;
    
    // Color code AQI
    const aqiElement = document.getElementById('avgAQI');
    const aqi = data.eco_route.avg_aqi;

    // Reset color before applying new rule
    aqiElement.style.color = '#10b981'; 

    if (typeof aqi === 'number') {
        if (aqi <= 50) {
            aqiElement.style.color = '#10b981'; // Green (Good)
        } else if (aqi <= 100) {
            aqiElement.style.color = '#f59e0b'; // Yellow (Moderate)
        } else {
            aqiElement.style.color = '#ef4444'; // Red (Unhealthy)
        }
    } else {
        // Default color if data is missing or '---'
        aqiElement.style.color = '#6b7280'; 
    }
}

// Initialize on page load
checkDashboardAuth();
initMap();