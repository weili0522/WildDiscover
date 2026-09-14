<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])
</script>

<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="modal-backdrop"
      @click.self="emit('close')"
    >
      <section
        class="species-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="species-modal-title"
      >
        <button
          class="close-button"
          type="button"
          aria-label="Close"
          @click="emit('close')"
        >
          ×
        </button>

        <!-- Left -->
        <div class="modal-left">
          <div class="image-wrapper">
            <img
              src="../assets/night-parrot.jpg"
              alt="Night Parrot"
              class="modal-image"
            >

            <span class="status-badge">
              ● Critically Endangered
            </span>

            <span class="verified-badge">
              ALA Verified
            </span>
          </div>

          <section class="soundscape-card">
            <div class="soundscape-heading">
              <strong>♬ Bioacoustic Soundscape</strong>
              <span>0:18</span>
            </div>

            <div class="audio-player">
              <button type="button" aria-label="Play bird call">
                ▶
              </button>

              <div class="waveform" aria-hidden="true">
                <span
                  v-for="height in [8, 14, 10, 21, 13, 18, 9, 22, 15, 8, 16, 11]"
                  :key="height"
                  :style="{ height: `${height}px` }"
                ></span>
              </div>
            </div>

            <p>
              Listen to the Night Parrot’s distinctive whistling and
              bell-like call recorded in remote spinifex hummocks.
            </p>
          </section>
        </div>

        <!-- Right -->
        <div class="modal-right">
          <div class="title-row">
            <h2 id="species-modal-title">
              Night Parrot
            </h2>

            <em>Pezoporus occidentalis</em>
          </div>

          <p class="introduction">
            A rare nocturnal ground parrot found in remote spinifex
            habitats in Australia.
          </p>

          <div class="information-grid">
            <article>
              <span>△ Conservation Status</span>
              <strong class="critical-text">
                Critically Endangered
              </strong>
            </article>

            <article>
              <span>♧ Habitat</span>
              <strong>
                Spinifex grasslands &amp; arid regions
              </strong>
            </article>

            <article>
              <span>◷ Active Time</span>
              <strong>
                Dusk and night (nocturnal)
              </strong>
            </article>

            <article>
              <span>⌖ Where It Lives</span>
              <strong>
                Remote inland WA &amp; QLD
              </strong>
            </article>
          </div>

          <article class="why-card">
            <span>◎ Why It Matters</span>

            <p>
              One of Australia’s rarest birds and a flagship species
              for inland biodiversity conservation and invasive
              predator control.
            </p>
          </article>

          <article class="fact-card">
            <strong>♧ Did you know?</strong>

            <p>
              Night Parrots are exceptionally elusive and are far more
              frequently detected using acoustic listening sensors
              than visual sightings.
            </p>
          </article>

          <div class="modal-actions">
            <RouterLink
              to="/map?species=night-parrot"
              class="map-button"
              @click="emit('close')"
            >
              ▣ View on Map
            </RouterLink>

            <button
              type="button"
              @click="emit('close')"
            >
              Close
            </button>
          </div>
        </div>
      </section>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: grid;
  padding: 25px;
  place-items: center;
  background: rgba(8, 17, 12, 0.68);
  backdrop-filter: blur(2px);
}

.species-modal {
  position: relative;
  display: grid;
  grid-template-columns: minmax(260px, 0.9fr) minmax(350px, 1.25fr);
  width: 100%;
  max-width: 820px;
  max-height: 92vh;
  padding: 22px;
  overflow-y: auto;
  gap: 21px;
  background: #ffffff;
  border-radius: 13px;
  box-shadow: 0 25px 75px rgba(0, 0, 0, 0.3);
}

.close-button {
  position: absolute;
  top: 12px;
  right: 14px;
  z-index: 5;
  padding: 4px;
  color: #7a8580;
  font-size: 19px;
  line-height: 1;
  background: transparent;
  border: 0;
}

.modal-left,
.modal-right {
  min-width: 0;
}

.image-wrapper {
  position: relative;
}

.modal-image {
  display: block;
  width: 100%;
  height: 245px;
  object-fit: cover;
  border-radius: 9px;
}

.status-badge,
.verified-badge {
  position: absolute;
  top: 11px;
  padding: 5px 7px;
  font-size: 7px;
  font-weight: 700;
  border-radius: 10px;
}

.status-badge {
  left: 11px;
  color: #b84343;
  background: #ffe1e1;
}

.verified-badge {
  right: 11px;
  color: #536158;
  background: rgba(255, 255, 255, 0.95);
}

.soundscape-card {
  margin-top: 11px;
  padding: 13px;
  background: #f8faf8;
  border: 1px solid #e1e7e3;
  border-radius: 8px;
}

.soundscape-heading {
  display: flex;
  margin-bottom: 10px;
  color: #27704f;
  font-size: 9px;
  justify-content: space-between;
}

.soundscape-heading span {
  color: #7c8781;
}

.audio-player {
  display: flex;
  margin-bottom: 10px;
  align-items: center;
  gap: 11px;
}

.audio-player button {
  display: grid;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  color: #ffffff;
  place-items: center;
  background: #2d7a58;
  border: 0;
  border-radius: 50%;
}

.waveform {
  display: flex;
  height: 26px;
  align-items: center;
  gap: 4px;
}

.waveform span {
  display: block;
  width: 3px;
  background: #31a171;
  border-radius: 2px;
}

.soundscape-card p {
  margin: 0;
  color: #758079;
  font-size: 8px;
  line-height: 1.45;
}

.modal-right {
  padding: 6px 5px 0 0;
}

.title-row {
  display: flex;
  padding-right: 25px;
  align-items: baseline;
  gap: 8px;
}

.title-row h2 {
  margin: 0;
  color: #205d43;
  font-size: 25px;
  font-weight: 700;
}

.title-row em {
  color: #77827c;
  font-family: Georgia, serif;
  font-size: 9px;
}

.introduction {
  margin: 8px 0 14px;
  color: #69756e;
  font-size: 10px;
  line-height: 1.45;
}

.information-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  margin-bottom: 10px;
  gap: 8px;
}

.information-grid article {
  padding: 10px;
  background: #f7f9f7;
  border: 1px solid #e6ebe8;
  border-radius: 7px;
}

.information-grid span,
.information-grid strong {
  display: block;
}

.information-grid span {
  margin-bottom: 5px;
  color: #468267;
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
}

.information-grid strong {
  color: #4c5b53;
  font-size: 9px;
}

.information-grid .critical-text {
  color: #c04646;
}

.why-card,
.fact-card {
  padding: 11px;
  border-radius: 7px;
}

.why-card {
  margin-bottom: 9px;
  background: #f7f9f7;
  border: 1px solid #e5eae7;
}

.why-card span {
  color: #438064;
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
}

.why-card p,
.fact-card p {
  margin: 5px 0 0;
  color: #58675f;
  font-size: 9px;
  line-height: 1.45;
}

.fact-card {
  color: #277452;
  background: #e7f8ef;
  border: 1px solid #bfe8d1;
}

.fact-card strong {
  font-size: 9px;
}

.modal-actions {
  display: flex;
  margin-top: 11px;
  align-items: center;
  justify-content: space-between;
}

.map-button,
.modal-actions button {
  padding: 9px 13px;
  font-size: 9px;
  font-weight: 700;
  border-radius: 6px;
}

.map-button {
  color: #ffffff;
  text-decoration: none;
  background: #2d7a58;
}

.modal-actions button {
  color: #59675f;
  background: transparent;
  border: 0;
}

@media (max-width: 720px) {
  .species-modal {
    grid-template-columns: 1fr;
  }

  .modal-image {
    height: 220px;
  }
}

@media (max-width: 480px) {
  .modal-backdrop {
    padding: 12px;
  }

  .species-modal {
    padding: 16px;
  }

  .information-grid {
    grid-template-columns: 1fr;
  }

  .title-row {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>