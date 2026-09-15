<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import {
  investigations,
  journalStatuses,
  journalSummary
} from '../mocks/journal'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const selectedStatus = ref('All Statuses')
const router = useRouter()

const speciesImages = {
  'night-parrot.jpg': nightParrotImage,
  'princess-parrot.jpg': princessParrotImage,
  'plains-wanderer.jpg': plainsWandererImage,
  'rufous-scrub-bird.jpg': rufousScrubBirdImage,
  'malleefowl.jpg': malleefowlImage,
  'dusky-grasswren.jpg': duskyGrasswrenImage
}

const filteredInvestigations = computed(() => {
  if (selectedStatus.value === 'All Statuses') {
    return investigations
  }

  return investigations.filter(
    (investigation) =>
      investigation.status === selectedStatus.value
  )
})

function getImage(imageName) {
  return speciesImages[imageName]
}

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

        <article class="summary-card">
          <div>
            <span>Evidence Submitted</span>
            <strong>{{ journalSummary.evidenceSubmitted }}</strong>
            <small>Field audio, photos &amp; habitat logs</small>
          </div>

          <div class="summary-icon">▣</div>
        </article>
      </section>

      <!-- Filter -->
      <section class="journal-toolbar">
        <span>
          All Investigations ({{ investigations.length }})
        </span>

        <label>
          Filter by Status:

          <select v-model="selectedStatus">
            <option
              v-for="status in journalStatuses"
              :key="status"
              :value="status"
            >
              {{ status }}
            </option>
          </select>
        </label>
      </section>

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
                 url(${getImage(investigation.image)})`
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
            <div
              class="status-label"
              :class="{
                completed: investigation.status === 'Completed',
                progress: investigation.status === 'In Progress'
              }"
            >
              <span>◉ Latest Exploration</span>
              <b>{{ investigation.status }}</b>
              <small>{{ investigation.latestExploration }}</small>
            </div>

            <div class="metrics-grid">
              <div>
                <span>Zones Explored</span>
                <strong>{{ investigation.zonesExplored }}</strong>
              </div>

              <div>
                <span>Evidence Submitted</span>
                <strong>{{ investigation.evidenceSubmitted }}</strong>
              </div>

              <div>
                <span>Saved Boundary</span>
                <strong>{{ investigation.savedBoundary }}</strong>
              </div>
            </div>

            <div class="saved-area">
              <div>
                <span>⌖ Saved Exploration Area</span>
                <strong>{{ investigation.savedArea }}</strong>
              </div>

              <b>
                ↑ {{ investigation.probability }}%
                {{ investigation.probabilityLevel }}
              </b>
            </div>

            <!-- Completed investigation -->
            <RouterLink
              v-if="investigation.status === 'Completed'"
              :to="`/journal/${investigation.id}/summary`"
              class="investigation-button"
            >
              {{ investigation.actionLabel }}
              <span>→</span>
            </RouterLink>

            <!-- Active investigation -->
            <RouterLink
              v-else-if="investigation.status === 'In Progress'"
              :to="`/journal/${investigation.id}`"
              class="investigation-button"
            >
              {{ investigation.actionLabel }}
              <span>→</span>
            </RouterLink>

            <!-- Not-started investigation -->
           <button
            v-else
            class="investigation-button"
            type="button"
            @click="startExploration(investigation)"
          >
            {{ investigation.actionLabel }}
            <span>→</span>
          </button>

          </div>
        </article>
      </section>

      <RouterLink to="/map" class="map-dashboard-link">
        Open Map Dashboard →
      </RouterLink>
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
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  background: #d5f1e2;
  border-radius: 12px;
}

.journal-heading h1 {
  margin: 0 0 7px;
  color: #193e2d;
  font-size: 35px;
  font-weight: 700;
}

.journal-heading p {
  margin: 0;
  color: #68756e;
  font-size: 13px;
}

.heading-actions {
  display: flex;
  gap: 10px;
}

.primary-button,
.secondary-button {
  padding: 10px 16px;
  font-size: 11px;
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
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}

.summary-card strong {
  margin-bottom: 6px;
  color: #246747;
  font-size: 28px;
}

.summary-card small {
  color: #707c75;
  font-size: 9px;
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
  font-size: 10px;
  font-weight: 700;
  background: #2d7a58;
  border-radius: 15px;
}

.journal-toolbar label {
  color: #66736c;
  font-size: 10px;
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
  font-size: 8px;
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
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
}

.species-title h2 {
  margin: 5px 0 1px;
  font-size: 26px;
  font-weight: 700;
}

.species-title em {
  font-family: Georgia, serif;
  font-size: 11px;
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
  font-size: 9px;
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
  font-size: 8px;
}

.metrics-grid strong {
  font-size: 15px;
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
  font-size: 8px;
}

.saved-area strong {
  margin-top: 3px;
  font-size: 10px;
}

.saved-area > b {
  padding: 5px 8px;
  color: #246d4d;
  font-size: 8px;
  background: #d6f1e2;
  border-radius: 11px;
}

.investigation-button {
  display: flex;
  width: 100%;
  margin-top: auto;
  padding: 10px 15px;
  color: #ffffff;
  font-size: 10px;
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
  font-size: 10px;
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
</style>