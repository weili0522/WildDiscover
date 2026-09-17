<script setup>
import { computed, reactive, ref } from 'vue'

import {
  australianRegions,
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

const showCalendar = ref(false)
const selectedDate = ref(18)

const filters = reactive({
  region: props.initialFilters.region,
  probability: props.initialFilters.probability,
  selectedLayers: [...props.initialFilters.selectedLayers],
  explorationDate: '18 July 2026'
})

const calendarDays = [
  { key: 'previous-29', number: 29, disabled: true },
  { key: 'previous-30', number: 30, disabled: true },
  { key: 'july-1', number: 1 },
  { key: 'july-2', number: 2 },
  { key: 'july-3', number: 3 },
  { key: 'july-4', number: 4 },
  { key: 'july-5', number: 5 },
  { key: 'july-6', number: 6 },
  { key: 'july-7', number: 7 },
  { key: 'july-8', number: 8 },
  { key: 'july-9', number: 9 },
  { key: 'july-10', number: 10 },
  { key: 'july-11', number: 11 },
  { key: 'july-12', number: 12 },
  { key: 'july-13', number: 13 },
  { key: 'july-14', number: 14 },
  { key: 'july-15', number: 15, recommended: true },
  { key: 'july-16', number: 16, recommended: true },
  { key: 'july-17', number: 17, recommended: true },
  { key: 'july-18', number: 18, recommended: true },
  { key: 'july-19', number: 19, recommended: true },
  { key: 'july-20', number: 20, recommended: true },
  { key: 'july-21', number: 21, recommended: true },
  { key: 'july-22', number: 22 },
  { key: 'july-23', number: 23 },
  { key: 'july-24', number: 24 },
  { key: 'july-25', number: 25 },
  { key: 'july-26', number: 26 },
  { key: 'july-27', number: 27 },
  { key: 'july-28', number: 28 },
  { key: 'july-29', number: 29 },
  { key: 'july-30', number: 30 },
  { key: 'july-31', number: 31 },
  { key: 'next-1', number: 1, disabled: true },
  { key: 'next-2', number: 2, disabled: true }
]

const formattedDate = computed(
  () => `${selectedDate.value} July 2026`
)

function selectDate(day) {
  if (!day.disabled) {
    selectedDate.value = day.number
  }
}

function applyDate() {
  filters.explorationDate = formattedDate.value
  showCalendar.value = false
  emitFilters()
}

function selectRegion(regionCode) {
  filters.region = regionCode
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
    ...props.initialFilters,
    region: filters.region,
    probability: Number(filters.probability),
    selectedLayers: [...filters.selectedLayers],
    explorationDate: filters.explorationDate
  })
}

function saveZone() {
  filters.explorationDate = formattedDate.value
  emitFilters()

  emit('save-zone', {
    explorationDate: filters.explorationDate,
    region: filters.region,
    probability: Number(filters.probability),
    selectedLayers: [...filters.selectedLayers]
  })
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
      <!-- Date -->
      <div class="control-section date-section">
        <div class="section-label">
          <label>Exploration Date</label>
          <span>Recommended: Dry Season</span>
        </div>

        <button
          class="date-input"
          type="button"
          :aria-expanded="showCalendar"
          @click="showCalendar = !showCalendar"
        >
          <span>{{ formattedDate }}</span>
          <span aria-hidden="true">▣</span>
        </button>

        <div
          v-if="showCalendar"
          class="calendar-panel"
        >
          <div class="calendar-header">
            <button type="button" aria-label="Previous month">
              ‹
            </button>

            <strong>July 2026</strong>

            <button type="button" aria-label="Next month">
              ›
            </button>

            <span>● Dry Season Window</span>
          </div>

          <div class="weekday-row">
            <span>MO</span>
            <span>TU</span>
            <span>WE</span>
            <span>TH</span>
            <span>FR</span>
            <span>SA</span>
            <span>SU</span>
          </div>

          <div class="calendar-grid">
            <button
              v-for="day in calendarDays"
              :key="day.key"
              type="button"
              :disabled="day.disabled"
              :class="{
                recommended: day.recommended,
                selected:
                  !day.disabled &&
                  day.number === selectedDate
              }"
              @click="selectDate(day)"
            >
              {{ day.number }}
            </button>
          </div>

          <div class="calendar-footer">
            <button
              class="apply-date-button"
              type="button"
              @click="applyDate"
            >
              Apply Date
            </button>
          </div>
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
            @click="selectRegion(region.code)"
          >
            {{ region.name }}
          </button>
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
        ephemeral pools (≤4.8 km), with low feral predator index.
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
  box-shadow: 0 3px 12px rgba(26, 69, 49, 0.04);
}

.controls-introduction h2 {
  margin: 0 0 8px;
  color: #2d4037;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.1;
}

.controls-introduction p,
.suitability-card p {
  margin: 0;
  color: #707c75;
  font-size: 13px;
  line-height: 1.5;
}

.control-section {
  position: relative;
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
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.section-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.section-label span {
  color: #3a8a68;
  font-size: 11px;
  font-weight: 600;
}

.date-input {
  display: flex;
  width: 100%;
  padding: 10px 11px;
  color: #536159;
  font-size: 13px;
  text-align: left;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border: 1px solid #dfe6e1;
  border-radius: 6px;
  cursor: pointer;
}

.calendar-panel {
  position: relative;
  z-index: 20;
  margin-top: 8px;
  padding: 11px;
  background: #ffffff;
  border: 1px solid #dfe6e1;
  border-radius: 8px;
  box-shadow: 0 10px 26px rgba(20, 55, 39, 0.14);
}

.calendar-header {
  display: grid;
  grid-template-columns: 22px 1fr 22px;
  align-items: center;
}

.calendar-header button {
  width: 22px;
  height: 22px;
  padding: 0;
  color: #506159;
  background: transparent;
  border: 0;
  cursor: pointer;
}

.calendar-header strong {
  color: #405249;
  font-size: 13px;
  text-align: center;
}

.calendar-header > span {
  grid-column: 1 / -1;
  margin: 6px 0 3px;
  color: #35906a;
  font-size: 10px;
  text-align: right;
}

.weekday-row,
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}

.weekday-row {
  margin: 6px 0 4px;
}

.weekday-row span {
  color: #8b948f;
  font-size: 10px;
  text-align: center;
}

.calendar-grid button {
  display: grid;
  min-height: 25px;
  padding: 0;
  color: #58655e;
  font-size: 11px;
  place-items: center;
  background: transparent;
  border: 0;
  border-radius: 5px;
  cursor: pointer;
}

.calendar-grid button:disabled {
  color: #c7ceca;
  cursor: default;
}

.calendar-grid button.recommended {
  color: #267653;
  background: #e0f4e9;
}

.calendar-grid button.selected {
  color: #ffffff;
  font-weight: 700;
  background: #267653;
}

.calendar-footer {
  display: flex;
  margin-top: 8px;
  justify-content: flex-end;
}

.apply-date-button {
  padding: 7px 12px;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  background: #236b4c;
  border: 0;
  border-radius: 5px;
  cursor: pointer;
}

.pill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.filter-pill {
  padding: 6px 10px;
  color: #667169;
  font-size: 11px;
  background: #f0f2f0;
  border: 0;
  border-radius: 15px;
  cursor: pointer;
}

.filter-pill.active {
  color: #ffffff;
  background: #2d7a58;
}

.layer-option {
  display: flex;
  width: 100%;
  padding: 8px 2px;
  color: #4e5d55;
  font-size: 13px;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: 0;
  cursor: pointer;
}

.layer-name {
  display: flex;
  align-items: center;
  gap: 7px;
}

.layer-icon {
  color: #2f815e;
  font-size: 16px;
}

.layer-checkbox {
  display: grid;
  width: 14px;
  height: 14px;
  color: transparent;
  font-size: 11px;
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
  font-size: 14px;
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
  font-size: 14px;
  font-weight: 700;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #2d7a58;
  border: 0;
  border-radius: 7px;
  cursor: pointer;
}

.save-button:hover {
  background: #1f6044;
}

@media (max-width: 600px) {
  .section-label {
    align-items: flex-start;
    flex-direction: column;
  }

  .calendar-grid button {
    min-height: 30px;
  }
}
</style>