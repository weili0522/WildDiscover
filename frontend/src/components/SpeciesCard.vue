<script setup>
defineProps({
  species: {
    type: Object,
    required: true
  },
  featured: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])
</script>

<template>
  <article
    class="species-card"
    :class="{ featured }"
    @click="emit('select', species)"
  >
    <div class="card-image-wrapper">
      <img
        :src="species.image"
        :alt="species.name"
        class="species-image"
      />

      <div
        v-if="featured"
        class="featured-overlay"
      >
        <span
          class="status-badge"
          :class="species.statusClass"
        >
          {{ species.status }}
        </span>

        <h2>{{ species.name }}</h2>

        <p>{{ species.scientificName }}</p>
      </div>
    </div>

    <div
      v-if="!featured"
      class="card-body"
    >
      <span
        class="status-badge"
        :class="species.statusClass"
      >
        {{ species.status }}
      </span>

      <h2>{{ species.name }}</h2>

      <p>{{ species.scientificName }}</p>
    </div>
  </article>
</template>

<style scoped>
.species-card {
  overflow: hidden;

  background-color: #ffffff;

  border: 1px solid #eeeeee;
  border-radius: 8px;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.species-card:hover {
  transform: translateY(-3px);

  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.08);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
}

.species-image {
  width: 100%;
  height: 210px;

  object-fit: cover;
}

.featured .species-image {
  height: 290px;
}

.featured-overlay {
  position: absolute;

  left: 0;
  right: 0;
  bottom: 0;

  padding: 54px 20px 18px;

  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.72),
    rgba(0, 0, 0, 0)
  );

  color: #ffffff;
}

.featured-overlay h2 {
  margin: 10px 0 3px;

  color: #ffffff;

  font-size: 24px;
  font-weight: 600;
}

.featured-overlay p {
  margin: 0;

  color: #eeeeee;

  font-size: 12px;
  font-style: italic;
}

.card-body {
  padding: 16px 18px 18px;
}

.card-body h2 {
  margin: 10px 0 4px;

  color: #1f1f1f;

  font-size: 20px;
  font-weight: 500;
}

.card-body p {
  margin: 0;

  color: #666666;

  font-size: 12px;
  font-style: italic;
}

.status-badge {
  display: inline-block;

  padding: 4px 9px;

  border-radius: 20px;

  font-size: 9px;
  font-weight: 600;
}

.status-badge.critical {
  color: #a84848;
  background-color: #fde5e5;
}

.status-badge.vulnerable {
  color: #555555;
  background-color: #f1f1ef;

  border: 1px solid #ddddda;
}

.status-badge.lesser {
  color: #2d7c56;
  background-color: #dff4e5;
}

.status-badge.endangered {
  color: #a84848;
  background-color: #fde5e5;
}
</style>