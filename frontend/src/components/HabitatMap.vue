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
let watchZone = null

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

const watchZoneCoordinates = [
  [-22.18, 118.63],
  [-22.18, 118.94],
  [-22.52, 118.98],
  [-22.58, 118.65]
]

function createMarkerIcon(point) {
  return L.divIcon({
    className: 'potential-marker-wrapper',
    html: `
      <button
        class="potential-marker marker-${point.id}"
        type="button"
        aria-label="${point.level} ${point.probability}%"
      >
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

function addPotentialArea(point) {
  const style = levelStyles[point.id]

  L.circle(
    [point.latitude, point.longitude],
    {
      radius:
        props.mode === 'plan'
          ? style.radius * 1.25
          : style.radius,
      color: style.color,
      fillColor: style.fillColor,
      fillOpacity: props.mode === 'plan' ? 0.48 : 0.3,
      opacity: props.mode === 'plan' ? 0.2 : 0.7,
      weight: props.mode === 'plan' ? 1 : 2,
      className: `potential-circle potential-${point.id}`
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
}

function addPlanningDecorations() {
  const decorativeAreas = [
    {
      coordinates: [-22.34, 118.5],
      radius: 110000,
      color: '#dd8a19',
      opacity: 0.27
    },
    {
      coordinates: [-22.39, 118.81],
      radius: 76000,
      color: '#286be8',
      opacity: 0.48
    },
    {
      coordinates: [-22.22, 119.04],
      radius: 98000,
      color: '#dc8a1d',
      opacity: 0.28
    },
    {
      coordinates: [-22.47, 118.8],
      radius: 175000,
      color: '#899590',
      opacity: 0.17
    }
  ]

  decorativeAreas.forEach((area) => {
    L.circle(area.coordinates, {
      radius: area.radius,
      color: 'transparent',
      fillColor: area.color,
      fillOpacity: area.opacity,
      weight: 0,
      className: 'heat-area'
    }).addTo(map)
  })

  watchZone = L.polygon(
    watchZoneCoordinates,
    {
      color: '#42bd89',
      fillColor: '#42bd89',
      fillOpacity: 0.09,
      weight: 2,
      dashArray: '7 6'
    }
  ).addTo(map)

  watchZoneCoordinates.forEach((coordinate) => {
    L.circleMarker(coordinate, {
      radius: 4,
      color: '#ffffff',
      fillColor: '#42bd89',
      fillOpacity: 1,
      weight: 2
    }).addTo(map)
  })

  watchZone.bindTooltip(
    `
      <div class="watch-zone-popup">
        <div class="watch-zone-heading">
          <strong>◉ Watch Zone Created</strong>
          <small>Pilbara Sector 4</small>
        </div>

        <span>
          <b>Night Parrot</b> • Area: 14.2 km²
        </span>

        <span>
          Avg Suitability:
          <mark>82%</mark>
        </span>

        <div class="watch-zone-actions">
          <button type="button">✎ Edit Zone</button>
          <button type="button">Clear Zone</button>
        </div>
      </div>
    `,
    {
      permanent: true,
      direction: 'top',
      offset: [0, -6],
      className: 'watch-zone-tooltip'
    }
  )

  map.fitBounds(watchZone.getBounds(), {
    padding: [110, 110]
  })
}

function initialiseMap() {
  const isPlanningMode = ['plan', 'detail', 'summary'].includes(
    props.mode
  )

  map = L.map('habitat-map', {
    zoomControl: false,
    attributionControl: false
  }).setView([-22.4, 118.75], 7)

  const tileUrl = isPlanningMode
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

  L.tileLayer(tileUrl, {
    maxZoom: 19
  }).addTo(map)

  L.control.zoom({
    position: 'bottomright'
  }).addTo(map)

  habitatPotentialPoints.forEach(addPotentialArea)

  if (isPlanningMode) {
    addPlanningDecorations()
  }
}

onMounted(() => {
  initialiseMap()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    watchZone = null
  }
})
</script>

<template>
  <section
    class="map-shell"
    :class="{ 'planning-map': props.mode === 'plan' }"
  >
    <div
      v-if="props.mode === 'plan'"
      class="watch-zone-toolbar"
    >
      <div class="toolbar-buttons">
        <button type="button" class="active">
          ⌖ Draw Watch Zone
        </button>

        <button type="button" aria-label="Information">
          ⓘ
        </button>

        <button type="button">
          ✎ Edit Zone
        </button>

        <button type="button">
          ▣ Clear
        </button>
      </div>

      <span class="toolbar-hint">
        ● Click and drag handles to resize, or click map to trace points.
      </span>
    </div>

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
    saturate(0.45)
    brightness(0.68)
    sepia(0.1)
    hue-rotate(85deg);
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
  font-size: 9px;
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
  font-size: 8px;
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
  font-size: 9px;
}

.legend-heading span {
  color: #6e7a73;
  font-size: 7px;
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

.map-legend small {
  display: block;
  margin-top: 9px;
  color: #718078;
  font-size: 7px;
}

.map-environment {
  position: absolute;
  z-index: 500;
  right: 16px;
  bottom: 16px;
  padding: 7px 9px;
  color: #637068;
  font-size: 8px;
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
  font-size: 8px;
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
  font-size: 9px;
}

:deep(.watch-zone-heading) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

:deep(.watch-zone-heading strong) {
  color: #2d7a58;
  font-size: 9px;
}

:deep(.watch-zone-heading small) {
  color: #77837d;
  font-size: 7px;
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
  font-size: 7px;
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