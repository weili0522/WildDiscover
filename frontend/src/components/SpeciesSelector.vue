<script setup>
import { computed } from 'vue'
import { targetSpecies } from '../mocks/mapOptions'

const props = defineProps({
  species: {
    type: Array,
    default: () => targetSpecies
  },
  selectedSpeciesId: {
    type: String,
    default: 'night-parrot'
  }
})

const emit = defineEmits(['select'])

const featuredSpecies = computed(() =>
  props.species.filter((item) => item.featured)
)

function selectSpecies(speciesId) {
  emit('select', speciesId)
}
</script>

<template>
  <section class="species-section">
    <div class="species-heading">
      <span>FEATURED NATIVE SPECIES</span>
      <small>Select one to activate prediction layers</small>
    </div>

    <div class="species-grid">
      <button
        v-for="item in featuredSpecies"
        :key="item.id"
        class="species-card"
        :class="{ selected: item.id === selectedSpeciesId }"
        type="button"
        @click="selectSpecies(item.id)"
      >
        <div class="species-details">
          <h3>{{ item.commonName }}</h3>

          <em>{{ item.scientificName }}</em>

          <p>
            <span class="location-icon">◎</span>
            {{ item.habitat }}
          </p>
        </div>

        <div class="species-action">
          <span>
            {{
              item.id === selectedSpeciesId
                ? 'Selected'
                : 'View Predicted Map'
            }}
          </span>

          <span>→</span>
        </div>
      </button>
    </div>
  </section>
</template>

<style scoped>
.species-section {
  width: 100%;
}

.species-heading {
  display: flex;
  margin-bottom: 12px;
  color: #44554d;
  align-items: center;
  justify-content: space-between;
}

.species-heading > span {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.species-heading small {
  color: #348263;
  font-size: 11px;
  font-weight: 600;
}

.species-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.species-card {
  display: flex;
  min-height: 154px;
  padding: 17px;
  color: inherit;
  text-align: left;
  flex-direction: column;
  justify-content: space-between;
  background: #ffffff;
  border: 1px solid #e2e8e4;
  border-radius: 11px;
  box-shadow: 0 2px 8px rgba(24, 63, 45, 0.04);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.species-card:hover {
  border-color: #74aa90;
  box-shadow: 0 6px 16px rgba(24, 63, 45, 0.1);
  transform: translateY(-2px);
}

.species-card.selected {
  background: #f4faf6;
  border: 2px solid #2d7a59;
}

.species-details h3 {
  margin: 0 0 4px;
  color: #263d32;
  font-size: 16px;
  font-weight: 700;
}

.species-details em {
  display: block;
  color: #68746e;
  font-family: Georgia, serif;
  font-size: 11px;
}

.species-details p {
  display: flex;
  margin: 12px 0 0;
  color: #506159;
  font-size: 11px;
  font-weight: 600;
  align-items: center;
  gap: 5px;
}

.location-icon {
  color: #2f8a62;
  font-weight: 700;
}

.species-action {
  display: flex;
  padding-top: 12px;
  color: #4e5d56;
  font-size: 11px;
  font-weight: 600;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #edf0ee;
}

.species-card.selected .species-action {
  color: #267254;
}

@media (max-width: 1000px) {
  .species-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .species-heading {
    align-items: flex-start;
    flex-direction: column;
    gap: 5px;
  }

  .species-grid {
    grid-template-columns: 1fr;
  }
}
</style>