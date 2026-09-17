<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const props = defineProps({
  speciesId: {
    type: String,
    default: null
  },
  showViewingPoints: {
    type: Boolean,
    default: false
  },
  probabilityThreshold: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['select-potential'])

let map = null
let watchZone = null
let habitatLayer = null
let viewingPointsLayer = null
let currentGeoJSON = null


const levelStyles = {
  high: { color: '#3265e8', fillColor: '#3265e8', threshold: 0.8 },
  medium: { color: '#df8b24', fillColor: '#df8b24', threshold: 0.6 },
  low: { color: '#8c9791', fillColor: '#8c9791', threshold: 0 }
}

const watchZoneCoordinates = [
  [-22.18, 118.63],
  [-22.18, 118.94],
  [-22.52, 118.98],
  [-22.58, 118.65]
]

function getLevelBySuitability(suit) {
  if (suit >= 0.8) return 'high'
  if (suit >= 0.6) return 'medium'
  return 'low'
}

function renderHabitatLayer() {
    if (!map || !currentGeoJSON) return
    
    if (habitatLayer) {
      map.removeLayer(habitatLayer)
    }
    
    habitatLayer = L.geoJSON(currentGeoJSON, {
      filter: (feature) => {
        const suit = feature.properties.suitability || 0;
        return (suit * 100) >= props.probabilityThreshold;
      },
      style: (feature) => {
        const suit = feature.properties.suitability || 0
        const level = getLevelBySuitability(suit)
        const style = levelStyles[level]
        return {
          color: style.color,
          fillColor: style.fillColor,
          fillOpacity: 0.6,
          opacity: 0.8,
          weight: 1.5,
          className: `habitat-polygon potential-${level}` // removed potential-circle to prevent blur
        }
      },
      onEachFeature: (feature, layer) => {
        const suit = feature.properties.suitability || 0
        const level = getLevelBySuitability(suit)
        const probability = Math.round(suit * 100)
        
        // Add hover tooltip
        layer.bindTooltip(`<strong>${level.toUpperCase()} POTENTIAL</strong><br/>Probability: ${probability}%`, {
          sticky: true,
          className: 'habitat-tooltip'
        })
        
        layer.on('click', () => {
          emit('select-potential', {
             id: level,
             probability: probability,
             level: `${level.charAt(0).toUpperCase() + level.slice(1)} Potential`,
             location: 'Selected Region'
          })
        })
      }
    }).addTo(map)
}

async function fetchAndRenderHabitat() {
  if (!props.speciesId || !map) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/predict/${props.speciesId}`)
    if (!res.ok) throw new Error('Failed to fetch habitat data')
    currentGeoJSON = await res.json()
    
    renderHabitatLayer()
    
    if (habitatLayer && habitatLayer.getBounds && habitatLayer.getBounds().isValid && habitatLayer.getBounds().isValid()) {
      map.fitBounds(habitatLayer.getBounds(), { padding: [50, 50] })
    }
  } catch (e) {
    console.error(e)
  }
}

async function fetchAndRenderViewingPoints() {
  if (!map) return
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/map/geojson`)
    if (!res.ok) throw new Error('Failed to fetch viewing points')
    const geojsonData = await res.json()
    
    if (viewingPointsLayer) {
      map.removeLayer(viewingPointsLayer)
    }
    
    viewingPointsLayer = L.geoJSON(geojsonData, {
      pane: 'viewingPointsPane',
      filter: (feature) => {
        return feature.properties && feature.properties.name
      },
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          pane: 'viewingPointsPane',
          radius: 6,
          fillColor: "#ff7800",
          color: "#fff",
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        })
      },
      onEachFeature: (feature, layer) => {
        const p = feature.properties
        const name = p.name || 'Unnamed Viewpoint'
        
        let details = []
        if (p.tourism && p.tourism !== 'viewpoint') {
          details.push(p.tourism.charAt(0).toUpperCase() + p.tourism.slice(1))
        }
        if (p.surface) {
          details.push(`Surface: ${p.surface}`)
        }
        
        let content = `<strong>${name}</strong>`
        if (details.length > 0) {
          content += `<br/><span style="color: #666; font-size: 1.17em;">${details.join(' • ')}</span>`
        }
        
        layer.bindTooltip(content, { 
          direction: 'top',
          className: 'viewing-point-tooltip',
          offset: [0, -6]
        })
      }
    })
    
    if (props.showViewingPoints) {
      viewingPointsLayer.addTo(map)
    }
  } catch (e) {
    console.error(e)
  }
}


function initialiseMap() {
  map = L.map('habitat-map', { zoomControl: false, attributionControl: false }).setView([-25.4, 133.75], 4)
  
  // Create a custom pane for viewing points so they always sit above polygons
  map.createPane('viewingPointsPane')
  map.getPane('viewingPointsPane').style.zIndex = 650
  
  const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  L.tileLayer(tileUrl, { maxZoom: 19 }).addTo(map)
  L.control.zoom({ position: 'bottomright' }).addTo(map)
  fetchAndRenderHabitat()
  fetchAndRenderViewingPoints()
}

watch(() => props.showViewingPoints, (newVal) => {
  if (!viewingPointsLayer || !map) return
  if (newVal) {
    viewingPointsLayer.addTo(map)
  } else {
    map.removeLayer(viewingPointsLayer)
  }
})

watch(() => props.speciesId, () => {
  fetchAndRenderHabitat()
})

watch(() => props.probabilityThreshold, () => {
  renderHabitatLayer()
})

onMounted(() => {
  initialiseMap()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    watchZone = null
    habitatLayer = null
    viewingPointsLayer = null
  }
})
</script>

<template>
  <section class="map-shell">
    

    <div
      v-if="props.mode === 'explore'"
      class="map-context"
    >
      <span>
        <b class="context-dot"></b>
        PILBARA REGION, WA
      </span>

      <span>22.13° S, 118.89° E</span>

      <span class="terrain-label">
        △ Spinifex Grassland / Swale
      </span>
    </div>

    <div id="habitat-map"></div>

    <div class="map-legend">
      <div class="legend-heading">
        <strong>HABITAT POTENTIAL</strong>
        <span>Color-Blind Safe</span>
      </div>

      <div class="mini-levels">
        <span class="high-level">
          ◆ High (≥70%)
        </span>

        <span class="medium-level">
          ▲ Medium (40–69%)
        </span>

        <span class="low-level">
          ○ Low (&lt;40%)
        </span>
      </div>

      <small v-if="props.mode === 'plan'">
        ◉ Pattern &amp; shape coded:
        Blue ◆ | Amber ▲ | Slate ○
      </small>
    </div>

    <div
      v-if="props.mode === 'explore'"
      class="map-environment"
    >
      ELEV: 412m&nbsp;&nbsp;•&nbsp;&nbsp;RAINFALL: 318mm/yr
    </div>

    <div
      v-if="props.mode === 'plan'"
      class="map-scale"
    >
      50 km
    </div>
  </section>
</template>

<style scoped>
.map-shell {
  position: relative;
  min-height: 590px;
  overflow: hidden;
  background: #dfe3e1;
  border: 1px solid #dfe5e1;
  border-radius: 12px;
}

.map-shell.planning-map {
  min-height: 760px;
  background: #17251e;
  border-color: #25382e;
}

#habitat-map {
  z-index: 1;
  width: 100%;
  min-height: 590px;
}

.planning-map #habitat-map {
  min-height: 760px;
}

:deep(.leaflet-container) {
  font-family: inherit;
  background: #e2e5e3;
}

.planning-map :deep(.leaflet-container) {
  background: #17251e;
}

:deep(.leaflet-tile-pane) {
  filter: saturate(0.55) brightness(0.92);
}

.planning-map :deep(.leaflet-tile-pane) {
  filter:
    invert(90%)
    hue-rotate(180deg)
    brightness(85%)
    contrast(85%)
    sepia(15%);
}

:deep(.leaflet-control-zoom) {
  overflow: hidden;
  border: 0 !important;
  border-radius: 6px !important;
  box-shadow: 0 3px 10px rgba(10, 30, 20, 0.2) !important;
}

:deep(.leaflet-control-zoom a) {
  color: #344b3e !important;
  background: rgba(255, 255, 255, 0.95) !important;
  border-bottom-color: #e0e6e2 !important;
}

.map-context {
  position: absolute;
  z-index: 500;
  top: 14px;
  left: 14px;
  display: flex;
  max-width: calc(100% - 86px);
  padding: 7px 10px;
  color: #42524a;
  font-size: 12px;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.94);
  border-radius: 7px;
  box-shadow: 0 2px 7px rgba(26, 56, 42, 0.1);
}

.context-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  background: #2e8b61;
  border-radius: 50%;
}

.terrain-label {
  padding-left: 8px;
  border-left: 1px solid #dce2de;
}

.watch-zone-toolbar {
  position: absolute;
  z-index: 600;
  top: 14px;
  left: 14px;
  display: flex;
  max-width: calc(100% - 28px);
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.toolbar-buttons {
  display: flex;
  padding: 5px;
  align-items: center;
  gap: 3px;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 6px;
  box-shadow: 0 3px 10px rgba(10, 24, 17, 0.2);
}

.toolbar-buttons button {
  padding: 7px 10px;
  color: #536159;
  font-size: 12px;
  font-weight: 600;
  background: transparent;
  border: 0;
  border-radius: 5px;
  cursor: pointer;
}

.toolbar-buttons button.active {
  color: #ffffff;
  background: #2c7657;
}

.toolbar-hint {
  padding: 6px 9px;
  color: #45564d;
  font-size: 11px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 5px;
}

.map-legend {
  position: absolute;
  z-index: 500;
  bottom: 16px;
  left: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(21, 47, 34, 0.16);
}

.legend-heading {
  display: flex;
  margin-bottom: 9px;
  align-items: center;
  gap: 8px;
}

.legend-heading strong {
  color: #405047;
  font-size: 12px;
}

.legend-heading span {
  color: #6e7a73;
  font-size: 10px;
}

.mini-levels {
  display: flex;
  font-size: 12px;
  font-weight: 600;
  gap: 14px;
}

.high-level {
  color: #3265e8;
}

.medium-level {
  color: #c97516;
}

.low-level {
  color: #79847f;
}

.map-legend small {
  display: block;
  margin-top: 9px;
  color: #718078;
  font-size: 10px;
}

.map-environment {
  position: absolute;
  z-index: 500;
  right: 16px;
  bottom: 16px;
  padding: 7px 9px;
  color: #637068;
  font-size: 11px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 5px;
}

.map-scale {
  position: absolute;
  z-index: 500;
  right: 62px;
  bottom: 16px;
  padding: 6px 9px;
  color: #56635c;
  font-size: 11px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.94);
  border-radius: 4px;
}

:deep(.potential-marker-wrapper) {
  background: transparent;
  border: 0;
}

:deep(.potential-marker) {
  display: grid;
  width: 190px;
  min-height: 48px;
  padding: 7px 9px;
  cursor: pointer;
  grid-template-columns: 14px 1fr auto;
  text-align: left;
  align-items: center;
  gap: 7px;
  background: #ffffff;
  border: 2px solid;
  border-radius: 8px;
  box-shadow: 0 6px 16px rgba(17, 38, 28, 0.25);
}

:deep(.potential-marker:hover) {
  transform: translateY(-2px);
}

:deep(.potential-marker strong),
:deep(.potential-marker small) {
  display: block;
}

:deep(.potential-marker strong) {
  font-size: 14px;
}

:deep(.potential-marker small) {
  margin-top: 2px;
  color: #68736d;
  font-size: 11px;
}

:deep(.potential-marker b) {
  padding: 3px 5px;
  color: #ffffff;
  font-size: 12px;
  border-radius: 4px;
}

:deep(.marker-high) {
  color: #3265e8;
  border-color: #3265e8;
}

:deep(.marker-high b),
:deep(.marker-high .marker-shape) {
  background: #3265e8;
}

:deep(.marker-medium) {
  color: #c97516;
  border-color: #df8b24;
}

:deep(.marker-medium b),
:deep(.marker-medium .marker-shape) {
  background: #df8b24;
}

:deep(.marker-low) {
  color: #747f79;
  border-color: #9aa39e;
}

:deep(.marker-low b),
:deep(.marker-low .marker-shape) {
  background: #8c9791;
}

:deep(.marker-shape) {
  display: block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  transform: rotate(45deg);
}

:deep(.potential-circle) {
  filter: blur(5px);
}

:deep(.heat-area) {
  filter: blur(17px);
}

:deep(.watch-zone-tooltip) {
  padding: 0;
  background: #ffffff;
  border: 0;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(8, 24, 16, 0.28);
}

:deep(.watch-zone-tooltip::before) {
  border-top-color: #ffffff;
}

:deep(.watch-zone-popup) {
  display: flex;
  min-width: 205px;
  padding: 11px;
  flex-direction: column;
  gap: 5px;
  color: #48564f;
  font-size: 12px;
}

:deep(.watch-zone-heading) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

:deep(.watch-zone-heading strong) {
  color: #2d7a58;
  font-size: 12px;
}

:deep(.watch-zone-heading small) {
  color: #77837d;
  font-size: 10px;
}

:deep(.watch-zone-popup span b) {
  color: #30463a;
}

:deep(.watch-zone-popup mark) {
  padding: 2px 5px;
  color: #ffffff;
  background: #3265e8;
  border-radius: 3px;
}

:deep(.watch-zone-actions) {
  display: flex;
  padding-top: 5px;
  justify-content: flex-end;
  gap: 8px;
  border-top: 1px solid #e7ece8;
}

:deep(.watch-zone-actions button) {
  padding: 2px;
  color: #2d7a58;
  font-size: 10px;
  background: transparent;
  border: 0;
}

:deep(.leaflet-container img.leaflet-tile) {
  width: 256px !important;
  height: 256px !important;
  max-width: none !important;
  max-height: none !important;
}

@media (max-width: 700px) {
  .map-shell,
  #habitat-map {
    min-height: 500px;
  }

  .map-shell.planning-map,
  .planning-map #habitat-map {
    min-height: 620px;
  }

  .map-context {
    align-items: flex-start;
    flex-direction: column;
  }

  .terrain-label {
    padding-left: 0;
    border-left: 0;
  }

  .map-environment {
    display: none;
  }

  .toolbar-buttons {
    flex-wrap: wrap;
  }

  .mini-levels {
    flex-direction: column;
    gap: 4px;
  }
}
</style>
<style scoped>
:deep(.habitat-tooltip) {
  background: #ffffff;
  border: 1px solid #d4ddd8;
  border-radius: 6px;
  color: #2b4137;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(17, 38, 28, 0.15);
  padding: 6px 10px;
}
:deep(.habitat-tooltip strong) {
  color: #2c7657;
}
</style>
<style>
.viewing-point-tooltip {
  background: white;
  border: 1px solid #d5e0da;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 8px 12px;
  color: #173d2d;
  font-family: inherit;
}
.viewing-point-tooltip strong {
  display: block;
  font-size: 17px;
  margin-bottom: 2px;
}
</style>
