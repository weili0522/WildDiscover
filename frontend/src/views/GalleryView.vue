<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import SpeciesCard from '../components/SpeciesCard.vue'
import SpeciesModal from '../components/SpeciesModal.vue'

import {
  conservationFilters,
  gallerySpecies
} from '../mocks/gallery'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const router = useRouter()

const searchTerm = ref('')
const selectedFilter = ref('all')
const selectedSpecies = ref(null)
const activeAudioId = ref(null)

const imageMap = {
  'night-parrot.jpg': nightParrotImage,
  'princess-parrot.jpg': princessParrotImage,
  'plains-wanderer.jpg': plainsWandererImage,
  'rufous-scrub-bird.jpg': rufousScrubBirdImage,
  'malleefowl.jpg': malleefowlImage,
  'dusky-grasswren.jpg': duskyGrasswrenImage
}

const speciesWithImages = computed(() =>
  gallerySpecies.map((species) => ({
    ...species,
    image: imageMap[species.image]
  }))
)

const filteredSpecies = computed(() => {
  const normalizedSearch = searchTerm.value
    .trim()
    .toLowerCase()

  return speciesWithImages.value.filter((species) => {
    const matchesSearch =
      !normalizedSearch ||
      species.name.toLowerCase().includes(normalizedSearch) ||
      species.scientificName
        .toLowerCase()
        .includes(normalizedSearch)

    const matchesFilter =
      selectedFilter.value === 'all' ||
      species.statusClass === selectedFilter.value

    return matchesSearch && matchesFilter
  })
})

function viewDetails(species) {
  selectedSpecies.value = species
}

function viewOnMap(species) {
  router.push({
    path: '/map',
    query: {
      species: species.id
    }
  })
}

function listenToCall(species) {
  activeAudioId.value =
    activeAudioId.value === species.id
      ? null
      : species.id

  console.log('Mock bird call selected:', species.name)
}
</script>

<template>
  <div class="gallery-page">
    <div class="gallery-container">
      <section class="gallery-header">
        <div>
          <span class="heading-badge">
            ● Field Catalogue
          </span>

          <h1>Bird Gallery</h1>

          <p>
            Discover Australian birds, learn about their habitats,
            and listen to their calls in pristine native soundscapes.
          </p>
        </div>

        <div class="header-actions">
          <label class="search-box">
            <span>⌕</span>

            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search birds..."
              aria-label="Search birds"
            >
          </label>
        </div>
      </section>

      <section class="challenge-banner">
        <div class="challenge-icon">
          ♬
        </div>

        <div>
          <div class="challenge-title">
            <h2>Bird Call Challenge</h2>
            <span>Interactive</span>
          </div>

          <p>
            Can you recognise a bird by its call? Test your ears,
            sharpen field skills, and earn community explorer points.
          </p>
        </div>

        <button
          type="button"
          @click="router.push('/gallery/challenge')"
        >
          Try the Challenge →
        </button>
      </section>

      <section class="filter-row">
        <button
          v-for="filter in conservationFilters"
          :key="filter.id"
          class="filter-button"
          :class="{ active: selectedFilter === filter.id }"
          type="button"
          @click="selectedFilter = filter.id"
        >
          {{ filter.label }}
          <span>{{ filter.count }}</span>
        </button>
      </section>

      <section class="species-grid">
        <SpeciesCard
          v-for="species in filteredSpecies"
          :key="species.id"
          :species="species"
          @view-details="viewDetails"
          @view-map="viewOnMap"
          @listen="listenToCall"
        />
      </section>

      <p
        v-if="filteredSpecies.length === 0"
        class="empty-message"
      >
        No birds match your current search.
      </p>
    </div>

    <SpeciesModal
      :visible="Boolean(selectedSpecies)"
      :species="selectedSpecies"
      @close="selectedSpecies = null"
      @view-map="viewOnMap"
      @listen="listenToCall"
    />
  </div>
</template>

<style scoped>
.gallery-page {
  min-height: 100vh;
  padding: 42px 24px 80px;
  background: #f8faf8;
}

.gallery-container {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
}

.gallery-header {
  display: flex;
  margin-bottom: 24px;
  align-items: flex-end;
  justify-content: space-between;
  gap: 25px;
}

.heading-badge {
  display: inline-block;
  margin-bottom: 8px;
  color: #2e805d;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}

.gallery-header h1 {
  margin: 0 0 6px;
  color: #174b35;
  font-size: 34px;
  font-weight: 700;
}

.gallery-header p {
  max-width: 650px;
  margin: 0;
  color: #68756e;
  font-size: 12px;
  line-height: 1.5;
}

.header-actions {
  display: flex;
  width: 320px;
  flex-direction: column;
  gap: 10px;
}

.search-box {
  display: flex;
  padding: 0 11px;
  align-items: center;
  gap: 7px;
  background: #ffffff;
  border: 1px solid #dfe6e1;
  border-radius: 18px;
}

.search-box span {
  color: #7d8782;
}

.search-box input {
  width: 100%;
  padding: 9px 0;
  font-size: 10px;
  outline: none;
  background: transparent;
  border: 0;
}

.challenge-banner {
  display: grid;
  grid-template-columns: 42px 1fr auto;
  margin-bottom: 23px;
  padding: 22px;
  color: #ffffff;
  align-items: center;
  gap: 14px;
  background:
    radial-gradient(
      circle at 80% 50%,
      rgba(100, 198, 148, 0.3),
      transparent 30%
    ),
    #176045;
  border-radius: 10px;
}

.challenge-icon {
  display: grid;
  width: 40px;
  height: 40px;
  color: #226c4e;
  font-size: 18px;
  place-items: center;
  background: #b9f0d1;
  border-radius: 50%;
}

.challenge-title {
  display: flex;
  align-items: center;
  gap: 9px;
}

.challenge-title h2 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
}

.challenge-title span {
  padding: 4px 7px;
  color: #c9f4dd;
  font-size: 7px;
  font-weight: 700;
  text-transform: uppercase;
  border: 1px solid rgba(201, 244, 221, 0.45);
  border-radius: 9px;
}

.challenge-banner p {
  max-width: 620px;
  margin: 5px 0 0;
  color: #dcebe4;
  font-size: 9px;
  line-height: 1.45;
}

.challenge-banner > button {
  padding: 10px 15px;
  color: #226247;
  font-size: 9px;
  font-weight: 700;
  background: #c9f4dd;
  border: 0;
  border-radius: 17px;
  cursor: pointer;
}

.filter-row {
  display: flex;
  margin-bottom: 19px;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-button {
  padding: 7px 11px;
  color: #66736c;
  font-size: 9px;
  font-weight: 600;
  background: transparent;
  border: 0;
  border-radius: 14px;
  cursor: pointer;
}

.filter-button span {
  margin-left: 4px;
  padding: 2px 5px;
  background: #e5eee9;
  border-radius: 8px;
}

.filter-button.active {
  color: #ffffff;
  background: #2d7a58;
}

.filter-button.active span {
  background: rgba(255, 255, 255, 0.18);
}

.species-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.empty-message {
  padding: 60px 20px;
  color: #77837d;
  text-align: center;
}

@media (max-width: 800px) {
  .gallery-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .challenge-banner {
    grid-template-columns: 42px 1fr;
  }

  .challenge-banner > button {
    grid-column: 1 / -1;
  }
}

@media (max-width: 620px) {
  .gallery-page {
    padding: 30px 14px 55px;
  }

  .species-grid {
    grid-template-columns: 1fr;
  }
}
</style>