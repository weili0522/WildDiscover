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
      <div class="species-modal">

        <!-- Close button -->
        <button
          class="close-button"
          type="button"
          aria-label="Close"
          @click="emit('close')"
        >
          x
        </button>

        <!-- Night Parrot image -->
        <img
          src="../assets/night-parrot.jpg"
          alt="Night Parrot"
          class="modal-image"
        />

        <!-- Modal content -->
        <div class="modal-content">

          <!-- Title -->
          <div class="modal-title-row">
            <div>
              <h2>Night Parrot</h2>

              <p class="scientific-name">
                Pezoporus occidentalis
              </p>
            </div>

            <span class="status-badge">
              Critically Endangered
            </span>
          </div>

          <!-- Species information -->
          <div class="species-info-grid">

            <div class="info-item">
              <span class="info-label">
                PRIMARY HABITAT
              </span>

              <p>
                Arid and semi-arid spinifex grasslands
              </p>
            </div>

            <div class="info-item">
              <span class="info-label">
                BEHAVIOR
              </span>

              <p>
                Strictly nocturnal and ground-dwelling
              </p>
            </div>

            <div class="info-item">
              <span class="info-label">
                DIET
              </span>

              <p>
                Seeds of grasses and herbaceous plants
              </p>
            </div>

          </div>

          <!-- Did you know -->
          <div class="did-you-know">

            <h3>💡 Did you know?</h3>

            <ul>
              <li>
                Often called the “holy grail” of birdwatching due to
                its extreme rarity and elusive nature.
              </li>

              <li>
                They spend their days roosting deep inside dense,
                tunnel-like spinifex rings.
              </li>
            </ul>

          </div>

          <!-- Action -->
          <div class="modal-actions">

            <RouterLink
              to="/gallery/night-parrot/sightings"
              class="sighting-button"
            >
              View Sighting Gallery ↗
            </RouterLink>

            <p>
              Explore all open-source community sightings of this bird.
            </p>

          </div>

        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* =========================
   Background overlay
   ========================= */

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 2000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 30px;

  background-color: rgba(0, 0, 0, 0.55);
}


/* =========================
   Modal container
   ========================= */

.species-modal {
  position: relative;

  width: 100%;
  max-width: 700px;
  max-height: 90vh;

  overflow-y: auto;

  background-color: #ffffff;

  border-radius: 16px;

  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.25);
}


/* =========================
   Close button
   ========================= */

.close-button {
  position: absolute;
  top: 14px;
  right: 14px;

  z-index: 5;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  padding: 0;

  border: none;
  border-radius: 50%;

  background-color: rgba(0, 0, 0, 0.45);
  color: #ffffff;

  font-size: 24px;
  font-weight: 300;
  line-height: 1;

  cursor: pointer;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.65);
}


/* =========================
   Main image
   ========================= */

.modal-image {
  display: block;

  width: 100%;
  height: 260px;

  object-fit: cover;

  border-radius: 16px 16px 0 0;
}


/* =========================
   Content
   ========================= */

.modal-content {
  padding: 28px 34px 32px;
}


/* =========================
   Title
   ========================= */

.modal-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 20px;

  margin-bottom: 28px;
}

.modal-title-row h2 {
  margin: 0 0 5px;

  color: #146c4a;

  font-size: 32px;
  font-weight: 700;
}

.scientific-name {
  margin: 0;

  color: #6b6b6b;

  font-size: 13px;
  font-style: italic;
}

.status-badge {
  flex-shrink: 0;

  display: inline-block;

  padding: 5px 10px;

  border-radius: 20px;

  background-color: #fde5e5;
  color: #a84848;

  font-size: 10px;
  font-weight: 600;
}


/* =========================
   Species information
   ========================= */

.species-info-grid {
  display: grid;

  grid-template-columns: 1fr 1fr;

  gap: 22px 36px;

  margin-bottom: 26px;
}

.info-item:last-child {
  grid-column: 1 / 2;
}

.info-label {
  display: block;

  margin-bottom: 6px;

  color: #277654;

  font-size: 10px;
  font-weight: 700;

  letter-spacing: 0.5px;
}

.info-item p {
  margin: 0;

  color: #444444;

  font-size: 13px;
  line-height: 1.5;
}


/* =========================
   Did you know
   ========================= */

.did-you-know {
  margin-bottom: 28px;

  padding: 20px 22px;

  background-color: #e5f5eb;

  border-radius: 10px;
}

.did-you-know h3 {
  margin: 0 0 12px;

  color: #277654;

  font-size: 17px;
  font-weight: 600;
}

.did-you-know ul {
  margin: 0;

  padding-left: 19px;

  color: #3f6f58;

  font-size: 12px;
  line-height: 1.6;
}

.did-you-know li + li {
  margin-top: 8px;
}


/* =========================
   Bottom action
   ========================= */

.modal-actions {
  text-align: center;
}

.sighting-button {
  display: inline-block;

  padding: 11px 24px;

  border-radius: 24px;

  background-color: #146c4a;
  color: #ffffff;

  font-size: 12px;
  font-weight: 500;

  text-decoration: none;

  transition: background-color 0.2s ease;
}

.sighting-button:hover {
  background-color: #0f573c;
  color: #ffffff;
}

.modal-actions p {
  margin: 10px 0 0;

  color: #777777;

  font-size: 10px;
}


/* =========================
   Responsive
   ========================= */

@media (max-width: 600px) {
  .modal-backdrop {
    padding: 15px;
  }

  .species-modal {
    max-height: 95vh;
  }

  .modal-image {
    height: 210px;
  }

  .modal-content {
    padding: 24px 20px;
  }

  .modal-title-row {
    align-items: flex-start;

    flex-direction: column;

    gap: 12px;
  }

  .modal-title-row h2 {
    font-size: 27px;
  }

  .species-info-grid {
    grid-template-columns: 1fr;

    gap: 18px;
  }

  .info-item:last-child {
    grid-column: auto;
  }
}
</style>