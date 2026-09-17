<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import HabitatMap from '../components/HabitatMap.vue'
import MapGuide from '../components/MapGuide.vue'
import PredictionLegend from '../components/PredictionLegend.vue'
import SpeciesSelector from '../components/SpeciesSelector.vue'
import { useExplorer } from '../composables/useExplorer'

import { defaultMapFilters, targetSpecies } from '../mocks/mapOptions'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const router = useRouter()

const { explorer, isGuest } = useExplorer()

const selectedSpeciesId = ref(null)
const selectedPotential = ref(null)
const showViewingPoints = ref(false)

const showDateModal = ref(false)
const explorationDate = ref('2026-07-18')

const activeFilters = ref({
  selectedSpecies: [],
  region: defaultMapFilters.region,
  climateHorizon: defaultMapFilters.climateHorizon,
  probability: defaultMapFilters.probability,
  selectedLayers: [...defaultMapFilters.selectedLayers]
})

const selectedSpecies = computed(() =>
  targetSpecies.find(species => species.id === selectedSpeciesId.value)
)

function selectSpecies(speciesOrId) {
  const speciesId = typeof speciesOrId === 'string' ? speciesOrId : speciesOrId?.id
  if (!speciesId) return

  selectedSpeciesId.value = speciesId
  activeFilters.value.selectedSpecies = [speciesId]
  selectedPotential.value = null // reset potential when species changes
}

function selectPotential(point) {
  if (!selectedSpeciesId.value) return
  selectedPotential.value = point
}

async function confirmSaveZone() {
  if (isGuest.value || !explorer.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/journal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: explorer.value.displayName,
        species_id: selectedSpeciesId.value,
        exploration_date: explorationDate.value
      })
    })
    
    if (!res.ok) throw new Error('Failed to save journal')
    router.push('/journal')
  } catch (e) {
    console.error(e)
    alert('Failed to save your journey')
  }
}
</script>

<template>
  <main class="map-page">
    <div class="map-container">
      <section class="explore-grid">
        <div class="explore-main">
          <header class="map-heading">
            <span class="heading-badge">◉ Habitat Prediction Map</span>
            <h1>Explore a Species</h1>
            <p>Choose a bird to explore its predicted habitat across Australia.</p>
          </header>

          <SpeciesSelector
            v-model="selectedSpeciesId"
            :species="targetSpecies"
            @select="selectSpecies"
          />



          <div class="map-column">
            <HabitatMap
              key="explore-map"
              :species-id="selectedSpeciesId"
              :show-viewing-points="showViewingPoints"
              :probability-threshold="activeFilters.probability"
              @select-potential="selectPotential"
            />
            <p v-if="!selectedSpeciesId" class="selection-message">
              Select a bird species before choosing a habitat prediction area.
            </p>
          </div>
        </div>

        <aside class="information-sidebar">
          <MapGuide :active-step="selectedSpeciesId ? 2 : 1" />
          <section class="toggle-card">
            <label class="toggle-checkbox-card">
              <input type="checkbox" v-model="showViewingPoints" />
              <span>Show Popular Viewing Points</span>
            </label>
          </section>
          
          <section class="threshold-card">
            <div class="threshold-heading">
              <span>PROBABILITY THRESHOLD</span>
              <strong>≥ {{ activeFilters.probability }}%</strong>
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

          <section class="save-zone-card">
            <button 
              class="save-zone-btn" 
              :disabled="!selectedPotential || isGuest"
              @click="showDateModal = true"
            >
              {{ isGuest ? 'Log in to Save Journeys' : 'Save Zone to Investigation Journal' }}
            </button>
          </section>
        </aside>
      </section>

      <!-- Date Modal -->
      <div v-if="showDateModal" class="modal-overlay" @click.self="showDateModal = false">
        <div class="modal-content">
          <h3>Select Exploration Date</h3>
          <input type="date" v-model="explorationDate" class="date-input" />
          <div class="modal-actions">
            <button @click="showDateModal = false" class="cancel-btn">Cancel</button>
            <button @click="confirmSaveZone" class="confirm-btn">Confirm & Save</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<style scoped>

.toggle-card {
  padding: 18px 20px;
  border: 1px solid #e1e8e3;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 3px 12px rgb(26 69 49 / 5%);
}

.toggle-checkbox-card {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 17px;
  color: #244336;
  font-weight: 700;
  cursor: pointer;
}

.toggle-checkbox-card input {
  accent-color: #2b7a54;
  width: 18px;
  height: 18px;
  cursor: pointer;
}





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
  align-items: stretch;
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
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.map-heading h1 {
  margin: 0 0 7px;
  color: #14533a;
  font-size: 37px;
  font-weight: 700;
}

.map-heading p {
  margin: 0;
  color: #69756f;
  font-size: 18px;
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
  font-size: 14px;
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
  margin-top: auto;
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
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.threshold-heading strong {
  padding: 4px 8px;
  border-radius: 5px;
  background: #e5f5eb;
  color: #287b57;
  font-size: 15px;
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
  font-size: 11px;
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
  font-size: 15px;
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
  font-size: 13px;
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
    font-size: 32px;
  }

  .information-sidebar {
    grid-template-columns: 1fr;
  }

  .information-sidebar > :first-child {
    grid-column: auto;
  }

  .threshold-labels {
    font-size: 10px;
  }

  .species-pills {
    gap: 6px;
  }

  .species-pill {
    padding: 7px 10px;
  }
}

.save-zone-card {
  margin-top: 10px;
}
.save-zone-btn {
  width: 100%;
  padding: 14px;
  background-color: #287b57;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}
.save-zone-btn:disabled {
  background-color: #a8b8b0;
  cursor: not-allowed;
}
.save-zone-btn:not(:disabled):hover {
  background-color: #1e6345;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.modal-content h3 {
  margin-top: 0;
  color: #14533a;
}
.date-input {
  width: 100%;
  padding: 10px;
  margin: 16px 0;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 19px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.cancel-btn {
  padding: 10px 16px;
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
}
.confirm-btn {
  padding: 10px 16px;
  background: #287b57;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>