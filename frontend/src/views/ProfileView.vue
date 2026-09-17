<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExplorer } from '../composables/useExplorer'
import { gallerySpecies } from '../mocks/gallery'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const imageMap = {
  'night-parrot.jpg': nightParrotImage,
  'princess-parrot.jpg': princessParrotImage,
  'plains-wanderer.jpg': plainsWandererImage,
  'rufous-scrub-bird.jpg': rufousScrubBirdImage,
  'malleefowl.jpg': malleefowlImage,
  'dusky-grasswren.jpg': duskyGrasswrenImage
}

const router = useRouter()
const { explorer, hasExplorerSession } = useExplorer()

const profileData = ref({
  points: 0,
  rank: 0,
  total_users: 1,
  investigations: []
})

const displayName = computed(() => explorer.value?.displayName || 'Guest')
const explorerId = computed(() => explorer.value?.id?.toUpperCase() || 'EXP-GUEST')

const LEVELS = [
  { name: 'Novice Observer', threshold: 0 },
  { name: 'Field Enthusiast', threshold: 100 },
  { name: 'Conservation Scout', threshold: 300 },
  { name: 'Species Tracker', threshold: 600 },
  { name: 'Master Ecologist', threshold: 1000 }
]

const currentLevelIndex = computed(() => {
  const pts = profileData.value.points
  let idx = 0
  for (let i = 0; i < LEVELS.length; i++) {
    if (pts >= LEVELS[i].threshold) idx = i
  }
  return idx
})

const currentLevel = computed(() => LEVELS[currentLevelIndex.value])
const nextLevel = computed(() => {
  return currentLevelIndex.value < LEVELS.length - 1 
    ? LEVELS[currentLevelIndex.value + 1] 
    : null
})

const levelProgress = computed(() => {
  if (!nextLevel.value) return 100
  const currentThreshold = currentLevel.value.threshold
  const nextThreshold = nextLevel.value.threshold
  const pointsIntoLevel = profileData.value.points - currentThreshold
  const pointsRequired = nextThreshold - currentThreshold
  return Math.min(Math.round((pointsIntoLevel / pointsRequired) * 100), 100)
})

const pointsRemaining = computed(() => {
  if (!nextLevel.value) return 0
  return Math.max(nextLevel.value.threshold - profileData.value.points, 0)
})

// Filter investigations to only show future ones
const futureInvestigations = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  return profileData.value.investigations
    .filter(inv => {
      const invDate = new Date(inv.exploration_date)
      return invDate >= today
    })
    .map(inv => {
      // Find species info
      const species = gallerySpecies.find(s => s.id === inv.species_id)
      return {
        ...inv,
        commonName: species ? species.name : 'Unknown Bird',
        scientificName: species ? species.scientificName : '',
        statusClass: species ? species.statusClass : 'Endangered',
        image: species ? imageMap[species.image] : nightParrotImage
      }
    })
})

const showTooltip = ref(false)

onMounted(async () => {
  if (!hasExplorerSession.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/profile/${explorer.value.displayName}`)
    if (res.ok) {
      profileData.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to fetch profile', e)
  }
})
</script>

<template>
  <main class="profile-page">
    <div class="profile-container">
      <header class="profile-heading">
        <div>
          <p class="eyebrow">▣ CITIZEN SCIENCE · EXPLORER DASHBOARD</p>

          <h1>My Explorer Profile</h1>

          <p class="description">
            Track your personal contributions, rank in the community, and
            active field investigations across Australia.
          </p>
        </div>

        <div class="heading-actions">
          <button
            type="button"
            class="secondary-button"
            @click="router.push('/journal')"
          >
            ▣ View My Journal
          </button>

          <button
            type="button"
            class="primary-button"
            @click="router.push('/map')"
          >
            ◉ Explore More on Map
          </button>
        </div>
      </header>

      <section class="identity-card">
        <div class="avatar">
          <span class="avatar-symbol">♧</span>
          <span class="avatar-level">3</span>
        </div>

        <div class="identity-name">
          <h2>{{ displayName }}</h2>

          <span v-if="!hasExplorerSession" class="mock-label">
            Mock profile
          </span>
        </div>

        <div class="identity-status">
          <span>CURRENT STATUS</span>
          <strong>
            <i></i>
            Active
          </strong>
          <small>ID {{ explorerId }}</small>
        </div>
      </section>

      <div class="dashboard-grid">
        <div class="main-column">
          <section class="dashboard-card level-card" style="position: relative;">
            <h2>
              ⌁ Level Progress
              <span class="tooltip-icon" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">i</span>
              <div class="levels-tooltip" v-if="showTooltip">
                <h4>Level Thresholds</h4>
                <ul>
                  <li v-for="(lvl, idx) in LEVELS" :key="lvl.name">
                    Lvl {{ idx + 1 }} ({{ lvl.name }}): {{ lvl.threshold }}+ pts
                  </li>
                </ul>
              </div>
            </h2>

            <div class="level-row">
              <div>
                <strong>{{ currentLevel.name }}</strong>
                <span>Level {{ currentLevelIndex + 1 }}</span>
              </div>

              <p v-if="nextLevel">
                Next:
                <strong>{{ nextLevel.name }}</strong>
                <span>Level {{ currentLevelIndex + 2 }}</span>
              </p>
              <p v-else>
                <strong>Max Level Reached!</strong>
              </p>
            </div>

            <div
              class="progress-track"
              role="progressbar"
            >
              <div
                class="progress-value"
                :style="{ width: `${levelProgress}%` }"
              ></div>
            </div>

            <div class="progress-details">
              <strong v-if="nextLevel">
                {{ profileData.points }} /
                {{ nextLevel.threshold }} points
                ({{ levelProgress }}%)
              </strong>
              <strong v-else>
                {{ profileData.points }} points (Max!)
              </strong>

              <span v-if="nextLevel">
                {{ pointsRemaining }} points needed to unlock {{ nextLevel.name }} badge.
              </span>
            </div>
          </section>

          <section class="activity-section">
            <h2 class="section-title">⌁ My Planned Trips</h2>

            <div v-if="futureInvestigations.length === 0" style="padding: 1rem; color: #5a7566">
              No planned trips found in the future. Check out the Map to plan a new one!
            </div>
            
            <article v-for="inv in futureInvestigations" :key="inv.id" class="dashboard-card investigation-card">
              <div class="investigation-heading">
                <h3>◎ Upcoming Investigation</h3>
                <span class="planned-badge">● Status: Planned</span>
              </div>

              <div class="investigation-content">
                <div class="bird-image-wrapper">
                  <img
                    :src="inv.image"
                    :alt="inv.commonName"
                  />
                  <em>{{ inv.scientificName }}</em>
                </div>

                <div class="investigation-info">
                  <div class="title-row">
                    <h2>{{ inv.commonName }}</h2>
                    <span class="conservation-badge" style="background-color: #ffcccc; color: #b30000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 1.04rem;">
                      {{ inv.statusClass }}
                    </span>
                  </div>

                  <div class="details-grid" style="margin-top: 1rem;">
                    <div>
                      <span>Target Zone:</span>
                      <strong>Zone #{{ inv.id }}</strong>
                    </div>

                    <div>
                      <span>Target Date:</span>
                      <strong>{{ inv.exploration_date }}</strong>
                    </div>
                  </div>

                  <p class="description">
                    Planned exploration to search for the {{ inv.commonName }}. Ensure environmental conditions and sensor arrays are ready for the field trip.
                  </p>

                  <div class="card-footer">
                    <RouterLink
                      to="/journal"
                      class="view-journal-link"
                    >
                      View My Journal →
                    </RouterLink>

                    <span class="log-number">Expedition Log #{{ inv.id }}</span>
                  </div>
                </div>
              </div>
            </article>
          </section>
        </div>

        <aside class="side-column">
          <section class="dashboard-card rank-card">
            <h2>♜ Community Rank</h2>

            <div class="rank-display">
              <span>NATIONAL POSITION</span>
              <strong>#{{ profileData.rank }}</strong>
              <p>
                Contribution Score:
                <b>{{ profileData.points }} pts</b>
              </p>
              <small>
                Top {{ Math.max(1, Math.round((profileData.rank / profileData.total_users) * 100)) }}% of Active Conservation Observers
              </small>
            </div>
          </section>

          <section class="dashboard-card contribution-card">
            <div class="contribution-heading">
              <h2>◎ Contribution Points</h2>
              <strong>{{ profileData.points }} pts</strong>
            </div>

            <p>
              Points are earned through verified scientific contributions and
              fieldwork.
            </p>

            <ul>
              <li>
                <span>◉ Complete an Exploration</span>
                <strong>+20 pts</strong>
              </li>

              <li>
                <span>▣ Add an Observation</span>
                <strong>+10 pts</strong>
              </li>

              <li>
                <span>♫ Complete Bird Call Challenge</span>
                <strong>+5 pts</strong>
              </li>
            </ul>
          </section>
        </aside>
      </div>
    </div>
  </main>
</template>

<style scoped>
.profile-page {
  min-height: calc(100vh - 80px);
  padding: 46px 24px 80px;
  background: #fbfcfa;
  color: #193f30;
}

.profile-container {
  width: min(1160px, 100%);
  margin: 0 auto;
}

.profile-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 30px;
  margin-bottom: 26px;
}

.eyebrow {
  display: inline-block;
  margin: 0 0 10px;
  padding: 6px 11px;
  border-radius: 18px;
  background: #d8f4e4;
  color: #277b57;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.profile-heading h1 {
  margin: 0 0 8px;
  color: #16412f;
  font-size: clamp(34px, 4vw, 48px);
  line-height: 1.05;
}

.description {
  max-width: 610px;
  margin: 0;
  color: #6d7973;
  line-height: 1.5;
}

.heading-actions {
  display: flex;
  gap: 10px;
}

.heading-actions button {
  padding: 11px 17px;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
}

.secondary-button {
  border: 1px solid #d8e1dc;
  background: white;
  color: #2b624a;
}

.primary-button {
  border: 0;
  background: #217852;
  color: white;
}

.identity-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  margin-bottom: 30px;
  padding: 24px;
  border: 1px solid #e0e7e3;
  border-radius: 14px;
  background: white;
}

.avatar {
  position: relative;
  display: grid;
  width: 74px;
  height: 74px;
  place-items: center;
  border: 7px solid #eee8da;
  border-radius: 50%;
  background: #d8e2db;
  color: #275b43;
}

.avatar-symbol {
  font-size: 34px;
}

.avatar-level {
  position: absolute;
  right: -4px;
  bottom: -4px;
  display: grid;
  width: 23px;
  height: 23px;
  place-items: center;
  border: 3px solid white;
  border-radius: 50%;
  background: #176a47;
  color: white;
  font-size: 12px;
  font-weight: 900;
}

.identity-name {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.identity-name h2 {
  margin: 0;
  color: #263e33;
  font-size: 31px;
}

.mock-label {
  padding: 5px 8px;
  border-radius: 12px;
  background: #f1f3f1;
  color: #78847e;
  font-size: 12px;
}

.identity-status {
  display: grid;
  justify-items: end;
  gap: 4px;
}

.identity-status > span {
  color: #78867f;
  font-size: 12px;
  font-weight: 800;
}

.identity-status strong {
  color: #315444;
  font-size: 16px;
}

.identity-status i {
  display: inline-block;
  width: 7px;
  height: 7px;
  margin-right: 5px;
  border-radius: 50%;
  background: #42bb82;
}

.identity-status small {
  padding: 4px 8px;
  border-radius: 12px;
  background: #f1f3f1;
  color: #7a857f;
  font-size: 12px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 310px;
  gap: 24px;
  align-items: start;
}

.main-column,
.side-column {
  display: grid;
  gap: 22px;
}

.dashboard-card {
  padding: 24px;
  border: 1px solid #e0e7e3;
  border-radius: 14px;
  background: white;
  box-shadow: 0 5px 18px rgb(31 77 56 / 4%);
}

.dashboard-card h2,
.section-title {
  margin: 0 0 20px;
  color: #294638;
  font-size: 22px;
}

.level-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.level-row > div strong {
  margin-right: 7px;
  font-size: 21px;
}

.level-row span {
  color: #78857e;
  font-size: 13px;
}

.level-row p {
  margin: 0;
  color: #67756e;
  font-size: 14px;
}

.level-row p strong {
  color: #25805a;
}

.progress-track {
  height: 9px;
  margin-top: 17px;
  overflow: hidden;
  border-radius: 20px;
  background: #dce6e0;
}

.progress-value {
  height: 100%;
  border-radius: inherit;
  background: #238059;
}

.progress-details {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-top: 9px;
  color: #68776f;
  font-size: 13px;
}

.progress-details strong {
  color: #2d7656;
}

.activity-section {
  margin-top: 3px;
}

.section-title {
  margin-bottom: 14px;
}

.investigation-card {
  padding: 0;
  overflow: hidden;
}

.investigation-heading {
  display: flex;
  justify-content: space-between;
  padding: 18px 20px;
  border-bottom: 1px solid #e3e8e5;
}

.investigation-heading h3 {
  margin: 0;
  font-size: 20px;
}

.planned-badge {
  padding: 5px 10px;
  border-radius: 15px;
  background: #eef3f0;
  color: #4d6d5c;
  font-size: 12px;
  font-weight: 700;
}

.investigation-content {
  display: grid;
  grid-template-columns: 245px minmax(0, 1fr);
  gap: 20px;
  padding: 20px;
}

.bird-image-wrapper {
  position: relative;
  overflow: hidden;
  min-height: 185px;
  border-radius: 10px;
}

.bird-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bird-image-wrapper span {
  position: absolute;
  right: 12px;
  bottom: 10px;
  left: 12px;
  color: white;
  font-family: Georgia, serif;
  font-size: 14px;
  font-style: italic;
}

.bird-title-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.bird-title-row h3 {
  margin: 0;
  font-size: 23px;
}

.bird-title-row p {
  margin: 4px 0 0;
  color: #68776f;
  font-size: 14px;
}

.endangered-badge {
  align-self: start;
  padding: 5px 9px;
  border-radius: 13px;
  background: #ffe5e5;
  color: #c95151;
  font-size: 12px;
  font-weight: 800;
}

.investigation-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin: 18px 0 12px;
}

.investigation-meta p {
  display: grid;
  gap: 3px;
  margin: 0;
  font-size: 13px;
}

.investigation-meta span {
  color: #849088;
}

.investigation-description {
  margin: 0;
  color: #66766e;
  font-size: 15px;
  line-height: 1.5;
}

.investigation-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.investigation-footer button {
  padding: 0;
  border: 0;
  background: transparent;
  color: #217752;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}

.investigation-footer span {
  color: #8a948f;
  font-size: 12px;
}

.rank-display {
  padding: 20px;
  border-radius: 10px;
  background: #f3f5f3;
  text-align: center;
}

.rank-display > span {
  color: #728078;
  font-size: 12px;
  font-weight: 800;
}

.rank-display > strong {
  display: block;
  margin: 8px 0;
  color: #126543;
  font-size: 48px;
}

.rank-display p {
  margin: 0;
  color: #66746d;
  font-size: 14px;
}

.rank-display small {
  display: block;
  margin-top: 8px;
  color: #27805a;
  font-size: 12px;
}

.contribution-heading {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.contribution-heading strong {
  color: #247854;
  font-size: 23px;
}

.contribution-card > p {
  color: #6b7972;
  font-size: 14px;
  line-height: 1.5;
}

.contribution-card ul {
  display: grid;
  gap: 8px;
  margin: 18px 0 0;
  padding: 0;
  list-style: none;
}

.contribution-card li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  background: #f3f6f4;
  color: #53675d;
  font-size: 13px;
}

.contribution-card li strong {
  color: #208157;
}

@media (max-width: 900px) {
  .profile-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 650px) {
  .profile-page {
    padding: 30px 15px 60px;
  }

  .heading-actions,
  .level-row,
  .progress-details {
    align-items: stretch;
    flex-direction: column;
  }

  .identity-card {
    grid-template-columns: auto 1fr;
  }

  .identity-status {
    grid-column: 1 / -1;
    justify-items: start;
  }

  .investigation-content {
    grid-template-columns: 1fr;
  }

  .bird-image-wrapper {
    height: 220px;
  }

  .investigation-meta {
    grid-template-columns: 1fr;
  }
}
</style>
<style scoped>
.tooltip-icon {
  display: inline-block;
  margin-left: 8px;
  background-color: #2b7a54;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 15px;
  line-height: 1.5;
  text-align: center;
  cursor: pointer;
  font-weight: bold;
}
.levels-tooltip {
  position: absolute;
  top: 40px;
  left: 20px;
  background-color: #1a231f;
  color: white;
  padding: 12px;
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  min-width: 250px;
}
.levels-tooltip h4 {
  margin: 0 0 8px 0;
  color: #a4ceb3;
  font-size: 1.17rem;
}
.levels-tooltip ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.levels-tooltip li {
  margin-bottom: 4px;
  font-size: 1.1rem;
  font-weight: normal;
}
</style>
