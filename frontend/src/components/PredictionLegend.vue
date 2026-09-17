<script setup>
const predictionLevels = [
  {
    id: 'high',
    label: 'High',
    description: 'Prime cover',
    range: '≥ 70%'
  },
  {
    id: 'medium',
    label: 'Medium',
    description: 'Seasonal',
    range: '40–69%'
  },
  {
    id: 'low',
    label: 'Low',
    description: 'Marginal',
    range: '< 40%'
  }
]
</script>

<template>
  <section class="legend-card">
    <div class="legend-header">
      <h2>Prediction Legend</h2>

      <span class="accessible-label">
        ◉ Color-Blind Safe
      </span>
    </div>

    <p class="legend-description">
      Shape-coded indicators ensure all environmental zones are
      distinguishable in high-glare field conditions.
    </p>

    <div class="legend-grid">
      <div
        v-for="level in predictionLevels"
        :key="level.id"
        class="legend-item"
      >
        <span
          class="legend-shape"
          :class="`shape-${level.id}`"
          aria-hidden="true"
        ></span>

        <strong>{{ level.label }}</strong>
        <small>{{ level.description }}</small>
        <span class="probability-range">{{ level.range }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.legend-card {
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e1e8e3;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(26, 69, 49, 0.05);
}

.legend-header {
  display: flex;
  margin-bottom: 11px;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.legend-header h2 {
  margin: 0;
  color: #33463c;
  font-size: 17px;
  font-weight: 700;
}

.accessible-label {
  padding: 4px 7px;
  color: #587368;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  background: #eef5f1;
  border-radius: 10px;
}

.legend-description {
  margin-bottom: 16px;
  color: #7a857f;
  font-size: 13px;
  line-height: 1.5;
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.legend-item {
  display: flex;
  min-height: 91px;
  padding: 11px 6px;
  text-align: center;
  flex-direction: column;
  align-items: center;
  background: #f5f7f5;
  border: 1px solid #edf0ee;
  border-radius: 8px;
}

.legend-shape {
  display: block;
  width: 10px;
  height: 10px;
  margin-bottom: 8px;
}

.shape-high {
  background: #3265e8;
  transform: rotate(45deg);
}

.shape-medium {
  width: 0;
  height: 0;
  border-right: 6px solid transparent;
  border-bottom: 11px solid #df8b24;
  border-left: 6px solid transparent;
}

.shape-low {
  background: transparent;
  border: 2px solid #8c9791;
  border-radius: 50%;
}

.legend-item strong {
  color: #3e4d45;
  font-size: 14px;
}

.legend-item small {
  margin-top: 3px;
  color: #78837d;
  font-size: 11px;
}

.probability-range {
  margin-top: 5px;
  color: #66736c;
  font-size: 11px;
  font-weight: 600;
}
</style>