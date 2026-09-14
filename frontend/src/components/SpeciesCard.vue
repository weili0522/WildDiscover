<script setup>
defineProps({
  species: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'view-details',
  'view-map',
  'listen'
])
</script>

<template>
  <article class="species-card">
    <div class="image-wrapper">
      <img
        :src="species.image"
        :alt="species.name"
        class="species-image"
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

    <div class="card-body">
      <div class="species-heading">
        <h2>{{ species.name }}</h2>
        <em>{{ species.scientificName }}</em>
      </div>

      <p class="description">
        {{ species.description }}
      </p>

      <div class="audio-row">
        <button
          class="listen-button"
          type="button"
          @click="emit('listen', species)"
        >
          ▶ Listen to Call
        </button>

        <div class="waveform" aria-hidden="true">
          <span
            v-for="height in [7, 13, 9, 18, 11, 20, 14, 8, 16, 10, 6]"
            :key="height"
            :style="{ height: `${height}px` }"
          ></span>
        </div>

        <small>{{ species.audioDuration }}</small>
      </div>

      <div class="card-actions">
        <button
          class="map-link"
          type="button"
          @click="emit('view-map', species)"
        >
          ⌖ View on Map
        </button>

        <button
          class="details-button"
          type="button"
          @click="emit('view-details', species)"
        >
          View Details
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.species-card {
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #e0e7e2;
  border-radius: 11px;
  box-shadow: 0 3px 12px rgba(24, 61, 44, 0.05);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.species-card:hover {
  box-shadow: 0 9px 24px rgba(24, 61, 44, 0.11);
  transform: translateY(-3px);
}

.image-wrapper {
  position: relative;
  height: 290px;
  overflow: hidden;
}

.species-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge,
.verified-badge {
  position: absolute;
  top: 13px;
  padding: 5px 8px;
  font-size: 8px;
  font-weight: 700;
  border-radius: 11px;
}

.status-badge {
  left: 13px;
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

.verified-badge {
  right: 13px;
  color: #526159;
  background: rgba(255, 255, 255, 0.94);
}

.card-body {
  padding: 17px;
}

.species-heading {
  display: flex;
  margin-bottom: 9px;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.species-heading h2 {
  margin: 0;
  color: #23533e;
  font-size: 17px;
  font-weight: 700;
}

.species-heading em {
  color: #79837e;
  font-family: Georgia, serif;
  font-size: 9px;
}

.description {
  min-height: 44px;
  margin: 0 0 12px;
  color: #66736c;
  font-size: 10px;
  line-height: 1.5;
}

.audio-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  margin-bottom: 14px;
  align-items: center;
  gap: 9px;
}

.listen-button {
  padding: 6px 9px;
  color: #267653;
  font-size: 8px;
  font-weight: 700;
  background: #e0f4e9;
  border: 0;
  border-radius: 11px;
}

.waveform {
  display: flex;
  height: 22px;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.waveform span {
  display: block;
  width: 2px;
  background: #398b68;
  border-radius: 2px;
}

.audio-row small {
  color: #7a857f;
  font-size: 8px;
}

.card-actions {
  display: flex;
  padding-top: 12px;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #e9edea;
}

.map-link,
.details-button {
  padding: 7px 10px;
  font-size: 9px;
  font-weight: 700;
  border-radius: 6px;
}

.map-link {
  color: #327557;
  background: transparent;
  border: 0;
}

.details-button {
  color: #ffffff;
  background: #2d7a58;
  border: 0;
}

.details-button:hover {
  background: #205e43;
}

@media (max-width: 600px) {
  .image-wrapper {
    height: 235px;
  }

  .species-heading {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }
}
</style>