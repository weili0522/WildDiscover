<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'


const selectedStatus = ref('All Statuses')
const router = useRouter()
import { useExplorer } from '../composables/useExplorer'
const { explorer, isGuest } = useExplorer()
const investigations = ref([])
const journalSummary = computed(() => ({
  activeInvestigations: investigations.value.length,
  savedZones: investigations.value.length
}))

onMounted(async () => {
  if (isGuest.value || !explorer.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/journal/${explorer.value.displayName}`)
    if (res.ok) {
      investigations.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
})

// Species mapping
const speciesLookup = {
  'night-parrot': {
    commonName: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    category: 'Critically Elusive',
    type: 'Priority Investigation',
    image: nightParrotImage
  },
  'princess-parrot': {
    commonName: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    category: 'Nomadic Desert Explorer',
    type: 'Arid Corridor Study',
    image: princessParrotImage
  },
  'plains-wanderer': {
    commonName: 'Plains-wanderer',
    scientificName: 'Pedionomus torquatus',
    category: 'Ground-dwelling Specialist',
    type: 'Grassland Survey',
    image: plainsWandererImage
  },
  'rufous-scrub-bird': {
    commonName: 'Rufous Scrub-bird',
    scientificName: 'Atrichornis rufescens',
    category: 'Gondwanan Relict',
    type: 'Rainforest Audit',
    image: rufousScrubBirdImage
  },
  'malleefowl': {
    commonName: 'Malleefowl',
    scientificName: 'Leipoa ocellata',
    category: 'Mound Builder',
    type: 'Scrubland Mapping',
    image: malleefowlImage
  },
  'dusky-grasswren': {
    commonName: 'Dusky Grasswren',
    scientificName: 'Amytornis purnelli',
    category: 'Rock-hopping Endemic',
    type: 'Range Assessment',
    image: duskyGrasswrenImage
  }
}



const filteredInvestigations = computed(() => {
  // Group by species
  const grouped = {}
  investigations.value.forEach(inv => {
    if (!grouped[inv.species_id]) {
      grouped[inv.species_id] = []
    }
    grouped[inv.species_id].push(inv)
  })

  // Create an array of grouped investigations
  const groupedArray = []
  for (const [species_id, invs] of Object.entries(grouped)) {
    // Sort by id descending (latest first)
    invs.sort((a, b) => b.id - a.id)
    
    const info = speciesLookup[species_id] || speciesLookup['night-parrot']
    const latestInv = invs[0]
    
    groupedArray.push({
      ...info,
      id: species_id,
      number: latestInv.id, // For the # number top right
      latestExploration: new Date(latestInv.exploration_date).toLocaleDateString(),
      zonesExplored: invs.length,
      journeys: invs.map(i => ({
        id: i.id,
        label: `Zone #${i.id} - ${new Date(i.exploration_date).toLocaleDateString()}`
      }))
    })
  }

  // Sort groups by the latest journey id
  return groupedArray.sort((a, b) => b.number - a.number)
})


function startExploration(investigation) {
  router.push({
    path: '/map',
    query: {
      species: investigation.speciesId
    }
  })
}
</script>

<template>
  <div class="journal-page">
    
    <div class="journal-container">
      <!-- Guest lock -->
      <div v-if="isGuest" class="empty-state">
        <div class="empty-icon">🔒</div>
        <h2>Journal Locked</h2>
        <p>You are browsing as a guest. Please log in or create an account to start saving your explorations.</p>
        <RouterLink to="/onboarding" class="start-exploration">Create Account</RouterLink>
      </div>

      <template v-else>

      <!-- Heading -->
      <section class="journal-heading">
        <div>
          <span class="heading-badge">
            ▤ Field Notebook • Citizen Science
          </span>

          <h1>My Investigation Journal</h1>

          <p>
            Track the birds you are investigating, your saved areas,
            and your progress.
          </p>
        </div>

        <div class="heading-actions">
          <RouterLink to="/map" class="primary-button">
            + New Investigation
          </RouterLink>

          <RouterLink to="/gallery" class="secondary-button">
            ◉ Go to Gallery
          </RouterLink>
        </div>
      </section>

      <!-- Summary -->
      <section class="summary-grid">
        <article class="summary-card">
          <div>
            <span>Active Investigations</span>
            <strong>{{ journalSummary.activeInvestigations }}</strong>
            <small>Species actively monitored</small>
          </div>

          <div class="summary-icon">⌕</div>
        </article>

        <article class="summary-card">
          <div>
            <span>Saved Zones</span>
            <strong>{{ journalSummary.savedZones }}</strong>
            <small>Demarcated exploration sectors</small>
          </div>

          <div class="summary-icon">⌁</div>
        </article>

        
      </section>

      <!-- Filter -->
        <section class="journal-toolbar"><span>All Investigations ({{ investigations.length }})</span></section>

      <!-- Investigations -->
      <section class="investigation-list">
        <article
          v-for="investigation in filteredInvestigations"
          :key="investigation.id"
          class="investigation-card"
        >
          <div
            class="species-image"
            :style="{
              backgroundImage:
                `linear-gradient(to top, rgba(5, 22, 14, 0.8), transparent 58%),
                 url(${investigation.image})`
            }"
          >
            <span class="category-label">
              {{ investigation.category }}
            </span>

            <span class="record-number">
              #{{ investigation.number }}
            </span>

            <div class="species-title">
              <small>{{ investigation.type }}</small>
              <h2>{{ investigation.commonName }}</h2>
              <em>{{ investigation.scientificName }}</em>
            </div>
          </div>

          <div class="investigation-details">
            <div class="status-label">
              <span>◉ Latest Exploration</span>
              <small>{{ investigation.latestExploration }}</small>
            </div>

            <div class="metrics-grid">
              <div>
                <span>Zones Explored</span>
                <strong>{{ investigation.zonesExplored }}</strong>
              </div>

              <div>
                <span>Logged Journeys</span>
                <select class="journey-dropdown">
                  <option v-for="journey in investigation.journeys" :key="journey.id" :value="journey.id">
                    {{ journey.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="saved-area">
              <div>
                <span>⌖ Saved Exploration Area</span>
                <strong>Zone #{{ investigation.number }}</strong>
              </div>

              <b style="opacity: 0.5;">
                ↑ %
              </b>
            </div>

            <button
              class="investigation-button"
              type="button"
              @click="startExploration(investigation)"
            >
              Continue Investigation
              <span>→</span>
            </button>
          </div>
        </article>
      </section>

      <RouterLink to="/map" class="map-dashboard-link">
        Open Map Dashboard →
      </RouterLink>
      </template>
    </div>
  </div>
</template>

<style scoped>
.journal-page {
  min-height: 100vh;
  padding: 44px 24px 80px;
  color: #293e34;
  background: #f8faf8;
}

.journal-container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.journal-heading {
  display: flex;
  margin-bottom: 30px;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.heading-badge {
  display: inline-block;
  margin-bottom: 10px;
  padding: 5px 9px;
  color: #277553;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  background: #d5f1e2;
  border-radius: 12px;
}

.journal-heading h1 {
  margin: 0 0 7px;
  color: #193e2d;
  font-size: 38px;
  font-weight: 700;
}

.journal-heading p {
  margin: 0;
  color: #68756e;
  font-size: 16px;
}

.heading-actions {
  display: flex;
  gap: 10px;
}

.primary-button,
.secondary-button {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  border-radius: 19px;
}

.primary-button {
  color: #ffffff;
  background: #2d7a58;
}

.secondary-button {
  color: #526159;
  background: #ffffff;
  border: 1px solid #d8e0db;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin-bottom: 26px;
  gap: 16px;
}

.summary-card {
  display: flex;
  padding: 22px;
  justify-content: space-between;
  background: #ffffff;
  border: 1px solid #e1e7e3;
  border-radius: 10px;
}

.summary-card span,
.summary-card strong,
.summary-card small {
  display: block;
}

.summary-card span {
  margin-bottom: 9px;
  color: #68756e;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.summary-card strong {
  margin-bottom: 6px;
  color: #246747;
  font-size: 31px;
}

.summary-card small {
  color: #707c75;
  font-size: 12px;
}

.summary-icon {
  display: grid;
  width: 32px;
  height: 32px;
  color: #247653;
  place-items: center;
  background: #d8f3e5;
  border-radius: 7px;
}

.journal-toolbar {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
  justify-content: space-between;
}

.journal-toolbar > span {
  padding: 7px 13px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  background: #2d7a58;
  border-radius: 15px;
}

.journal-toolbar label {
  color: #66736c;
  font-size: 13px;
}

.journal-toolbar select {
  margin-left: 8px;
  padding: 7px 28px 7px 10px;
  color: #536158;
  background: #ffffff;
  border: 1px solid #dce3df;
  border-radius: 15px;
}

.investigation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.investigation-card {
  display: grid;
  grid-template-columns: minmax(280px, 0.8fr) minmax(0, 1.4fr);
  min-height: 280px;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #e0e6e2;
  border-radius: 12px;
}

.species-image {
  position: relative;
  min-height: 280px;
  padding: 18px;
  color: #ffffff;
  background-position: center;
  background-size: cover;
}

.category-label,
.record-number {
  position: absolute;
  top: 16px;
  font-size: 11px;
  font-weight: 700;
}

.category-label {
  left: 16px;
  padding: 4px 7px;
  color: #286d4e;
  background: #e5f4eb;
  border-radius: 10px;
}

.record-number {
  right: 16px;
}

.species-title {
  position: absolute;
  right: 18px;
  bottom: 18px;
  left: 18px;
}

.species-title small {
  color: #b9dbc9;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.species-title h2 {
  margin: 5px 0 1px;
  font-size: 29px;
  font-weight: 700;
}

.species-title em {
  font-family: Georgia, serif;
  font-size: 14px;
}

.investigation-details {
  display: flex;
  padding: 20px;
  flex-direction: column;
  gap: 14px;
}

.status-label {
  display: flex;
  width: fit-content;
  padding: 7px 11px;
  color: #66726b;
  font-size: 12px;
  align-items: center;
  gap: 8px;
  background: #eef1ef;
  border-radius: 15px;
}

.status-label.completed,
.status-label.progress {
  color: #267653;
  background: #d7f3e4;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.metrics-grid div {
  padding: 12px;
  background: #f3f5f3;
  border-radius: 7px;
}

.metrics-grid span,
.metrics-grid strong {
  display: block;
}

.metrics-grid span {
  margin-bottom: 5px;
  color: #707b75;
  font-size: 11px;
}

.metrics-grid strong {
  font-size: 18px;
}

.saved-area {
  display: flex;
  padding: 11px 13px;
  align-items: center;
  justify-content: space-between;
  background: #f5f7f5;
  border-radius: 7px;
}

.saved-area span,
.saved-area strong {
  display: block;
}

.saved-area span {
  color: #718078;
  font-size: 11px;
}

.saved-area strong {
  margin-top: 3px;
  font-size: 13px;
}

.saved-area > b {
  padding: 5px 8px;
  color: #246d4d;
  font-size: 11px;
  background: #d6f1e2;
  border-radius: 11px;
}

.investigation-button {
  display: flex;
  width: 100%;
  margin-top: auto;
  padding: 10px 15px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #2d7a58;
  border: 0;
  border-radius: 7px;
}

.map-dashboard-link {
  display: block;
  margin-top: 25px;
  padding: 14px;
  color: #267251;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  background: #eef2ef;
  border-radius: 7px;
}

@media (max-width: 800px) {
  .journal-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .investigation-card {
    grid-template-columns: 1fr;
  }

  .journal-toolbar {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 520px) {
  .journal-page {
    padding: 30px 14px 55px;
  }

  .heading-actions {
    width: 100%;
    flex-direction: column;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .saved-area {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e3ebe6;
  margin-top: 40px;
}
.empty-icon {
  font-size: 51px;
  margin-bottom: 20px;
}
.empty-state h2 {
  color: #173d2d;
  margin-bottom: 12px;
}
.empty-state p {
  color: #6d7872;
  margin-bottom: 24px;
}

</style><style scoped>
.journey-dropdown {
  width: 100%;
  margin-top: 4px;
  padding: 6px;
  border-radius: 4px;
  border: 1px solid #d4ddd8;
  background-color: transparent;
  color: #1a231f;
  font-weight: 600;
  font-family: inherit;
  font-size: 18px;
  outline: none;
  appearance: auto;
  cursor: pointer;
}
.journey-dropdown:hover {
  border-color: #2b7a54;
}
</style>
