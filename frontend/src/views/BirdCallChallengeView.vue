<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { gallerySpecies } from '../mocks/gallery'
import { useAudio } from '../composables/useAudio'
import { useExplorer } from '../composables/useExplorer'
import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const imageMap = {
  'night-parrot.jpg': nightParrotImage,
  'princess-parrot.jpg': princessParrotImage,
  'plains-wanderer.jpg': plainsWandererImage,
  'rufous-scrub-bird.jpg': rufousScrubBirdImage,
  'malleefowl.jpg': malleefowlImage,
  'dusky-grasswren.jpg': duskyGrasswrenImage
}

const router = useRouter()
const { explorer } = useExplorer()
const { currentlyPlayingId, currentTime, duration, playAudio, stopAudio } = useAudio()

const answers = ref([])
const selectedAnswer = ref(null)
const submitted = ref(false)
const correctAnswerId = ref(null)

const isCorrect = computed(
  () => submitted.value && selectedAnswer.value === correctAnswerId.value
)

const theCorrectBird = computed(() => gallerySpecies.find(b => b.id === correctAnswerId.value))

function generateQuestion() {
  stopAudio()
  selectedAnswer.value = null
  submitted.value = false

  // Pick random correct
  const shuffledSpecies = [...gallerySpecies].sort(() => Math.random() - 0.5)
  const correct = shuffledSpecies[0]
  correctAnswerId.value = correct.id
  
  // Use all 6 birds, just shuffle them
  const options = [...gallerySpecies].sort(() => Math.random() - 0.5)
  answers.value = options.map(b => ({
    id: b.id,
    name: b.name,
    scientificName: b.scientificName
  }))
}

onMounted(() => {
  generateQuestion()
})

onBeforeUnmount(() => {
  stopAudio()
})

function selectAnswer(id) {
  if (submitted.value) return
  selectedAnswer.value = id
}

async function submitAnswer() {
  if (!selectedAnswer.value) return
  submitted.value = true
  
  if (isCorrect.value && explorer.value) {
    try {
      await fetch(`${API_BASE_URL}/api/v1/challenge/success`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: explorer.value.displayName })
      })
    } catch (e) {
      console.error('Failed to save challenge points', e)
    }
  }
}

function tryAgain() {
  selectedAnswer.value = null
  submitted.value = false
}

function playCall() {
  if (correctAnswerId.value) {
    playAudio(correctAnswerId.value)
  }
}

function nextCall() {
  generateQuestion()
}
</script>

<template>
  <main class="challenge-page">
    <div class="challenge-container">
      <button class="back-button" type="button" @click="router.push('/gallery')">
        ← Back to Gallery
      </button>

      <section class="page-heading">
        <p class="eyebrow">AUDITORY FIELD ID CHALLENGE</p>
        <h1>Guess the Bird</h1>
        <p>
          Listen carefully to the audio snippet below and identify which
          Australian bird is calling across the nocturnal plains.
        </p>
      </section>

      <div class="challenge-layout" :class="{ submitted: submitted }">
        <div class="challenge-column">
          <section class="audio-card">
            <div class="audio-meta">
              <span>● Mystery Call</span>
            </div>

            <div class="waveform-box">
              <div class="waveform" aria-hidden="true">
                <span
                  v-for="(height, index) in [
                    12, 18, 27, 42, 63, 78, 68, 51, 31, 20,
                    33, 58, 75, 82, 70, 49, 30, 19, 13, 9
                  ]"
                  :key="index"
                  :style="{ height: `${height}%` }"
                ></span>
              </div>

              <div class="time-row">
                <span>0:{{ Math.floor(currentTime).toString().padStart(2, '0') }}</span>
                <div class="progress-track">
                  <div class="progress-value" :style="{ width: (duration ? (currentTime / duration) * 100 : 0) + '%' }"></div>
                </div>
                <span>0:{{ Math.floor(duration || 0).toString().padStart(2, '0') }}</span>
              </div>
            </div>

            <div class="audio-actions">
              <button class="play-button" type="button" @click="playCall">
                {{ currentlyPlayingId === correctAnswerId ? '■ Stop Audio' : '🔊 Play Bird Call' }}
              </button>


            </div>
          </section>

          <section class="answer-card">
            <div class="answer-heading">
              <h2>
                <span class="question-icon">?</span>
                Which bird is this?
              </h2>

              <span>Single choice</span>
            </div>

            <div class="answer-grid">
              <button
                v-for="answer in answers"
                :key="answer.id"
                class="answer-option"
                :class="{
                  selected: selectedAnswer === answer.id,
                  correct:
                    submitted &&
                    answer.id === correctAnswerId &&
                    selectedAnswer === correctAnswerId,
                  incorrect:
                    submitted &&
                    answer.id === selectedAnswer &&
                    selectedAnswer !== correctAnswerId
                }"
                type="button"
                @click="selectAnswer(answer.id)"
              >
                <span class="choice-indicator">
                  {{
                    submitted &&
                    answer.id === correctAnswerId &&
                    selectedAnswer === correctAnswerId
                      ? '✓'
                      : ''
                  }}
                </span>

                <span class="answer-text">
                  <strong>{{ answer.name }}</strong>
                  <em>{{ answer.scientificName }}</em>
                </span>

                <span
                  v-if="selectedAnswer === answer.id"
                  class="selected-mark"
                >
                  ●
                </span>
              </button>
            </div>

            

            <button
              v-if="!submitted"
              class="submit-button"
              type="button"
              :disabled="!selectedAnswer"
              @click="submitAnswer"
            >
              Submit Answer
            </button>

            
          </section>
        </div>

        <aside v-if="submitted" class="result-card">
          <div class="result-heading" :style="{ color: isCorrect ? '#2b7a54' : '#e74c3c' }">
            {{ isCorrect ? '🎉 Correct! 🎉' : '❌ Incorrect ❌' }}
          </div>

          <img
            v-if="isCorrect"
            :src="theCorrectBird ? imageMap[theCorrectBird.image] : nightParrotImage"
            :alt="theCorrectBird?.name"
          />

          <div class="result-content">
            <h3 v-if="isCorrect">{{ theCorrectBird?.name }}</h3>
            <h3 v-else>That was not correct.</h3>
            
            <p v-if="isCorrect">
              Great job! You successfully identified the call of the {{ theCorrectBird?.name }}.
            </p>
            <p v-else>
              You selected the wrong bird. Listen carefully to the audio again.
            </p>

            <button
              class="investigation-button"
              type="button"
              style="margin-top: 1rem; width: 100%"
              @click="isCorrect ? nextCall() : tryAgain()"
            >
              {{ isCorrect ? 'Next Question →' : 'Try Again ↻' }}
            </button>
          </div>
        </aside>
      </div>
    </div>
  </main>
</template>

<style scoped>
.challenge-page {
  min-height: calc(100vh - 80px);
  padding: 42px 24px 80px;
  background: #fbfcfa;
  color: #173f30;
}

.challenge-container {
  width: min(1060px, 100%);
  margin: 0 auto;
}

.back-button {
  margin-bottom: 28px;
  padding: 0;
  border: 0;
  background: transparent;
  color: #217451;
  font-weight: 700;
  cursor: pointer;
}

.page-heading {
  max-width: 650px;
  margin-bottom: 34px;
}

.eyebrow {
  margin: 0 0 7px;
  color: #2c835f;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.page-heading h1 {
  margin: 0 0 10px;
  color: #183e30;
  font-size: clamp(32px, 4vw, 46px);
  line-height: 1.05;
}

.page-heading > p:last-child {
  margin: 0;
  color: #68756e;
  line-height: 1.6;
}

.challenge-layout {
  display: grid;
  grid-template-columns: minmax(0, 700px);
  justify-content: center;
  gap: 24px;
  align-items: start;
}

.challenge-layout.submitted {
  grid-template-columns: minmax(0, 620px) minmax(280px, 370px);
}

.challenge-column {
  display: grid;
  gap: 20px;
}

.audio-card,
.answer-card,
.result-card {
  border: 1px solid #e1e7e3;
  border-radius: 14px;
  background: white;
  box-shadow: 0 8px 24px rgb(25 67 49 / 5%);
}

.audio-card,
.answer-card {
  padding: 24px;
}

.audio-meta {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 17px;
  color: #385748;
  font-size: 15px;
  font-weight: 700;
}

.quality {
  padding: 5px 9px;
  border-radius: 20px;
  background: #f0f3f1;
  white-space: nowrap;
}

.waveform-box {
  padding: 22px 20px 15px;
  border-radius: 10px;
  background: #f4f6f4;
}

.waveform {
  height: 94px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
}

.waveform span {
  width: 10px;
  min-height: 8px;
  border-radius: 8px;
  background: #186744;
}

.waveform span:nth-child(-n + 3),
.waveform span:nth-last-child(-n + 5) {
  background: #b7d3c6;
}

.time-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 10px;
  color: #557065;
  font-size: 14px;
}

.progress-track {
  height: 4px;
  overflow: hidden;
  border-radius: 10px;
  background: #dce4df;
}

.progress-value {
  width: 36%;
  height: 100%;
  background: #176543;
}

.audio-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 18px;
}

.audio-actions button {
  border: 0;
  cursor: pointer;
}

.play-button {
  padding: 11px 18px;
  border-radius: 24px;
  background: #217954;
  color: white;
  font-weight: 700;
}

.secondary-actions {
  display: flex;
  align-items: center;
  gap: 9px;
}

.secondary-actions button,
.speed {
  padding: 9px 13px;
  border-radius: 20px;
  background: #f0f3f1;
  color: #3e5249;
}

.answer-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.answer-heading h2 {
  display: flex;
  align-items: center;
  gap: 9px;
  margin: 0;
  color: #243d32;
  font-size: 25px;
}

.answer-heading > span {
  color: #718078;
  font-size: 14px;
  font-weight: 700;
}

.question-icon {
  display: inline-grid;
  width: 24px;
  height: 24px;
  place-items: center;
  border-radius: 50%;
  background: #e7f6ee;
  color: #28815c;
  font-size: 16px;
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.answer-option {
  display: grid;
  grid-template-columns: 26px 1fr auto;
  align-items: center;
  gap: 10px;
  min-height: 70px;
  padding: 13px;
  border: 1px solid transparent;
  border-radius: 10px;
  background: #f3f5f3;
  color: #31473d;
  text-align: left;
  cursor: pointer;
}

.answer-option:hover,
.answer-option.selected {
  border-color: #65b991;
  background: #ddf8e9;
}

.answer-option.correct {
  border-color: #25845e;
  background: #d9f8e8;
}

.answer-option.incorrect {
  border-color: #d77070;
  background: #fff0f0;
}

.choice-indicator {
  display: grid;
  width: 22px;
  height: 22px;
  place-items: center;
  border-radius: 50%;
  background: #dce3df;
  color: white;
  font-size: 15px;
  font-weight: 800;
}

.answer-option.selected .choice-indicator {
  background: #247a56;
}

.answer-text {
  display: grid;
  gap: 3px;
}

.answer-text strong {
  font-size: 17px;
}

.answer-text em {
  color: #7a8881;
  font-family: Georgia, serif;
  font-size: 14px;
}

.selected-mark {
  color: #1d704e;
  font-size: 14px;
}

.submit-button {
  width: 100%;
  margin-top: 18px;
  padding: 13px 20px;
  border: 0;
  border-radius: 7px;
  background: #267d58;
  color: white;
  font-weight: 800;
  cursor: pointer;
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.incorrect-message {
  margin: 16px 0 0;
  color: #b14444;
  font-size: 16px;
}

.result-card {
  overflow: hidden;
}

.result-heading {
  padding: 14px 18px;
  background: #09633f;
  color: white;
  font-size: 24px;
  font-weight: 800;
}

.result-card > img {
  display: block;
  width: 100%;
  height: 210px;
  object-fit: cover;
}

.result-content {
  padding: 20px;
}

.status-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  color: #37805f;
  font-size: 13px;
  font-weight: 800;
}

.status-badge {
  color: #cf4e4e;
}

.result-content h2 {
  margin: 14px 0 2px;
  font-size: 27px;
}

.scientific-name {
  margin: 0 0 18px;
  color: #718078;
  font-family: Georgia, serif;
  font-style: italic;
}

.fact-box {
  padding: 15px;
  border-radius: 9px;
  background: #f2f6f3;
  color: #496057;
  font-size: 15px;
  line-height: 1.5;
}

.fact-box p {
  margin: 6px 0 0;
}

.result-actions {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  margin-top: 17px;
}

.result-actions button {
  padding: 11px 13px;
  border-radius: 7px;
  font-weight: 700;
  cursor: pointer;
}

.next-button {
  border: 0;
  background: #17734d;
  color: white;
}

.bird-button {
  border: 1px solid #dce4df;
  background: white;
  color: #395246;
}

@media (max-width: 900px) {
  .challenge-layout.submitted {
    grid-template-columns: 1fr;
  }

  .result-card {
    max-width: 620px;
  }
}

@media (max-width: 620px) {
  .challenge-page {
    padding: 28px 15px 60px;
  }

  .answer-grid {
    grid-template-columns: 1fr;
  }

  .audio-meta,
  .audio-actions {
    flex-direction: column;
  }

  .secondary-actions {
    justify-content: space-between;
  }
}
</style>