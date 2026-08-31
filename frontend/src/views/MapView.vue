<template>
  <div class="map-page">

    <!-- Left: Map -->
    <section class="map-section">

      <div id="map"></div>

      <!-- Target Species -->
      <div class="species-card">
        <span class="species-dot"></span>

        <div>
          <div class="species-label">Target Species</div>

          <div class="species-name">
            Night Parrot
            <span>(Pezoporus occidentalis)</span>
          </div>
        </div>
      </div>

      <!-- Prediction Legend -->
      <div class="prediction-legend">
        <div class="legend-title">
          PREDICTION PROBABILITY
        </div>

        <div class="legend-bar"></div>

        <div class="legend-range">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>

      <!-- Data Source -->
      <div class="data-source">
        Data Source: AWC Acoustics (2026)
      </div>

    </section>


    <!-- Right Sidebar -->
    <aside class="map-sidebar">

      <!-- Insights -->
      <SpeciesInsights />

      <!-- Quiz placeholder -->
      <SpeciesQuiz />
    </aside>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import SpeciesQuiz from '../components/SpeciesQuiz.vue'
import SpeciesInsights from '../components/SpeciesInsights.vue'

onMounted(async () => {
  const map = L.map('map').setView([-25.2744, 133.7751], 5)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  try {
    const response = await fetch(
      'http://127.0.0.1:8000/api/v1/predict/pilot-bird'
    )

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`)
    }

    const geojson = await response.json()

    L.geoJSON(geojson, {
      style: {
      color: '#d9534f',
      weight: 2,
      fillColor: '#d9534f',
      fillOpacity: 0.45
      }
    }).addTo(map)

    console.log('GeoJSON received:', geojson)
  } catch (error) {
    console.error('Failed to fetch habitat prediction:', error)
  }
})
</script>

<style scoped>
.map-page {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr);
  gap: 18px;

  padding: 10px;
  background-color: #ffffff;

  min-height: calc(100vh - 64px);
}


/* =========================
   Map
   ========================= */

.map-section {
  position: relative;
  min-width: 0;
  min-height: 680px;
}

#map {
  width: 100%;
  height: 100%;
  min-height: 680px;

  z-index: 1;
}


/* =========================
   Target Species
   ========================= */

.species-card {
  position: absolute;
  top: 18px;
  left: 18px;
  z-index: 500;

  display: flex;
  align-items: center;
  gap: 10px;

  background: rgba(255, 255, 255, 0.95);

  padding: 12px 18px;
  border-radius: 8px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.species-dot {
  width: 9px;
  height: 9px;

  border-radius: 50%;
  background-color: #f3a65a;
}

.species-label {
  font-size: 10px;
  font-weight: 600;
  color: #555555;

  margin-bottom: 2px;
}

.species-name {
  color: #146c4a;
  font-size: 18px;
  font-weight: 600;
}

.species-name span {
  color: #555555;
  font-size: 12px;
  font-weight: 400;
}


/* =========================
   Prediction legend
   ========================= */

.prediction-legend {
  position: absolute;
  left: 18px;
  bottom: 18px;

  z-index: 500;

  width: 220px;

  padding: 13px 16px;

  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 7px;

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.legend-title {
  font-size: 10px;
  font-weight: 600;

  margin-bottom: 8px;
}

.legend-bar {
  height: 7px;

  border-radius: 10px;

  background: linear-gradient(
    to right,
    #4ca66b,
    #d8c95a,
    #ef7b4d
  );
}

.legend-range {
  display: flex;
  justify-content: space-between;

  margin-top: 5px;

  font-size: 10px;
  font-weight: 600;
}


/* =========================
   Data source
   ========================= */

.data-source {
  position: absolute;

  right: 18px;
  bottom: 18px;

  z-index: 500;

  background-color: rgba(255, 255, 255, 0.9);

  padding: 4px 10px;

  font-size: 10px;
  color: #666666;
}


/* =========================
   Sidebar
   ========================= */

.map-sidebar {
  display: flex;
  flex-direction: column;

  gap: 14px;
}

/* =========================
   Responsive
   ========================= */

@media (max-width: 900px) {

  .map-page {
    grid-template-columns: 1fr;
  }

  .map-section,
  #map {
    min-height: 550px;
  }

}
</style>