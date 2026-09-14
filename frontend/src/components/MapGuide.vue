<script setup>
defineProps({
  activeStep: {
    type: Number,
    default: 1
  }
})

const steps = [
  {
    number: 1,
    title: 'Choose Bird',
    description: 'Pick an elusive or threatened native bird from our featured species.'
  },
  {
    number: 2,
    title: 'View Predictions',
    description: 'Discover suitable micro-habitats, food corridors, and ecological zones.'
  },
  {
    number: 3,
    title: 'Plan Exploration',
    description: 'Select a promising area and save it to your investigation journal.'
  }
]
</script>

<template>
  <section class="guide-card">
    <div class="guide-header">
      <div class="guide-icon">◫</div>

      <div>
        <h2>Welcome to Habitat Explorer</h2>
        <p>3-step citizen science journey</p>
      </div>
    </div>

    <ol class="guide-steps">
      <li
        v-for="step in steps"
        :key="step.number"
        :class="{ active: step.number <= activeStep }"
      >
        <span class="step-number">
          {{ step.number }}
        </span>

        <div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
        </div>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.guide-card {
  padding: 22px;
  background: #ffffff;
  border: 1px solid #e1e8e3;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(26, 69, 49, 0.05);
}

.guide-header {
  display: flex;
  padding-bottom: 18px;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #e7ece8;
}

.guide-icon {
  display: grid;
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  color: #237453;
  font-size: 19px;
  place-items: center;
  background: #dff4e9;
  border-radius: 10px;
}

.guide-header h2 {
  margin: 0 0 4px;
  color: #236044;
  font-size: 16px;
  font-weight: 700;
}

.guide-header p {
  margin: 0;
  color: #718078;
  font-size: 11px;
}

.guide-steps {
  margin: 0;
  padding: 18px 0 0;
  list-style: none;
}

.guide-steps li {
  position: relative;
  display: grid;
  grid-template-columns: 28px 1fr;
  padding-bottom: 18px;
  gap: 11px;
}

.guide-steps li:not(:last-child)::after {
  position: absolute;
  top: 28px;
  bottom: 3px;
  left: 13px;
  width: 1px;
  content: '';
  background: #dde5e0;
}

.step-number {
  position: relative;
  z-index: 1;
  display: grid;
  width: 28px;
  height: 28px;
  color: #68766e;
  font-size: 11px;
  font-weight: 700;
  place-items: center;
  background: #edf0ee;
  border-radius: 50%;
}

.guide-steps li.active .step-number {
  color: #176540;
  background: #a9efc9;
}

.guide-steps h3 {
  margin: 2px 0 4px;
  color: #34463d;
  font-size: 12px;
  font-weight: 700;
}

.guide-steps p {
  margin: 0;
  color: #748078;
  font-size: 10px;
  line-height: 1.45;
}
</style>