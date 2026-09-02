<script setup>
defineProps({
  sighting: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <article class="sighting-card">

    <div class="image-wrapper">
      <img
        :src="sighting.image"
        :alt="sighting.location"
        class="sighting-image"
      />

      <span class="type-badge">
        {{ sighting.type }}
      </span>
    </div>

    <div class="card-content">

      <div class="location">
        📍 {{ sighting.location }}
      </div>

      <h2>
        {{ sighting.title }}
      </h2>

      <hr />

      <div class="date">
        {{ sighting.date }}
      </div>

    </div>

  </article>
</template>

<style scoped>
.sighting-card {
  overflow: hidden;

  background-color: #ffffff;

  border: 1px solid #e4e4e4;
  border-radius: 10px;
}

.image-wrapper {
  position: relative;
}

.sighting-image {
  width: 100%;
  height: 230px;

  object-fit: cover;
}

.type-badge {
  position: absolute;

  top: 14px;
  right: 14px;

  padding: 6px 12px;

  background-color: rgba(255, 255, 255, 0.92);

  border-radius: 20px;

  color: #333333;

  font-size: 11px;
  font-weight: 600;
}

.card-content {
  padding: 18px 20px 20px;
}

.location {
  margin-bottom: 12px;

  color: #277654;

  font-size: 12px;
  font-weight: 600;
}

.card-content h2 {
  margin: 0;

  color: #1f1f1f;

  font-size: 20px;
  font-weight: 600;

  line-height: 1.25;
}

.card-content hr {
  margin: 16px 0;

  border: none;
  border-top: 1px solid #eeeeee;
}

.date {
  color: #555555;

  font-size: 12px;
}
</style>