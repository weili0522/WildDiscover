<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import HabitatMap from '../components/HabitatMap.vue'
import MapControls from '../components/MapControls.vue'
import MapGuide from '../components/MapGuide.vue'
import PredictionLegend from '../components/PredictionLegend.vue'
import SpeciesSelector from '../components/SpeciesSelector.vue'

import {
  defaultMapFilters,
  targetSpecies
} from '../mocks/mapOptions'

const router = useRouter()

const mapStep = ref('explore')
const selectedSpeciesId = ref(null)
const selectedPotential = ref(null)

const activeFilters = ref({
  selectedSpecies: [],
  region: defaultMapFilters.region,
  climateHorizon: defaultMapFilters.climateHorizon,
  probability: defaultMapFilters.probability,
  selectedLayers: [...defaultMapFilters.selectedLayers]
})

const selectedSpecies = computed(() =>
  targetSpecies.find(
    species => species.id === selectedSpeciesId.value
  )
)

function selectSpecies(speciesOrId) {
  const speciesId =
    typeof speciesOrId === 'string'
      ? speciesOrId
      : speciesOrId?.id

  if (!speciesId) return

  selectedSpeciesId.value = speciesId
  activeFilters.value.selectedSpecies = [speciesId]
}

function selectPotential(point) {
  // The user must choose a species before planning an exploration.
  if (!selectedSpeciesId.value) {
    return
  }

  selectedPotential.value = point

  if (point.id === 'high') {
    mapStep.value = 'plan'
  }
}

function returnToExplore() {
  mapStep.value = 'explore'
  selectedPotential.value = null
}

function updateFilters(updatedFilters) {
  activeFilters.value = updatedFilters

  if (updatedFilters.selectedSpecies?.length) {
    selectedSpeciesId.value = updatedFilters.selectedSpecies[0]
  }

  console.log('Mock map filters updated:', updatedFilters)
}

function saveZone(controlData = {}) {
  const savedZone = {
    species: selectedSpecies.value,
    potential: selectedPotential.value,
    filters: {
      ...activeFilters.value,
      ...controlData
    },
    explorationDate:
      controlData.explorationDate ||
      activeFilters.value.explorationDate ||
      '18 July 2026',
    savedAt: new Date().toISOString()
  }

  localStorage.setItem(
    'wilddiscover_saved_zone',
    JSON.stringify(savedZone)
  )

  router.push('/journal')
}
</script>

<template>
  <main class="map-page">
    <div class="map-container">
      <!-- State 1: Choose a Species -->
      <template v-if="mapStep === 'explore'">
        <section class="explore-grid">
          <div class="explore-main">
            <header class="map-heading">
              <span class="heading-badge">
                ◉ Habitat Prediction Map
              </span>

              <h1>Explore a Species</h1>

              <p>
                Choose a bird to explore its predicted habitat across Australia.
              </p>
            </header>

            <SpeciesSelector
              v-model="selectedSpeciesId"
              :species="targetSpecies"
              @select="selectSpecies"
            />

            <div class="map-column">
              <HabitatMap
                key="explore-map"
                mode="explore"
                @select-potential="selectPotential"
              />

              <p
                v-if="!selectedSpeciesId"
                class="selection-message"
              >
                Select a bird species before choosing a habitat prediction area.
              </p>
            </div>
          </div>

          <aside class="information-sidebar">
            <MapGuide
              :active-step="selectedSpeciesId ? 2 : 1"
            />

            <section class="threshold-card">
              <div class="threshold-heading">
                <span>PROBABILITY THRESHOLD</span>

                <strong>
                  ≥ {{ activeFilters.probability }}%
                </strong>
              </div>

              <input
                v-model.number="activeFilters.probability"
                class="threshold-slider"
                type="range"
                min="0"
                max="100"
                step="1"
                aria-label="Probability threshold"
              />

              <div class="threshold-labels">
                <span>Broad Search (0%)</span>
                <span>High Confidence (≥70%)</span>
                <span>Strict (100%)</span>
              </div>
            </section>

            <PredictionLegend />
          </aside>
        </section>
      </template>

      <!-- State 2: Plan Your Exploration -->
      <template v-else>
        <section class="planning-navigation">
          <button
            class="back-button"
            type="button"
            @click="returnToExplore"
          >
            ← Back
          </button>

          <div class="species-pills">
            <button
              v-for="species in targetSpecies.slice(0, 4)"
              :key="species.id"
              class="species-pill"
              :class="{
                active: species.id === selectedSpeciesId
              }"
              type="button"
              @click="selectSpecies(species.id)"
            >
              <span v-if="species.id === selectedSpeciesId">
                ✓
              </span>

              {{ species.commonName }}
            </button>

            <button
              class="species-pill"
              type="button"
              @click="returnToExplore"
            >
              + More Species
            </button>
          </div>
        </section>

        <section class="planning-layout">
          <div class="map-column">
            <HabitatMap
              key="planning-map"
              mode="plan"
              @select-potential="selectPotential"
            />
          </div>

          <MapControls
            :key="selectedSpeciesId"
            :initial-filters="activeFilters"
            @update:filters="updateFilters"
            @save-zone="saveZone"
          />
        </section>
      </template>
    </div>
  </main>
</template>

<style scoped>
.map-page {
  min-height: 100vh;
  padding: 40px 24px 70px;
  color: #293d33;
  background: #f7f9f7;
}

.map-container {
  width: 100%;
  max-width: 1320px;
  margin: 0 auto;
}

/* Explore state */

.explore-grid {
  display: grid;
  grid-template-columns:
    minmax(0, 2.15fr)
    minmax(280px, 1fr);
  align-items: start;
  gap: 24px;
}

.explore-main {
  min-width: 0;
}

.map-heading {
  margin-bottom: 22px;
}

.heading-badge {
  display: inline-flex;
  align-items: center;
  margin-bottom: 11px;
  padding: 6px 11px;
  border-radius: 15px;
  background: #ccefdc;
  color: #24704f;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.map-heading h1 {
  margin: 0 0 7px;
  color: #14533a;
  font-size: 34px;
  font-weight: 700;
}

.map-heading p {
  margin: 0;
  color: #69756f;
  font-size: 15px;
}

.map-column {
  min-width: 0;
}

.explore-main .map-column {
  position: relative;
  margin-top: 16px;
}

.selection-message {
  position: absolute;
  right: 16px;
  bottom: 16px;
  left: 16px;
  z-index: 500;
  margin: 0;
  padding: 10px 14px;
  border: 1px solid #dbe7df;
  border-radius: 8px;
  background: rgb(255 255 255 / 92%);
  color: #5a6e63;
  font-size: 11px;
  text-align: center;
  pointer-events: none;
  backdrop-filter: blur(4px);
}

.information-sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* Probability threshold */

.threshold-card {
  padding: 18px 20px;
  border: 1px solid #e1e8e3;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 3px 12px rgb(26 69 49 / 5%);
}

.threshold-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 10px;
}

.threshold-heading span {
  color: #53675d;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.threshold-heading strong {
  padding: 4px 8px;
  border-radius: 5px;
  background: #e5f5eb;
  color: #287b57;
  font-size: 12px;
}

.threshold-slider {
  width: 100%;
  height: 5px;
  accent-color: #3478d4;
  cursor: pointer;
}

.threshold-labels {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-top: 8px;
  color: #7b8780;
  font-size: 8px;
}

.threshold-labels span {
  flex: 1;
}

.threshold-labels span:nth-child(2) {
  text-align: center;
}

.threshold-labels span:last-child {
  text-align: right;
}

/* Planning state */

.planning-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}

.back-button {
  padding: 8px 0;
  border: 0;
  background: transparent;
  color: #335648;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;
}

.back-button:hover {
  color: #1e7a55;
}

.species-pills {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 7px;
}

.species-pill {
  padding: 8px 13px;
  border: 0;
  border-radius: 17px;
  background: #eef1ef;
  color: #65716a;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
}

.species-pill:hover {
  background: #e2ebe6;
  color: #2d684e;
}

.species-pill.active {
  background: #2d7a58;
  color: #ffffff;
}

.planning-layout {
  display: grid;
  grid-template-columns:
    minmax(0, 1.85fr)
    minmax(310px, 0.9fr);
  align-items: start;
  gap: 20px;
}

/* Responsive */

@media (max-width: 960px) {
  .explore-grid,
  .planning-layout {
    grid-template-columns: 1fr;
  }

  .information-sidebar {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .information-sidebar > :first-child {
    grid-column: 1 / -1;
  }

  .planning-navigation {
    align-items: flex-start;
    flex-direction: column;
  }

  .species-pills {
    justify-content: flex-start;
  }
}

@media (max-width: 650px) {
  .map-page {
    padding: 28px 14px 50px;
  }

  .map-heading h1 {
    font-size: 29px;
  }

  .information-sidebar {
    grid-template-columns: 1fr;
  }

  .information-sidebar > :first-child {
    grid-column: auto;
  }

  .threshold-labels {
    font-size: 7px;
  }

  .species-pills {
    gap: 6px;
  }

  .species-pill {
    padding: 7px 10px;
  }
}
</style>