<script setup>
import { reactive } from 'vue'
import {
  targetSpecies,
  australianRegions,
  climateHorizons,
  environmentalLayers,
  defaultMapFilters
} from '../mocks/mapOptions'

const props = defineProps({
  initialFilters: {
    type: Object,
    default: () => defaultMapFilters
  }
})

const emit = defineEmits(['update:filters', 'save-zone'])

const filters = reactive({
  selectedSpecies: [...props.initialFilters.selectedSpecies],
  region: props.initialFilters.region,
  climateHorizon: props.initialFilters.climateHorizon,
  probability: props.initialFilters.probability,
  selectedLayers: [...props.initialFilters.selectedLayers]
})

function toggleSpecies(speciesId) {
  const index = filters.selectedSpecies.indexOf(speciesId)

  if (index >= 0) {
    if (filters.selectedSpecies.length > 1) {
      filters.selectedSpecies.splice(index, 1)
    }
  } else {
    filters.selectedSpecies.push(speciesId)
  }

  emitFilters()
}

function toggleLayer(layerId) {
  const index = filters.selectedLayers.indexOf(layerId)

  if (index >= 0) {
    filters.selectedLayers.splice(index, 1)
  } else {
    filters.selectedLayers.push(layerId)
  }

  emitFilters()
}

function emitFilters() {
  emit('update:filters', {
    selectedSpecies: [...filters.selectedSpecies],
    region: filters.region,
    climateHorizon: filters.climateHorizon,
    probability: Number(filters.probability),
    selectedLayers: [...filters.selectedLayers]
  })
}

function saveZone() {
  emitFilters()
  emit('save-zone')
}
</script>

<template>
  <aside class="controls-sidebar">
    <section class="controls-introduction">
      <h2>Habitat Exploration Controls</h2>

      <p>
        Adjust citizen-science model layers and filter habitat
        occurrence predictions.
      </p>
    </section>

    <section class="controls-card">
      <!-- Species -->
      <div class="control-section">
        <label>Species Selection</label>

        <div class="pill-list">
          <button
            v-for="species in targetSpecies.slice(0, 4)"
            :key="species.id"
            class="filter-pill"
            :class="{
              active: filters.selectedSpecies.includes(species.id)
            }"
            type="button"
            @click="toggleSpecies(species.id)"
          >
            {{ species.commonName }}
          </button>
        </div>
      </div>

      <!-- Region -->
      <div class="control-section">
        <div class="section-label">
          <label>Region</label>
          <span>Pilbara Focus</span>
        </div>

        <div class="pill-list">
          <button
            v-for="region in australianRegions"
            :key="region.code"
            class="filter-pill"
            :class="{ active: filters.region === region.code }"
            type="button"
            @click="filters.region = region.code; emitFilters()"
          >
            {{ region.name }}
          </button>
        </div>
      </div>

      <!-- Climate horizon -->
      <div class="control-section">
        <label>Time &amp; Climate Horizon</label>

        <div class="climate-options">
          <button
            v-for="horizon in climateHorizons"
            :key="horizon.id"
            class="climate-button"
            :class="{
              active: filters.climateHorizon === horizon.id
            }"
            type="button"
            @click="
              filters.climateHorizon = horizon.id;
              emitFilters()
            "
          >
            {{ horizon.label }}
          </button>
        </div>
      </div>

      <!-- Probability -->
      <div class="control-section">
        <div class="section-label">
          <label for="probability-threshold">
            Probability Threshold
          </label>

          <strong>≥ {{ filters.probability }}%</strong>
        </div>

        <input
          id="probability-threshold"
          v-model="filters.probability"
          class="probability-slider"
          type="range"
          min="0"
          max="100"
          step="1"
          @input="emitFilters"
        >

        <div class="range-labels">
          <span>Broad Search (0%)</span>
          <span>High Confidence (≥70%)</span>
          <span>Strict (100%)</span>
        </div>
      </div>

      <!-- Environmental layers -->
      <div class="control-section layers-section">
        <label>Environmental Layers</label>

        <button
          v-for="layer in environmentalLayers"
          :key="layer.id"
          class="layer-option"
          type="button"
          @click="toggleLayer(layer.id)"
        >
          <span class="layer-name">
            <span class="layer-icon">⌁</span>
            {{ layer.label }}
          </span>

          <span
            class="layer-checkbox"
            :class="{
              checked: filters.selectedLayers.includes(layer.id)
            }"
          >
            ✓
          </span>
        </button>
      </div>
    </section>

    <section class="suitability-card">
      <h3>◉ Why is this area suitable?</h3>

      <p>
        Contains contiguous long-unburnt Triodia basedowii hummocks,
        providing nesting tunnels. Water access is available within
        ephemeral pools, with low feral predator index.
      </p>
    </section>

    <section class="save-card">
      <button
        class="save-button"
        type="button"
        @click="saveZone"
      >
        Save Zone to Investigation Journal
        <span>→</span>
      </button>
    </section>
  </aside>
</template>

<style scoped>
.controls-sidebar {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.controls-introduction,
.controls-card,
.suitability-card,
.save-card {
  padding: 18px;
  background: #ffffff;
  border: 1px solid #e1e7e3;
  border-radius: 11px;
}

.controls-introduction h2 {
  margin: 0 0 8px;
  color: #2d4037;
  font-size: 21px;
  font-weight: 700;
  line-height: 1.1;
}

.controls-introduction p,
.suitability-card p {
  margin: 0;
  color: #707c75;
  font-size: 10px;
  line-height: 1.5;
}

.control-section {
  padding: 15px 0;
  border-bottom: 1px solid #e8ece9;
}

.control-section:first-child {
  padding-top: 0;
}

.control-section:last-child {
  padding-bottom: 0;
  border-bottom: 0;
}

.control-section label {
  display: block;
  margin-bottom: 9px;
  color: #59665f;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.section-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-label span {
  color: #3a8a68;
  font-size: 8px;
  font-weight: 600;
}

.section-label strong {
  padding: 4px 7px;
  color: #287251;
  font-size: 10px;
  background: #e5f3eb;
  border-radius: 5px;
}

.pill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.filter-pill,
.climate-button {
  padding: 6px 10px;
  color: #667169;
  font-size: 9px;
  background: #f0f2f0;
  border: 0;
  border-radius: 15px;
}

.filter-pill.active,
.climate-button.active {
  color: #ffffff;
  background: #2d7a58;
}

.climate-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.climate-button {
  border-radius: 6px;
}

.probability-slider {
  width: 100%;
  accent-color: #3265e8;
}

.range-labels {
  display: flex;
  margin-top: 5px;
  color: #8a938e;
  font-size: 7px;
  justify-content: space-between;
}

.layer-option {
  display: flex;
  width: 100%;
  padding: 8px 2px;
  color: #4e5d55;
  font-size: 10px;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: 0;
}

.layer-name {
  display: flex;
  align-items: center;
  gap: 7px;
}

.layer-icon {
  color: #2f815e;
  font-size: 13px;
}

.layer-checkbox {
  display: grid;
  width: 14px;
  height: 14px;
  color: transparent;
  font-size: 8px;
  place-items: center;
  border: 1px solid #91a099;
  border-radius: 2px;
}

.layer-checkbox.checked {
  color: #ffffff;
  background: #2d7a58;
  border-color: #2d7a58;
}

.suitability-card h3 {
  margin: 0 0 9px;
  color: #3f5148;
  font-size: 11px;
  font-weight: 700;
}

.save-card {
  padding: 15px;
}

.save-button {
  display: flex;
  width: 100%;
  padding: 13px 16px;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #2d7a58;
  border: 0;
  border-radius: 7px;
}

.save-button:hover {
  background: #1f6044;
}
</style>