<script setup>
import { onBeforeUnmount, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import { habitatPotentialPoints } from '../mocks/mapOptions'

const props = defineProps({
  mode: {
    type: String,
    default: 'explore'
  }
})

const emit = defineEmits(['select-potential'])

let map = null

const levelStyles = {
  high: {
    color: '#3265e8',
    fillColor: '#3265e8',
    radius: 65000
  },
  medium: {
    color: '#df8b24',
    fillColor: '#df8b24',
    radius: 85000
  },
  low: {
    color: '#8c9791',
    fillColor: '#8c9791',
    radius: 55000
  }
}

function createMarkerIcon(point) {
  return L.divIcon({
    className: 'potential-marker-wrapper',
    html: `
      <button class="potential-marker marker-${point.id}" type="button">
        <span class="marker-shape"></span>

        <span class="marker-content">
          <strong>${point.level}</strong>
          <small>${point.location}</small>
        </span>

        <b>${point.probability}%</b>
      </button>
    `,
    iconSize: [190, 52],
    iconAnchor: [95, 26]
  })
}

onMounted(() => {
  map = L.map('habitat-map', {
    zoomControl: false
  }).setView([-22.4, 118.75], 7)

  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }
  ).addTo(map)

  L.control.zoom({
    position: 'topright'
  }).addTo(map)

  habitatPotentialPoints.forEach((point) => {
    const style = levelStyles[point.id]

    L.circle(
      [point.latitude, point.longitude],
      {
        radius: style.radius,
        color: style.color,
        fillColor: style.fillColor,
        fillOpacity: 0.3,
        opacity: 0.7,
        weight: 2
      }
    ).addTo(map)

    const marker = L.marker(
      [point.latitude, point.longitude],
      {
        icon: createMarkerIcon(point)
      }
    ).addTo(map)

    marker.on('click', () => {
      emit('select-potential', point)
    })
  })

    if (['plan', 'detail', 'summary'].includes(props.mode)) {
      const watchZoneCoordinates = [
        [-22.18, 118.63],
        [-22.18, 118.94],
        [-22.52, 118.98],
        [-22.58, 118.65]
      ]

      const watchZone = L.polygon(
        watchZoneCoordinates,
        {
          color: '#2f8f67',
          fillColor: '#56b58a',
          fillOpacity: 0.12,
          weight: 3,
          dashArray: '7 6'
        }
      ).addTo(map)

      watchZone.bindTooltip(
        `
          <div class="watch-zone-popup">
            <strong>Watch Zone Created</strong>
            <span>Night Parrot • Area: 14.2 km²</span>
            <span>Avg Suitability: <b>82%</b></span>
          </div>
        `,
        {
          permanent: true,
          direction: 'top',
          className: 'watch-zone-tooltip'
        }
      )

      map.fitBounds(watchZone.getBounds(), {
        padding: [90, 90]
      })
    }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<template>
  <section class="map-shell">
    <div
      v-if="props.mode === 'plan'"
      class="watch-zone-toolbar"
    >
      <button type="button" class="active">
        ⌖ Draw Watch Zone
      </button>

      <button type="button">
        ✎ Edit Zone
      </button>

      <button type="button">
        ♲ Clear
      </button>

      <span>
        ● Click and drag handles to resize, or click map to trace points.
      </span>
    </div>
    
    <div class="map-context">
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
      <strong>HABITAT POTENTIAL</strong>

      <div class="mini-levels">
        <span class="high-level">◆ High ≥70%</span>
        <span class="medium-level">▲ Medium 40–69%</span>
        <span class="low-level">○ Low &lt;40%</span>
      </div>
    </div>

    <div class="map-environment">
      ELEV: 412m&nbsp;&nbsp;•&nbsp;&nbsp;RAINFALL: 318mm/yr
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

#habitat-map {
  width: 100%;
  min-height: 590px;
  z-index: 1;
}

:deep(.leaflet-tile-pane) {
  filter: saturate(0.5) brightness(0.92);
}

.map-context {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 500;
  display: flex;
  max-width: calc(100% - 86px);
  padding: 7px 10px;
  color: #42524a;
  font-size: 9px;
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

.map-legend {
  position: absolute;
  bottom: 16px;
  left: 16px;
  z-index: 500;
  padding: 12px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(21, 47, 34, 0.12);
}

.map-legend > strong {
  display: block;
  margin-bottom: 9px;
  color: #405047;
  font-size: 9px;
}

.mini-levels {
  display: flex;
  font-size: 9px;
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

.map-environment {
  position: absolute;
  right: 16px;
  bottom: 16px;
  z-index: 500;
  padding: 7px 9px;
  color: #637068;
  font-size: 8px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 5px;
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
  box-shadow: 0 6px 16px rgba(17, 38, 28, 0.2);
}

:deep(.potential-marker:hover) {
  transform: translateY(-2px);
}

:deep(.potential-marker strong),
:deep(.potential-marker small) {
  display: block;
}

:deep(.potential-marker strong) {
  font-size: 11px;
}

:deep(.potential-marker small) {
  margin-top: 2px;
  color: #68736d;
  font-size: 8px;
}

:deep(.potential-marker b) {
  padding: 3px 5px;
  color: #ffffff;
  font-size: 9px;
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

/* Prevent global responsive image styles from stretching Leaflet tiles */
:deep(.leaflet-container img.leaflet-tile) {
  width: 256px !important;
  height: 256px !important;
  max-width: none !important;
  max-height: none !important;
}

:deep(.leaflet-container) {
  font-family: inherit;
}

.watch-zone-toolbar {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 600;
  display: flex;
  max-width: calc(100% - 85px);
  padding: 7px;
  flex-wrap: wrap;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 7px;
  box-shadow: 0 2px 8px rgba(18, 43, 31, 0.15);
}

.watch-zone-toolbar button {
  padding: 6px 9px;
  color: #536159;
  font-size: 9px;
  font-weight: 600;
  background: transparent;
  border: 0;
  border-radius: 5px;
}

.watch-zone-toolbar button.active {
  color: #ffffff;
  background: #2c7657;
}

.watch-zone-toolbar > span {
  flex-basis: 100%;
  padding: 5px 8px;
  color: #506058;
  font-size: 8px;
  background: #f7f9f7;
  border-radius: 4px;
}

:deep(.watch-zone-tooltip) {
  padding: 0;
  background: #ffffff;
  border: 0;
  border-radius: 8px;
  box-shadow: 0 5px 18px rgba(16, 38, 27, 0.22);
}

:deep(.watch-zone-popup) {
  display: flex;
  min-width: 180px;
  padding: 11px;
  flex-direction: column;
  gap: 5px;
  color: #48564f;
  font-size: 9px;
}

:deep(.watch-zone-popup strong) {
  color: #2d7a58;
  font-size: 10px;
}

:deep(.watch-zone-popup b) {
  padding: 2px 4px;
  color: #ffffff;
  background: #3265e8;
  border-radius: 3px;
}

@media (max-width: 700px) {
  .map-shell,
  #habitat-map {
    min-height: 500px;
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

  .mini-levels {
    flex-direction: column;
    gap: 4px;
  }
}
</style>