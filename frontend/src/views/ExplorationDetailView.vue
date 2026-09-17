<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import HabitatMap from '../components/HabitatMap.vue'
import { explorationDetail } from '../mocks/journal'
import princessParrotImage from '../assets/princess-parrot.jpg'

const router = useRouter()

const selectedNotice = ref('heard-call')
const fieldNotes = ref('')
const saved = ref(false)
const showFinishModal = ref(false)

function saveObservation() {
  const observation = {
    investigationId: explorationDetail.investigationId,
    notice: selectedNotice.value,
    notes: fieldNotes.value,
    savedAt: new Date().toISOString()
  }

  localStorage.setItem(
    'wilddiscover_latest_observation',
    JSON.stringify(observation)
  )

  saved.value = true
}

function finishExploration() {
  showFinishModal.value = true
}

function continueExploring() {
  showFinishModal.value = false
}

function completeExploration() {
  const completedExploration = {
    investigationId: explorationDetail.investigationId,
    status: 'Completed',
    completedAt: new Date().toISOString(),
    fieldTime: explorationDetail.fieldTime,
    observationsLogged: explorationDetail.observationsLogged
  }

  localStorage.setItem(
    'wilddiscover_completed_exploration',
    JSON.stringify(completedExploration)
  )

  showFinishModal.value = false
  router.push('/journal')
}
</script>

<template>
  <div class="detail-page">
    <div class="detail-container">
      <!-- Heading -->
      <section class="detail-heading">
        <button
          class="back-button"
          type="button"
          @click="router.push('/journal')"
        >
          ← Back to Investigation Journal
        </button>

        <div class="title-row">
          <div>
            <p>
              {{ explorationDetail.sector }}
              &nbsp;/&nbsp;
              Active Session
            </p>

            <h1>{{ explorationDetail.title }}</h1>
          </div>

          <span class="session-status">
            ● {{ explorationDetail.sessionStatus }}
          </span>
        </div>
      </section>

      <section class="detail-layout">
        <!-- Left: map -->
        <div class="detail-map">
          <div class="map-summary">
            <div>
              <strong>
                Your Exploration Area:
                {{ explorationDetail.sector }}
              </strong>

              <small>
                {{ explorationDetail.location }} •
                {{ explorationDetail.coordinates }} •
                {{ explorationDetail.area }}
              </small>
            </div>

            <span>
              ↑ {{ explorationDetail.probability }}%
              {{ explorationDetail.probabilityLevel }}
            </span>
          </div>

          <div class="observation-count">
            ● {{ explorationDetail.observationsLogged }}
            observation logged
          </div>

          <HabitatMap
            key="detail-map"
            mode="detail"
          />
        </div>

        <!-- Right: observation controls -->
        <aside class="observation-sidebar">
          <!-- Species -->
          <section class="species-summary">
            <img
              :src="princessParrotImage"
              alt="Princess Parrot"
            >

            <div>
              <span>
                {{ explorationDetail.species.conservationStatus }}
              </span>

              <h2>
                {{ explorationDetail.species.commonName }}
              </h2>

              <em>
                {{ explorationDetail.species.scientificName }}
              </em>
            </div>

            <strong>
              {{ explorationDetail.probability }}%
              {{ explorationDetail.probabilityLevel }}
            </strong>
          </section>

          <!-- Field progress -->
          <section class="progress-card">
            <h2>▣ Field Progress</h2>

            <p>
              {{ explorationDetail.fieldTime }} •
              {{ explorationDetail.observationsLogged }}
              observation logged
            </p>

            <article
              v-for="observation in explorationDetail.observations"
              :key="observation.id"
              class="observation-record"
              :class="observation.type"
            >
              <div class="record-icon">
                {{ observation.type === 'audio' ? '♬' : '⌖' }}
              </div>

              <div>
                <strong>{{ observation.title }}</strong>
                <p>{{ observation.description }}</p>

                <a href="#" @click.prevent>
                  {{ observation.attachment }}
                </a>
              </div>

              <time>{{ observation.time }}</time>
            </article>
          </section>

          <!-- Add observation -->
          <section class="notice-card">
            <div class="card-heading">
              <h2>♧ What did you notice?</h2>
              <span>GPS Tagged</span>
            </div>

            <div class="notice-grid">
              <button
                v-for="option in explorationDetail.noticeOptions"
                :key="option.id"
                class="notice-option"
                :class="{ active: selectedNotice === option.id }"
                type="button"
                @click="selectedNotice = option.id"
              >
                <strong>{{ option.label }}</strong>
                <small>{{ option.description }}</small>
              </button>
            </div>

            <label for="field-notes">
              Field Notes &amp; Audio Description
            </label>

            <textarea
              id="field-notes"
              v-model="fieldNotes"
              rows="3"
              placeholder="Add a short field note… Describe sound, behavior, or vegetation context."
            ></textarea>

            <div class="attachment-actions">
              <button type="button">
                ▣ Add Photo
              </button>

              <button type="button">
                ▻ Add Video
              </button>
            </div>

            <button
              class="save-observation"
              type="button"
              @click="saveObservation"
            >
              {{
                saved
                  ? '✓ Observation Saved'
                  : '▣ Save Observation to Map'
              }}
            </button>
          </section>

          <!-- Finish -->
          <section class="finish-card">
            <h2>♧ Ready to wrap up field session?</h2>

            <p>
              You can continue adding observations above. Finishing will
              finalize your route and compile your exploration summary.
            </p>

            <button
              type="button"
              @click="finishExploration"
            >
              Finish Exploration →
            </button>
          </section>
        </aside>
      </section>
    </div>

    <!-- Finish confirmation modal -->
    <div
      v-if="showFinishModal"
      class="modal-overlay"
      @click.self="continueExploring"
    >
      <section
        class="finish-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="finish-modal-title"
      >
        <button
          class="modal-close"
          type="button"
          aria-label="Close"
          @click="continueExploring"
        >
          ×
        </button>

        <div class="modal-icon">✓</div>

        <h2 id="finish-modal-title">
          Finish this exploration?
        </h2>

        <p class="modal-location">
          Princess Parrot · Great Victoria Desert Dunes
        </p>

        <div class="modal-summary">
          <div>
            <strong>28 min</strong>
            <span>In field</span>
          </div>

          <div>
            <strong>1</strong>
            <span>Observation logged</span>
          </div>
        </div>

        <div class="recorded-section">
          <h3>Recorded Observations</h3>

          <article
            v-for="observation in explorationDetail.observations"
            :key="observation.id"
            class="modal-observation"
          >
            <div class="modal-record-icon">♬</div>

            <div>
              <strong>{{ observation.title }}</strong>
              <span>{{ observation.description }}</span>
            </div>

            <time>{{ observation.time }}</time>
          </article>
        </div>

        <div class="after-finish">
          <strong>◎ After you finish</strong>

          <p>
            Your exploration and observations will be saved to your
            Investigation Journal.
          </p>

          <small>
            Verified field contributions may be added to your
            Contribution Score.
          </small>
        </div>

        <button
          class="complete-button"
          type="button"
          @click="completeExploration"
        >
          Complete Exploration →
        </button>

        <button
          class="continue-button"
          type="button"
          @click="continueExploring"
        >
          Continue Exploring
        </button>
      </section>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  padding: 34px 24px 70px;
  background: #f8faf8;
}

.detail-container {
  width: 100%;
  max-width: 1350px;
  margin: 0 auto;
}

.detail-heading {
  margin-bottom: 24px;
}

.back-button {
  padding: 0;
  color: #496258;
  font-size: 13px;
  background: transparent;
  border: 0;
}

.title-row {
  display: flex;
  margin-top: 11px;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.title-row p {
  margin: 0 0 4px;
  color: #718078;
  font-size: 13px;
}

.title-row h1 {
  margin: 0;
  color: #194b35;
  font-size: 31px;
  font-weight: 700;
}

.session-status {
  padding: 6px 10px;
  color: #9a6411;
  font-size: 12px;
  font-weight: 700;
  background: #ffedc8;
  border-radius: 13px;
}

.detail-layout {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(330px, 0.9fr);
  align-items: start;
  gap: 20px;
}

.detail-map {
  position: relative;
}

.map-summary,
.observation-count {
  position: absolute;
  z-index: 600;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 2px 8px rgba(17, 39, 28, 0.14);
}

.map-summary {
  top: 15px;
  left: 15px;
  display: flex;
  max-width: 530px;
  padding: 10px 12px;
  align-items: center;
  gap: 15px;
  border-radius: 7px;
}

.map-summary strong,
.map-summary small {
  display: block;
}

.map-summary strong {
  color: #405249;
  font-size: 13px;
}

.map-summary small {
  margin-top: 3px;
  color: #7b8580;
  font-size: 11px;
}

.map-summary > span {
  padding: 5px 7px;
  color: #3265e8;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  background: #e7edff;
  border-radius: 5px;
}

.observation-count {
  top: 15px;
  right: 15px;
  padding: 8px 11px;
  color: #276e4d;
  font-size: 12px;
  font-weight: 700;
  border-radius: 14px;
}

.observation-sidebar {
  display: flex;
  flex-direction: column;
  gap: 13px;
}

.species-summary,
.progress-card,
.notice-card,
.finish-card {
  padding: 16px;
  background: #ffffff;
  border: 1px solid #e0e7e2;
  border-radius: 11px;
}

.species-summary {
  display: grid;
  grid-template-columns: 50px 1fr auto;
  align-items: center;
  gap: 11px;
}

.species-summary img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 7px;
}

.species-summary span {
  color: #d45454;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.species-summary h2 {
  margin: 3px 0 1px;
  color: #35483e;
  font-size: 18px;
}

.species-summary em {
  color: #758079;
  font-family: Georgia, serif;
  font-size: 12px;
}

.species-summary > strong {
  color: #3265e8;
  font-size: 15px;
}

.progress-card h2,
.notice-card h2,
.finish-card h2 {
  margin: 0;
  color: #405148;
  font-size: 15px;
  font-weight: 700;
}

.progress-card > p,
.finish-card p {
  margin: 4px 0 13px;
  color: #7b8680;
  font-size: 12px;
  line-height: 1.5;
}

.observation-record {
  display: grid;
  grid-template-columns: 30px 1fr auto;
  margin-top: 9px;
  padding: 11px;
  align-items: start;
  gap: 9px;
  background: #f0f5ff;
  border: 1px solid #b9cdfb;
  border-radius: 8px;
}

.record-icon,
.modal-record-icon {
  display: grid;
  width: 27px;
  height: 27px;
  color: #ffffff;
  place-items: center;
  background: #3265e8;
  border-radius: 7px;
}

.observation-record strong {
  font-size: 13px;
}

.observation-record p {
  margin: 2px 0;
  color: #66736c;
  font-size: 11px;
}

.observation-record a,
.observation-record time {
  font-size: 11px;
}

.card-heading {
  display: flex;
  margin-bottom: 12px;
  justify-content: space-between;
}

.card-heading span {
  color: #718078;
  font-size: 11px;
}

.notice-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  margin-bottom: 13px;
  gap: 7px;
}

.notice-option {
  padding: 9px;
  color: #66726b;
  text-align: left;
  background: #ffffff;
  border: 1px solid #dfe5e1;
  border-radius: 7px;
}

.notice-option.active {
  color: #286f50;
  background: #eff8f3;
  border: 2px solid #2d7a58;
}

.notice-option strong,
.notice-option small {
  display: block;
  font-size: 12px;
}

.notice-option small {
  margin-top: 2px;
  color: #89918d;
  font-size: 11px;
}

.notice-card label {
  display: block;
  margin-bottom: 6px;
  color: #526159;
  font-size: 12px;
  font-weight: 700;
}

.notice-card textarea {
  width: 100%;
  padding: 9px;
  font-size: 12px;
  resize: vertical;
  border: 1px solid #dce3df;
  border-radius: 7px;
}

.attachment-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  margin: 9px 0;
  gap: 7px;
}

.attachment-actions button {
  padding: 8px;
  color: #66736c;
  font-size: 12px;
  background: #ffffff;
  border: 1px dashed #cfd8d2;
  border-radius: 7px;
}

.save-observation {
  width: 100%;
  padding: 11px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  background: #121c2e;
  border: 0;
  border-radius: 7px;
}

.finish-card {
  background: #f5fff9;
  border-color: #bce8ce;
}

.finish-card button {
  width: 100%;
  padding: 11px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  background: #2d7a58;
  border: 0;
  border-radius: 7px;
}

/* Finish modal */

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: grid;
  padding: 20px;
  place-items: center;
  background: rgba(7, 20, 13, 0.72);
  backdrop-filter: blur(2px);
}

.finish-modal {
  position: relative;
  width: 100%;
  max-width: 460px;
  padding: 28px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.3);
}

.modal-close {
  position: absolute;
  top: 14px;
  right: 16px;
  color: #8a948f;
  font-size: 25px;
  background: transparent;
  border: 0;
}

.modal-icon {
  display: grid;
  width: 38px;
  height: 38px;
  margin-bottom: 14px;
  color: #277653;
  font-size: 21px;
  font-weight: 700;
  place-items: center;
  background: #dff4e8;
  border-radius: 9px;
}

.finish-modal h2 {
  margin: 0 0 5px;
  color: #273a31;
  font-size: 23px;
  font-weight: 700;
}

.modal-location {
  margin: 0 0 18px;
  color: #748078;
  font-size: 13px;
}

.modal-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  margin-bottom: 18px;
  gap: 10px;
}

.modal-summary div {
  padding: 12px;
  text-align: center;
  background: #f5f7f5;
  border: 1px solid #e4e9e6;
  border-radius: 8px;
}

.modal-summary strong,
.modal-summary span {
  display: block;
}

.modal-summary strong {
  color: #273d32;
  font-size: 21px;
}

.modal-summary span {
  margin-top: 3px;
  color: #7b8580;
  font-size: 12px;
}

.recorded-section h3 {
  margin-bottom: 9px;
  color: #68736d;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.modal-observation {
  display: grid;
  grid-template-columns: 30px 1fr auto;
  padding: 10px;
  align-items: center;
  gap: 9px;
  background: #f0f5ff;
  border: 1px solid #bed0fa;
  border-radius: 7px;
}

.modal-observation strong,
.modal-observation span {
  display: block;
}

.modal-observation strong {
  font-size: 12px;
}

.modal-observation span,
.modal-observation time {
  color: #6d7872;
  font-size: 11px;
}

.after-finish {
  margin: 16px 0;
  padding: 13px;
  color: #397157;
  background: #effaf4;
  border: 1px solid #b9e8ce;
  border-radius: 8px;
}

.after-finish strong {
  font-size: 12px;
}

.after-finish p {
  margin: 5px 0;
  color: #54685e;
  font-size: 12px;
  line-height: 1.45;
}

.after-finish small {
  color: #809087;
  font-size: 11px;
}

.complete-button,
.continue-button {
  width: 100%;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 7px;
}

.complete-button {
  margin-bottom: 8px;
  color: #ffffff;
  background: #2d7a58;
  border: 0;
}

.continue-button {
  color: #526159;
  background: #ffffff;
  border: 1px solid #dce3df;
}

@media (max-width: 950px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .detail-page {
    padding: 25px 14px 50px;
  }

  .title-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .map-summary,
  .observation-count {
    position: relative;
    top: auto;
    right: auto;
    left: auto;
    margin-bottom: 8px;
  }

  .map-summary {
    max-width: none;
    align-items: flex-start;
    flex-direction: column;
  }

  .notice-grid {
    grid-template-columns: 1fr;
  }
}
</style>