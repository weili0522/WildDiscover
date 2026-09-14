<script setup>
import { computed, ref } from 'vue'

import HabitatMap from '../components/HabitatMap.vue'
import MapControls from '../components/MapControls.vue'
import MapGuide from '../components/MapGuide.vue'
import PredictionLegend from '../components/PredictionLegend.vue'
import SpeciesSelector from '../components/SpeciesSelector.vue'
import { useRouter } from 'vue-router'
import {defaultMapFilters, targetSpecies} from '../mocks/mapOptions'

const router = useRouter()
const mapStep = ref('explore')
const selectedSpeciesId = ref('night-parrot')
const selectedPotential = ref(null)

const activeFilters = ref({
  selectedSpecies: [...defaultMapFilters.selectedSpecies],
  region: defaultMapFilters.region,
  climateHorizon: defaultMapFilters.climateHorizon,
  probability: defaultMapFilters.probability,
  selectedLayers: [...defaultMapFilters.selectedLayers]
})

const selectedSpecies = computed(() =>
  targetSpecies.find(
    (species) => species.id === selectedSpeciesId.value
  )
)

function selectSpecies(speciesId) {
  selectedSpeciesId.value = speciesId
  activeFilters.value.selectedSpecies = [speciesId]
}

function selectPotential(point) {
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

  console.log('Mock map filters updated:', updatedFilters)
}

function saveZone() {
  const savedZone = {
    species: selectedSpecies.value,
    potential: selectedPotential.value,
    filters: activeFilters.value,
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
  <div class="map-page">
    <div class="map-container">
      <!-- State 1: Explore a Species -->
      <template v-if="mapStep === 'explore'">
        <section class="map-heading">
          <span class="heading-badge">
            ◉ Habitat Prediction Map
          </span>

          <h1>Explore a Species</h1>

          <p>
            Choose a bird to explore its predicted habitat across Australia.
          </p>
        </section>

        <SpeciesSelector
          :selected-species-id="selectedSpeciesId"
          @select="selectSpecies"
        />

        <section class="exploration-layout">
          <div class="map-column">
            <HabitatMap
              key="explore-map"
              mode="explore"
              @select-potential="selectPotential"
            />
          </div>

          <aside class="information-sidebar">
            <MapGuide :active-step="2" />

            <PredictionLegend />

            <div class="selected-species-card">
              <span>ACTIVE SPECIES</span>

              <strong>{{ selectedSpecies?.commonName }}</strong>

              <em>{{ selectedSpecies?.scientificName }}</em>

              <small>◎ {{ selectedSpecies?.habitat }}</small>
            </div>
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
              <span v-if="species.id === selectedSpeciesId">✓</span>
              {{ species.commonName }}
            </button>

            <button class="species-pill" type="button">
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
  </div>
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

.map-heading {
  margin-bottom: 25px;
}

.heading-badge {
  display: inline-flex;
  margin-bottom: 11px;
  padding: 6px 11px;
  color: #24704f;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  align-items: center;
  background: #ccefdc;
  border-radius: 15px;
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

.exploration-layout {
  display: grid;
  grid-template-columns: minmax(0, 2.15fr) minmax(280px, 1fr);
  margin-top: 18px;
  align-items: start;
  gap: 20px;
}

.map-column {
  min-width: 0;
}

.information-sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.selected-species-card {
  display: flex;
  padding: 18px 20px;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e1e8e3;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(26, 69, 49, 0.05);
}

.selected-species-card > span {
  margin-bottom: 8px;
  color: #31805e;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.selected-species-card strong {
  color: #234d39;
  font-size: 15px;
}

.selected-species-card em {
  margin-top: 3px;
  color: #6c7871;
  font-family: Georgia, serif;
  font-size: 11px;
}

.selected-species-card small {
  margin-top: 10px;
  color: #4e675b;
  font-size: 10px;
  font-weight: 600;
}

.planning-navigation {
  display: flex;
  margin-bottom: 22px;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.back-button {
  padding: 8px 0;
  color: #335648;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  background: transparent;
  border: 0;
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
  color: #65716a;
  font-size: 10px;
  font-weight: 600;
  background: #eef1ef;
  border: 0;
  border-radius: 17px;
}

.species-pill.active {
  color: #ffffff;
  background: #2d7a58;
}

.planning-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.85fr) minmax(310px, 0.9fr);
  align-items: start;
  gap: 20px;
}

@media (max-width: 960px) {
  .planning-navigation {
    align-items: flex-start;
    flex-direction: column;
  }

  .species-pills {
    justify-content: flex-start;
  }

  .planning-layout {
    grid-template-columns: 1fr;
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

  .selected-species-card {
    grid-column: auto;
  }
}
</style>