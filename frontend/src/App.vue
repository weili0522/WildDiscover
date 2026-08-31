<template>
  <div id="app">
    <div id="map"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

onMounted(async () => {
  const map = L.map('map').setView([-25.2744, 133.7751], 4)

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

<style>
html,
body,
#app {
  margin: 0;
  width: 100%;
  height: 100%;
}

#map {
  width: 100%;
  height: 100vh;
}
</style>