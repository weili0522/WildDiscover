<script setup>
import { useRouter } from 'vue-router'

import HabitatMap from '../components/HabitatMap.vue'
import { completedExplorationSummary } from '../mocks/journal'
import nightParrotImage from '../assets/night-parrot.jpg'

const router = useRouter()
</script>

<template>
  <div class="summary-page">
    <div class="summary-container">
      <section class="page-heading">
        <button
          class="back-link"
          type="button"
          @click="router.push('/journal')"
        >
          ← Back to Investigation Journal
        </button>

        <div class="heading-row">
          <div>
            <p>
              Pilbara Sector 4 &nbsp;/&nbsp;
              Field Summary {{ completedExplorationSummary.fieldSummaryId }}
            </p>

            <div class="title-row">
              <h1>{{ completedExplorationSummary.title }}</h1>

              <span class="completed-label">
                ✓ {{ completedExplorationSummary.status }}
              </span>
            </div>
          </div>

          <div class="completion-badges">
            <span>
              ▣ Completed:
              {{ completedExplorationSummary.completedAt }}
            </span>

            <span class="points">
              ♧ +{{ completedExplorationSummary.contributionPoints }}
              Points Awarded
            </span>

            <span>▧ Read-Only Field Record</span>
          </div>
        </div>
      </section>

      <section class="summary-layout">
        <!-- Left map -->
        <div class="map-column">
          <div class="recorded-boundary">
            <div>
              <strong>
                ✓ Recorded Boundary:
                {{ completedExplorationSummary.sector }}
              </strong>

              <small>
                {{ completedExplorationSummary.area }} surveyed •
                Session closed at
                {{ completedExplorationSummary.sessionDate }}
              </small>
            </div>

            <span>
              ↑ {{ completedExplorationSummary.probability }}%
              {{ completedExplorationSummary.probabilityLevel }}
            </span>
          </div>

          <div class="finalized-label">
            ▣ Finalized Field Map
          </div>

          <HabitatMap
            key="summary-map"
            mode="summary"
          />

          <div class="environment-record">
            <p>
              ♧ Survey Environmental Record:
              {{ completedExplorationSummary.environmentalRecord }}
            </p>

            <span>
              ▣ {{ completedExplorationSummary.privacyProtection }}
            </span>
          </div>
        </div>

        <!-- Right summary -->
        <aside class="summary-sidebar">
          <section class="exploration-summary-card">
            <div class="card-title">
              <div>
                <h2>▣ Exploration Summary</h2>
                <p>Session record successfully compiled</p>
              </div>

              <span>✓ Verified</span>
            </div>

            <div class="species-summary">
              <img
                :src="nightParrotImage"
                alt="Night Parrot"
              >

              <div>
                <strong>
                  {{ completedExplorationSummary.species.commonName }}
                </strong>

                <em>
                  {{ completedExplorationSummary.species.scientificName }}
                </em>

                <small>◎ {{ completedExplorationSummary.sector }}</small>
              </div>

              <span>
                ↑ {{ completedExplorationSummary.probability }}%
                {{ completedExplorationSummary.probabilityLevel }}
              </span>
            </div>

            <div class="summary-metrics">
              <div>
                <span>Exploration Time</span>
                <strong>
                  {{ completedExplorationSummary.explorationTime }}
                </strong>
              </div>

              <div>
                <span>Observations</span>
                <strong>
                  {{ completedExplorationSummary.observationsRecorded }}
                  recorded
                </strong>
              </div>

              <div>
                <span>Habitat Potential</span>
                <strong>
                  {{ completedExplorationSummary.probability }}% High
                </strong>
              </div>
            </div>
          </section>

          <section class="findings-card">
            <h2>⌁ Recorded Findings (2)</h2>

            <article
              v-for="finding in completedExplorationSummary.findings"
              :key="finding.id"
              class="finding"
              :class="finding.type"
            >
              <div class="finding-icon">
                {{ finding.type === 'audio' ? '♬' : '⌖' }}
              </div>

              <div>
                <strong>{{ finding.title }}</strong>
                <p>{{ finding.description }}</p>

                <span>
                  {{ finding.attachment }}
                  <template v-if="finding.duration">
                    · {{ finding.duration }}
                  </template>
                </span>
              </div>

              <time>{{ finding.time }}</time>
            </article>
          </section>

          <section class="notes-card">
            <h2>⚑ Saved Field Notes</h2>

            <p>
              “{{ completedExplorationSummary.fieldNotes }}”
            </p>
          </section>

          <section class="contribution-card">
            <div class="contribution-icon">♙</div>

            <div>
              <strong>Contribution Recorded</strong>
              <span>Added to your Explorer contribution score.</span>
            </div>

            <b>
              +{{ completedExplorationSummary.contributionPoints }}
              Contribution Points
            </b>
          </section>

          <button
            class="journal-button"
            type="button"
            @click="router.push('/journal')"
          >
            Back to Journal →
          </button>

          <button
            class="gallery-button"
            type="button"
            @click="router.push('/gallery')"
          >
            ▣ View Gallery
          </button>
        </aside>
      </section>
    </div>
  </div>
</template>

<style scoped>
.summary-page {
  min-height: 100vh;
  padding: 34px 24px 70px;
  background: #f8faf8;
}

.summary-container {
  width: 100%;
  max-width: 1350px;
  margin: 0 auto;
}

.page-heading {
  margin-bottom: 23px;
}

.back-link {
  padding: 0;
  color: #47705e;
  font-size: 13px;
  background: transparent;
  border: 0;
}

.heading-row {
  display: flex;
  margin-top: 10px;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.heading-row p {
  margin: 0 0 4px;
  color: #748078;
  font-size: 12px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-row h1 {
  margin: 0;
  color: #174a34;
  font-size: 30px;
  font-weight: 700;
}

.completed-label {
  padding: 5px 9px;
  color: #277452;
  font-size: 12px;
  font-weight: 700;
  background: #d9f4e5;
  border-radius: 12px;
}

.completion-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 7px;
}

.completion-badges span {
  padding: 7px 9px;
  color: #647169;
  font-size: 11px;
  background: #ffffff;
  border: 1px solid #e0e6e2;
  border-radius: 6px;
}

.completion-badges .points {
  color: #267250;
  background: #e2f6eb;
}

.summary-layout {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(330px, 0.85fr);
  align-items: start;
  gap: 20px;
}

.map-column {
  position: relative;
}

.recorded-boundary,
.finalized-label {
  position: absolute;
  z-index: 600;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 2px 8px rgba(17, 39, 28, 0.14);
}

.recorded-boundary {
  top: 15px;
  left: 15px;
  display: flex;
  max-width: 520px;
  padding: 10px 12px;
  align-items: center;
  gap: 14px;
  border-radius: 7px;
}

.recorded-boundary strong,
.recorded-boundary small {
  display: block;
}

.recorded-boundary strong {
  color: #405249;
  font-size: 13px;
}

.recorded-boundary small {
  margin-top: 3px;
  color: #79847e;
  font-size: 11px;
}

.recorded-boundary > span {
  padding: 5px 7px;
  color: #3265e8;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  background: #e6edff;
  border-radius: 5px;
}

.finalized-label {
  top: 15px;
  right: 15px;
  padding: 8px 11px;
  color: #536159;
  font-size: 12px;
  border-radius: 6px;
}

.environment-record {
  margin-top: 12px;
  padding: 12px 14px;
  background: #ffffff;
  border: 1px solid #e1e7e3;
  border-radius: 8px;
}

.environment-record p {
  margin: 0 0 8px;
  color: #627068;
  font-size: 12px;
}

.environment-record span {
  display: inline-block;
  padding: 5px 8px;
  color: #277351;
  font-size: 11px;
  font-weight: 700;
  background: #e5f7ed;
  border-radius: 5px;
}

.summary-sidebar {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.exploration-summary-card,
.findings-card,
.notes-card,
.contribution-card {
  padding: 16px;
  background: #ffffff;
  border: 1px solid #e0e7e2;
  border-radius: 11px;
}

.card-title {
  display: flex;
  margin-bottom: 14px;
  justify-content: space-between;
}

.card-title h2,
.findings-card h2,
.notes-card h2 {
  margin: 0;
  color: #405148;
  font-size: 14px;
  font-weight: 700;
}

.card-title p {
  margin: 3px 0 0;
  color: #7b8580;
  font-size: 11px;
}

.card-title > span {
  padding: 4px 7px;
  color: #277452;
  font-size: 11px;
  background: #dff4e8;
  border-radius: 10px;
}

.species-summary {
  display: grid;
  grid-template-columns: 50px 1fr auto;
  margin-bottom: 12px;
  padding: 10px;
  align-items: center;
  gap: 9px;
  background: #f6f8f6;
  border-radius: 8px;
}

.species-summary img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.species-summary strong,
.species-summary em,
.species-summary small {
  display: block;
}

.species-summary strong {
  font-size: 14px;
}

.species-summary em,
.species-summary small {
  margin-top: 2px;
  color: #77827c;
  font-size: 11px;
}

.species-summary > span {
  color: #3265e8;
  font-size: 11px;
  font-weight: 700;
}

.summary-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 7px;
}

.summary-metrics div {
  padding: 9px 6px;
  text-align: center;
  background: #f3f5f3;
  border-radius: 6px;
}

.summary-metrics span,
.summary-metrics strong {
  display: block;
}

.summary-metrics span {
  margin-bottom: 4px;
  color: #78837d;
  font-size: 10px;
}

.summary-metrics strong {
  font-size: 12px;
}

.finding {
  display: grid;
  grid-template-columns: 28px 1fr auto;
  margin-top: 9px;
  padding: 10px;
  align-items: start;
  gap: 8px;
  border: 1px solid;
  border-radius: 7px;
}

.finding.audio {
  background: #f0f5ff;
  border-color: #bed0fa;
}

.finding.signs {
  background: #fff8e9;
  border-color: #efd18c;
}

.finding-icon {
  display: grid;
  width: 27px;
  height: 27px;
  color: #ffffff;
  place-items: center;
  background: #3265e8;
  border-radius: 6px;
}

.finding.signs .finding-icon {
  background: #df8b24;
}

.finding strong {
  font-size: 12px;
}

.finding p {
  margin: 2px 0;
  color: #69756f;
  font-size: 11px;
}

.finding span,
.finding time {
  color: #63736b;
  font-size: 11px;
}

.notes-card p {
  margin: 9px 0 0;
  color: #5f6c65;
  font-size: 12px;
  font-style: italic;
  line-height: 1.55;
}

.contribution-card {
  display: grid;
  grid-template-columns: 34px 1fr auto;
  color: #277452;
  align-items: center;
  gap: 9px;
  background: #effaf4;
  border-color: #b9e8ce;
}

.contribution-icon {
  display: grid;
  width: 32px;
  height: 32px;
  color: #ffffff;
  place-items: center;
  background: #21a46d;
  border-radius: 7px;
}

.contribution-card strong,
.contribution-card span {
  display: block;
}

.contribution-card strong {
  font-size: 13px;
}

.contribution-card span {
  margin-top: 2px;
  font-size: 11px;
}

.contribution-card b {
  padding: 6px 8px;
  font-size: 11px;
  background: #c8f1da;
  border-radius: 12px;
}

.journal-button,
.gallery-button {
  width: 100%;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 7px;
}

.journal-button {
  color: #ffffff;
  background: #2d7a58;
  border: 0;
}

.gallery-button {
  color: #536159;
  background: #ffffff;
  border: 1px solid #dce3df;
}

@media (max-width: 950px) {
  .heading-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .completion-badges {
    justify-content: flex-start;
  }

  .summary-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .summary-page {
    padding: 25px 14px 50px;
  }

  .title-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .recorded-boundary,
  .finalized-label {
    position: relative;
    top: auto;
    right: auto;
    left: auto;
    margin-bottom: 8px;
  }

  .recorded-boundary {
    max-width: none;
    align-items: flex-start;
    flex-direction: column;
  }

  .summary-metrics {
    grid-template-columns: 1fr;
  }
}
</style>