<script setup>
import SightingCard from '../components/SightingCard.vue'

const sightings = [
  {
    location: 'Pilbara Region',
    title: 'Community Observation',
    date: '◷ 14 days ago',
    type: 'Acoustic Detection',
    image: new URL('../assets/sighting-pilbara.jpg', import.meta.url).href
  },
  {
    location: 'Western Queensland',
    title: 'Open-source Sighting Record',
    date: ' 2026',
    type: 'Visual Observation',
    image: new URL('../assets/sighting-queensland.jpg', import.meta.url).href
  },
  {
    location: 'Central Australia',
    title: 'Community Observation',
    date: ' 2025',
    type: 'Acoustic Detection',
    image: new URL('../assets/sighting-central.jpg', import.meta.url).href
  }
]
</script>

<template>
  <div class="sightings-page">

    <RouterLink
      to="/gallery"
      class="back-link"
    >
      ← Back to Species Gallery
    </RouterLink>

    <div class="page-header">
      <h1>Night Parrot Sightings</h1>

      <p>
        Explore open-source community sightings and observation records
        of the Night Parrot.
      </p>
    </div>

    <section class="sightings-grid">
      <SightingCard
        v-for="sighting in sightings"
        :key="sighting.location"
        :sighting="sighting"
      />
    </section>

  </div>
</template>

<style scoped>
.sightings-page {
  max-width: 1180px;

  margin: 0 auto;

  padding: 60px 36px 90px;
}

.back-link {
  display: inline-block;

  margin-bottom: 30px;

  color: #277654;

  font-size: 13px;
  font-weight: 500;

  text-decoration: none;
}

.back-link:hover {
  color: #146c4a;
}

.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  margin: 0 0 12px;

  color: #1f1f1f;

  font-size: 40px;
  font-weight: 700;
}

.page-header p {
  max-width: 620px;

  margin: 0;

  color: #666666;

  font-size: 14px;
  line-height: 1.6;
}

.sightings-grid {
  display: grid;

  grid-template-columns: repeat(3, minmax(0, 1fr));

  gap: 24px;
}

@media (max-width: 900px) {
  .sightings-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .sightings-page {
    padding: 40px 20px 60px;
  }

  .page-header h1 {
    font-size: 32px;
  }

  .sightings-grid {
    grid-template-columns: 1fr;
  }
}
</style>