<script setup>
import { ref } from 'vue'

const selectedAnswer = ref('')
const submitted = ref(false)

const options = [
  {
    id: 'A',
    text: 'Dense eucalyptus canopies'
  },
  {
    id: 'B',
    text: 'Old-growth spinifex grass rings'
  },
  {
    id: 'C',
    text: 'Coastal mangrove swamps'
  },
  {
    id: 'D',
    text: 'Red sand dunes'
  }
]

const submitAnswer = () => {
  if (!selectedAnswer.value) return

  submitted.value = true
}

const resetQuiz = () => {
  selectedAnswer.value = ''
  submitted.value = false
}
</script>

<template>
  <div class="quiz-wrapper">

    <!-- Quiz -->
    <div
      v-if="!submitted"
      class="quiz-card"
    >
      <h2>Test Your Knowledge</h2>

      <hr />

      <p class="quiz-question">
        “The Night Parrot was famously presumed extinct for over a century.
        What type of vegetation does it heavily rely on for roosting and hiding?”
      </p>

      <div class="quiz-options">
        <label
          v-for="option in options"
          :key="option.id"
          class="quiz-option"
          :class="{ selected: selectedAnswer === option.id }"
        >
          <input
            v-model="selectedAnswer"
            type="radio"
            name="night-parrot-question"
            :value="option.id"
          />

          <span class="custom-radio"></span>

          <span class="option-text">
            {{ option.id }}. {{ option.text }}
          </span>
        </label>
      </div>

      <button
        class="submit-button"
        :disabled="!selectedAnswer"
        @click="submitAnswer"
      >
        Submit Answer
      </button>
    </div>


    <!-- Correct result -->
    <div
      v-else
      class="result-card"
    >
      <div class="result-header">
        <div class="check-circle">
          ✓
        </div>
      </div>

      <div class="result-content">
        <h2>
          {{ selectedAnswer === 'B' ? 'Great Job!' : 'Not Quite!' }}
        </h2>

        <div class="answer-box">
          <div class="answer-label">
            ✓ CORRECT ANSWER
          </div>

          <h3>
            B. Old-growth spinifex grass rings
          </h3>

          <p>
            “Night Parrots rely on old-growth spinifex for roosting
            and protection from heat and predators.”
          </p>
        </div>

        <RouterLink
          to="/"
          class="result-button primary-button"
        >
          Back to Home
        </RouterLink>

        <button
          class="try-again"
          @click="resetQuiz"
        >
          Try Again
        </button>
      </div>
    </div>
    
    <RouterLink
      to="/gallery"
      class="gallery-cta"
    >
      Curious about other wildlife? Explore the Gallery!
    </RouterLink>

  </div>
</template>

<style scoped>
.quiz-wrapper {
  width: 100%;
}


/* =========================
   Quiz card
   ========================= */

.quiz-card {
  background-color: #ffffff;

  border: 1px solid #e3e3e3;
  border-radius: 10px;

  padding: 20px;
}

.quiz-card h2 {
  margin: 0;

  color: #1f1f1f;

  font-size: 21px;
  font-weight: 600;
}

.quiz-card hr {
  border: none;
  border-top: 1px solid #e3e3e3;

  margin: 14px 0 18px;
}

.quiz-question {
  color: #333333;

  font-size: 13px;
  line-height: 1.5;

  margin-bottom: 18px;
}


/* =========================
   Options
   ========================= */

.quiz-options {
  display: flex;
  flex-direction: column;

  gap: 10px;
}

.quiz-option {
  position: relative;

  display: flex;
  align-items: center;

  gap: 10px;

  width: 100%;

  padding: 12px 14px;

  border: 1px solid #dddddd;
  border-radius: 7px;

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.quiz-option:hover {
  border-color: #8b8b8b;
}

.quiz-option.selected {
  border-color: #666666;
}

.quiz-option input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.custom-radio {
  width: 17px;
  height: 17px;

  flex-shrink: 0;

  border: 1px solid #cccccc;
  border-radius: 50%;

  position: relative;
}

.quiz-option.selected .custom-radio {
  border-color: #5ba06d;
}

.quiz-option.selected .custom-radio::after {
  content: '';

  position: absolute;

  width: 11px;
  height: 11px;

  top: 2px;
  left: 2px;

  border-radius: 50%;

  background-color: #5ba06d;
}

.option-text {
  color: #333333;

  font-size: 13px;
}


/* =========================
   Submit
   ========================= */

.submit-button {
  width: 100%;

  margin-top: 18px;

  padding: 12px;

  border: none;
  border-radius: 6px;

  background-color: #237553;
  color: #ffffff;

  font-size: 13px;
  font-weight: 500;

  cursor: pointer;
}

.submit-button:hover:not(:disabled) {
  background-color: #195f43;
}

.submit-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}


/* =========================
   Result
   ========================= */

.result-card {
  overflow: hidden;

  background-color: #ffffff;

  border: 1px solid #e3e3e3;
  border-radius: 10px;
}

.result-header {
  height: 52px;

  display: flex;
  justify-content: center;
  align-items: center;

  background-color: #2a7b59;
}

.check-circle {
  width: 36px;
  height: 36px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background-color: #ffffff;
  color: #2a7b59;

  font-size: 24px;
  font-weight: 700;
}

.result-content {
  padding: 20px;

  text-align: center;
}

.result-content > h2 {
  margin: 0 0 16px;

  color: #146c4a;

  font-size: 25px;
  font-weight: 700;
}

.answer-box {
  padding: 16px;

  margin-bottom: 18px;

  background-color: #f4f6f3;

  border-radius: 8px;

  text-align: left;
}

.answer-label {
  color: #666666;

  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.4px;

  margin-bottom: 10px;
}

.answer-box h3 {
  margin: 0 0 10px;

  color: #1f1f1f;

  font-size: 18px;
  font-weight: 600;

  text-align: center;
}

.answer-box p {
  margin: 0;

  padding-left: 12px;

  border-left: 2px solid #c7d9cf;

  color: #555555;

  font-size: 12px;
  line-height: 1.5;

  font-style: italic;

  text-align: center;
}

.result-button {
  display: block;

  width: 70%;

  margin: 10px auto;

  padding: 10px 14px;

  border-radius: 30px;

  font-size: 12px;
  font-weight: 500;

  text-decoration: none;
}

.primary-button {
  background-color: #146c4a;
  color: #ffffff;
}

.primary-button:hover {
  background-color: #0f573c;
  color: #ffffff;
}

.secondary-button {
  background-color: #ffffff;
  color: #146c4a;

  border: 1px solid #146c4a;
}

.secondary-button:hover {
  background-color: #f5faf7;
}

.try-again {
  margin-top: 8px;

  background: none;
  border: none;

  color: #777777;

  font-size: 11px;

  cursor: pointer;
}

.gallery-cta {
  display: block;

  width: 100%;
  margin-top: 16px;
  padding: 13px 18px;

  border: 1px solid #146c4a;
  border-radius: 8px;

  background-color: #f5faf7;
  color: #146c4a;

  font-size: 13px;
  font-weight: 600;
  line-height: 1.4;
  text-align: center;
  text-decoration: none;

  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

.gallery-cta:hover {
  background-color: #146c4a;
  color: #ffffff;
}
</style>