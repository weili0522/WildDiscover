<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref
} from 'vue'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const props = defineProps({
  species: {
    type: Array,
    required: true
  },

  modelValue: {
    type: String,
    default: null
  }
})

const emit = defineEmits([
  'update:modelValue',
  'select'
])

const selectorRoot = ref(null)
const isOpen = ref(false)

const imageMap = {
  'night-parrot': nightParrotImage,
  'princess-parrot': princessParrotImage,
  'plains-wanderer': plainsWandererImage,
  'rufous-scrub-bird': rufousScrubBirdImage,
  malleefowl: malleefowlImage,
  'dusky-grasswren': duskyGrasswrenImage
}

const statusMap = {
  'night-parrot': 'CR',
  'plains-wanderer': 'CR',
  'princess-parrot': 'VU',
  'rufous-scrub-bird': 'EN',
  malleefowl: 'VU',
  'dusky-grasswren': 'LC'
}

const selectedSpecies = computed(() =>
  props.species.find(
    item => item.id === props.modelValue
  )
)

function getImage(speciesId) {
  return imageMap[speciesId] || nightParrotImage
}

function getStatus(speciesId) {
  return statusMap[speciesId] || ''
}

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function selectSpecies(item) {
  emit('update:modelValue', item.id)
  emit('select', item)

  isOpen.value = false
}

function handleOutsideClick(event) {
  if (
    selectorRoot.value &&
    !selectorRoot.value.contains(event.target)
  ) {
    isOpen.value = false
  }
}

function handleEscape(event) {
  if (event.key === 'Escape') {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleEscape)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleEscape)
})
</script>

<template>
  <div
    ref="selectorRoot"
    class="species-selector"
  >
    <p class="selector-label">
      TARGET SPECIES
    </p>

    <button
      class="selector-trigger"
      :class="{ open: isOpen }"
      type="button"
      :aria-expanded="isOpen"
      aria-haspopup="listbox"
      @click="toggleDropdown"
    >
      <!-- Selected species -->
      <template v-if="selectedSpecies">
        <img
          :src="getImage(selectedSpecies.id)"
          :alt="selectedSpecies.commonName"
          class="selected-image"
        />

        <span class="selected-content">
          <span class="selected-name-row">
            <strong>
              {{ selectedSpecies.commonName }}
            </strong>

            <span
              v-if="getStatus(selectedSpecies.id)"
              class="status-code"
              :class="
                `status-${getStatus(selectedSpecies.id).toLowerCase()}`
              "
            >
              {{ getStatus(selectedSpecies.id) }}
            </span>
          </span>

          <em>
            {{ selectedSpecies.scientificName }}
          </em>
        </span>
      </template>

      <!-- No species selected -->
      <template v-else>
        <span class="placeholder-icon">
          Bird
        </span>

        <span class="placeholder-content">
          <strong>
            Choose a bird species...
          </strong>

          <small>
            {{ species.length }} native species catalogued
          </small>
        </span>
      </template>

      <span
        class="chevron"
        :class="{ open: isOpen }"
        aria-hidden="true"
      >
       ⌄
      </span>
    </button>

    <!-- Species dropdown -->
    <div
      v-if="isOpen"
      class="species-dropdown"
      role="listbox"
      aria-label="Choose a bird species"
    >
      <button
        v-for="item in species"
        :key="item.id"
        class="species-option"
        :class="{
          selected: item.id === modelValue
        }"
        type="button"
        role="option"
        :aria-selected="item.id === modelValue"
        @click="selectSpecies(item)"
      >
        <img
          :src="getImage(item.id)"
          :alt="item.commonName"
          class="option-image"
        />

        <span class="option-content">
          <span class="option-name-row">
            <strong>
              {{ item.commonName }}
            </strong>

            <span
              v-if="getStatus(item.id)"
              class="status-code"
              :class="
                `status-${getStatus(item.id).toLowerCase()}`
              "
            >
              {{ getStatus(item.id) }}
            </span>
          </span>

          <em>
            {{ item.scientificName }}
          </em>

          <small>
            Habitat:
            {{ item.habitat || 'Australian native habitat' }}
          </small>
        </span>

        <span
          class="option-arrow"
          aria-hidden="true"
        >
          ›
        </span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.species-selector {
  position: relative;
  z-index: 1000;
  width: min(460px, 100%);
}

.selector-label {
  margin: 0 0 7px;
  color: #52675c;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.selector-trigger {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) auto;
  align-items: center;
  width: 100%;
  min-height: 66px;
  padding: 7px 13px 7px 7px;
  border: 1px solid #d4ddd8;
  border-radius: 10px;
  background: #ffffff;
  color: #2b4137;
  text-align: left;
  cursor: pointer;
  box-shadow: 0 2px 6px rgb(24 63 46 / 5%);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.selector-trigger:hover,
.selector-trigger.open {
  border-color: #65b990;
  box-shadow: 0 0 0 3px rgb(77 177 127 / 10%);
}

.selected-image,
.option-image {
  width: 42px;
  height: 42px;
  border-radius: 6px;
  object-fit: cover;
}

.selected-content,
.placeholder-content,
.option-content {
  display: grid;
  min-width: 0;
  gap: 2px;
  padding-left: 10px;
}

.selected-name-row,
.option-name-row {
  display: flex;
  align-items: center;
  gap: 7px;
}

.selected-content strong,
.placeholder-content strong,
.option-content strong {
  color: #2c4137;
  font-size: 13px;
}

.selected-content em,
.option-content em {
  overflow: hidden;
  color: #76837c;
  font-family: Georgia, serif;
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.placeholder-icon {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 6px;
  background: #f0f2ef;
  color: #65736c;
  font-size: 11px;
}

.placeholder-content small,
.option-content small {
  color: #849089;
  font-size: 9px;
}

.chevron {
  color: #52665c;
  font-size: 21px;
  transition: transform 0.2s ease;
}

.chevron.open {
  transform: rotate(180deg);
}

.species-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  left: 0;
  display: grid;
  overflow: hidden;
  padding: 0;
  border: 1px solid #d9e1dc;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 14px 32px rgb(25 63 47 / 16%);
}

.species-option {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  align-items: center;
  width: 100%;
  min-height: 67px;
  padding: 8px;
  border: 0;
  border-bottom: 1px solid #edf0ee;
  background: #ffffff;
  color: #2d4539;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.species-option:last-child {
  border-bottom: 0;
}

.species-option:hover,
.species-option.selected {
  background: #eef8f2;
}

.option-arrow {
  padding-right: 7px;
  color: #779087;
  font-size: 18px;
}

.status-code {
  padding: 2px 5px;
  border-radius: 4px;
  font-size: 8px;
  font-style: normal;
  font-weight: 900;
}

.status-cr {
  background: #ffe2e2;
  color: #cb4d4d;
}

.status-en {
  background: #eceeed;
  color: #53635b;
}

.status-vu {
  background: #e5eee9;
  color: #5b7166;
}

.status-lc {
  background: #e7f4eb;
  color: #43805f;
}

@media (max-width: 600px) {
  .species-selector {
    width: 100%;
  }
}
</style>