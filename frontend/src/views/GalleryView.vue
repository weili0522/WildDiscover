<script setup>
import { ref } from 'vue'
import SpeciesCard from '../components/SpeciesCard.vue'
import SpeciesModal from '../components/SpeciesModal.vue'

const selectedSpecies = ref(null)
const species = [
  {
    name: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    status: 'Critically Endangered',
    statusClass: 'critical',
    image: new URL('../assets/night-parrot.jpg', import.meta.url).href
  },
  {
    name: 'Plains-wanderer',
    scientificName: 'Pedionomus torquatus',
    status: 'Critically Endangered',
    statusClass: 'critical',
    image: new URL('../assets/plains-wanderer.jpg', import.meta.url).href
  },
  {
    name: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    status: 'Vulnerable',
    statusClass: 'vulnerable',
    image: new URL('../assets/princess-parrot.jpg', import.meta.url).href
  },
  {
    name: 'Dusky Grasswren',
    scientificName: 'Amytornis purnelli',
    status: 'Lesser Concern',
    statusClass: 'lesser',
    image: new URL('../assets/dusky-grasswren.jpg', import.meta.url).href
  },
  {
    name: 'Malleefowl',
    scientificName: 'Leipoa ocellata',
    status: 'Vulnerable',
    statusClass: 'vulnerable',
    image: new URL('../assets/malleefowl.jpg', import.meta.url).href
  },
  {
    name: 'Rufous Scrub-bird',
    scientificName: 'Atrichornis rufescens',
    status: 'Endangered',
    statusClass: 'endangered',
    image: new URL('../assets/rufous-scrub-bird.jpg', import.meta.url).href
  }
]
</script>

<template>
  <div class="gallery-page">

    <section class="gallery-header">
      <h1>Species Gallery</h1>

      <p>
        Explore key vulnerable and indicator species across Australia’s
        arid and semi-arid ecosystems. Click on any bird to view species
        details and recent habitat updates.
      </p>
    </section>

    <section class="species-grid">
      <SpeciesCard
        v-for="(bird, index) in species"
        :key="bird.name"
        :species="bird"
        :featured="index === 0"
        :class="{ featured: index === 0 }"
        @select="selectedSpecies = $event"
      />
    </section>

  </div>
  <SpeciesModal
    :visible="selectedSpecies?.name === 'Night Parrot'"
    @close="selectedSpecies = null"
  />
</template>

<style scoped>
.gallery-page {
  max-width: 1180px;
  margin: 0 auto;

  padding: 48px 36px 80px;
}


/* =========================
   Header
   ========================= */

.gallery-header {
  margin-bottom: 38px;
}

.gallery-header h1 {
  margin: 0 0 16px;

  color: #146c4a;

  font-size: 38px;
  font-weight: 700;
}

.gallery-header p {
  max-width: 720px;

  margin: 0;

  color: #555555;

  font-size: 14px;
  line-height: 1.6;
}


/* =========================
   Grid
   ========================= */

.species-grid {
  display: grid;

  grid-template-columns: repeat(3, minmax(0, 1fr));

  gap: 24px;
}


/* Night Parrot occupies 2 columns */
.species-grid > .featured {
  grid-column: span 2;
}


/* =========================
   Responsive
   ========================= */

@media (max-width: 900px) {
  .gallery-page {
    padding: 36px 24px 60px;
  }

  .species-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .species-card.featured {
    grid-column: span 2;
  }
}

@media (max-width: 600px) {
  .gallery-page {
    padding: 30px 18px 50px;
  }

  .gallery-header h1 {
    font-size: 30px;
  }

  .species-grid {
    grid-template-columns: 1fr;
  }

  .species-card.featured {
    grid-column: span 1;
  }

  .featured .species-image {
    height: 240px;
  }
}
</style>