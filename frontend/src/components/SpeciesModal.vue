<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false
  },
species: {
    type: Object,
    default: null
  },
  playingId: {
    type: String,
    default: null
  }
})

const emit = defineEmits([
  'close',
  'view-map',
  'listen'
])

function closeModal() {
  emit('close')
}

function handleBackdropClick(event) {
  if (event.target === event.currentTarget) {
    closeModal()
  }
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="visible && species"
      class="modal-backdrop"
      role="presentation"
      @click="handleBackdropClick"
    >
      <article
        class="species-modal"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`modal-title-${species.id}`"
      >
        <button
          class="close-button"
          type="button"
          aria-label="Close details"
          @click="closeModal"
        >
          ×
        </button>

        <div class="modal-grid">
          <section class="left-column">
            <div class="image-wrapper">
              <img
                :src="species.image"
                :alt="species.name"
              >

              <span
                class="status-badge"
                :class="species.statusClass"
              >
                ● {{ species.status }}
              </span>

              <span
                v-if="species.verified"
                class="verified-badge"
              >
                ALA Verified
              </span>
            </div>

            <div class="audio-card">
              <div class="audio-heading">
                <div>
                  <strong>♬ Bioacoustic Soundscape</strong>
                  <span>{{ species.audioDuration }}</span>
                </div>
              </div>

              <div class="audio-controls">
                                <button
                  type="button"
                  class="play-button"
                  @click="emit('listen', species)"
                >
                  {{ playingId === species.id ? '■' : '▶' }}
                </button>

                <div class="waveform" aria-hidden="true">
                  <span
                    v-for="(height, index) in [
                      8, 14, 10, 20, 13, 24, 17,
                      10, 19, 13, 7, 15, 9
                    ]"
                    :key="index"
                    :style="{ height: `${height}px` }"
                  />
                </div>
              </div>

              <p>
                Listen to this bird’s distinctive call recorded
                in its natural habitat.
              </p>
            </div>
          </section>

          <section class="right-column">
            <header class="species-title">
              <div>
                <h2 :id="`modal-title-${species.id}`">
                  {{ species.name }}
                </h2>

                <em>{{ species.scientificName }}</em>
              </div>
            </header>

            <p class="summary">
              {{ species.description }}
            </p>

            <div class="information-grid">
              <div class="information-card">
                <span>⚠ Conservation Status</span>
                <strong :class="species.statusClass">
                  {{ species.status }}
                </strong>
              </div>

              <div class="information-card">
                <span>♣ Habitat</span>
                <strong>{{ species.habitat }}</strong>
              </div>

              <div class="information-card">
                <span>◷ Active Time</span>
                <strong>{{ species.activeTime }}</strong>
              </div>

              <div class="information-card">
                <span>⌖ Where It Lives</span>
                <strong>{{ species.location }}</strong>
              </div>
            </div>

            <div class="why-card">
              <span>♧ Why It Matters</span>
              <p>{{ species.whyItMatters }}</p>
            </div>

            <div class="fact-card">
              <strong>Did you know?</strong>
              <p>{{ species.didYouKnow }}</p>
            </div>

            
            <div class="source-attribution">
              Source: Atlas of Living Australia (ALA) & EPBC Act Database
            </div>

            <div class="modal-actions">
              <button
                class="map-button"
                type="button"
                @click="emit('view-map', species)"
              >
                ⌖ View on Map
              </button>

              <button
                class="secondary-close"
                type="button"
                @click="closeModal"
              >
                Close
              </button>
            </div>
          </section>
        </div>
      </article>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  z-index: 2000;
  inset: 0;
  display: grid;
  padding: 24px;
  place-items: center;
  background: rgba(8, 20, 14, 0.65);
  backdrop-filter: blur(2px);
}

.species-modal {
  position: relative;
  width: min(900px, 100%);
  max-height: calc(100vh - 48px);
  padding: 22px;
  overflow-y: auto;
  background: #ffffff;
  border-radius: 14px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
}

.close-button {
  position: absolute;
  z-index: 2;
  top: 12px;
  right: 15px;
  width: 32px;
  height: 32px;
  color: #65716b;
  font-size: 28px;
  line-height: 1;
  background: rgba(255, 255, 255, 0.94);
  border: 0;
  border-radius: 50%;
  cursor: pointer;
}

.modal-grid {
  display: grid;
  grid-template-columns: minmax(260px, 0.9fr) minmax(360px, 1.35fr);
  gap: 22px;
}

.image-wrapper {
  position: relative;
  height: 245px;
  overflow: hidden;
  border-radius: 10px;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge,
.verified-badge {
  position: absolute;
  top: 12px;
  padding: 5px 8px;
  font-size: 11px;
  font-weight: 700;
  border-radius: 12px;
}

.status-badge {
  left: 12px;
}

.verified-badge {
  right: 12px;
  color: #526159;
  background: rgba(255, 255, 255, 0.94);
}

.status-badge.critical {
  color: #b74646;
  background: #ffe2e2;
}

.status-badge.endangered {
  color: #9c5e1c;
  background: #fff0d5;
}

.status-badge.vulnerable {
  color: #267653;
  background: #dff4e8;
}

.status-badge.least-concern {
  color: #35705a;
  background: #e7f5ed;
}

.audio-card {
  margin-top: 12px;
  padding: 14px;
  border: 1px solid #dfe7e2;
  border-radius: 10px;
}

.audio-heading > div {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.audio-heading strong {
  color: #287353;
  font-size: 14px;
}

.audio-heading span {
  color: #75817b;
  font-size: 12px;
}

.audio-controls {
  display: flex;
  margin-top: 12px;
  align-items: center;
  gap: 12px;
}

.play-button {
  width: 35px;
  height: 35px;
  color: #ffffff;
  background: #287353;
  border: 0;
  border-radius: 50%;
  cursor: pointer;
}

.waveform {
  display: flex;
  height: 28px;
  flex: 1;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.waveform span {
  width: 3px;
  background: #3a906c;
  border-radius: 3px;
}

.audio-card p {
  margin: 10px 0 0;
  color: #6d7973;
  font-size: 13px;
  line-height: 1.5;
}

.species-title {
  padding-right: 32px;
}

.species-title h2 {
  margin: 0 0 3px;
  color: #174b35;
  font-size: 30px;
}

.species-title em {
  color: #7b8680;
  font-family: Georgia, serif;
  font-size: 15px;
}

.summary {
  margin: 12px 0;
  color: #5f6d66;
  font-size: 15px;
  line-height: 1.55;
}

.information-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}

.information-card {
  display: flex;
  min-height: 68px;
  padding: 11px;
  flex-direction: column;
  gap: 6px;
  background: #f7f9f7;
  border: 1px solid #e4e9e5;
  border-radius: 8px;
}

.information-card span {
  color: #79857f;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.information-card strong {
  color: #34483e;
  font-size: 13px;
  line-height: 1.35;
}

.information-card strong.critical {
  color: #c14646;
}

.information-card strong.endangered {
  color: #a06522;
}

.information-card strong.vulnerable,
.information-card strong.least-concern {
  color: #287353;
}

.why-card,
.fact-card {
  margin-top: 10px;
  padding: 11px;
  border-radius: 8px;
}

.why-card {
  background: #f7f9f7;
  border: 1px solid #e4e9e5;
}

.fact-card {
  color: #226347;
  background: #e7faef;
  border: 1px solid #bfe8d0;
}

.why-card span {
  color: #718079;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.why-card p,
.fact-card p {
  margin: 5px 0 0;
  font-size: 13px;
  line-height: 1.45;
}

.fact-card strong {
  font-size: 13px;
}

.modal-actions {
  display: flex;
  margin-top: 13px;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.map-button,
.secondary-close {
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
}

.map-button {
  color: #ffffff;
  background: #287353;
  border: 0;
}

.secondary-close {
  color: #53625a;
  background: transparent;
  border: 0;
}

@media (max-width: 720px) {
  .modal-backdrop {
    padding: 12px;
  }

  .species-modal {
    padding: 16px;
  }

  .modal-grid {
    grid-template-columns: 1fr;
  }

  .information-grid {
    grid-template-columns: 1fr;
  }

  .image-wrapper {
    height: 220px;
  }
}

.source-attribution {
  margin-top: 16px;
  margin-bottom: 2px;
  font-size: 13px;
  color: #7b8a82;
  font-style: italic;
  text-align: right;
}

</style>