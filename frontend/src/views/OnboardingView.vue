<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useExplorer } from '../composables/useExplorer'

const router = useRouter()
const { explorer, startExplorerSession } = useExplorer()

const currentStep = ref(explorer.value ? 'ready' : 'welcome')
const isGenerating = ref(false)

function continueAsExplorer() {
  isGenerating.value = true

  window.setTimeout(() => {
    startExplorerSession()
    currentStep.value = 'ready'
    isGenerating.value = false
  }, 700)
}

function startExploring() {
  router.push('/map')
}
</script>

<template>
  <section class="onboarding-page">
    <div class="onboarding-container">
      <!-- Welcome screen -->
      <div v-if="currentStep === 'welcome'" class="onboarding-card">
        <div class="brand-icon">W</div>

        <p class="eyebrow">PRIVATE EXPLORATION</p>

        <h1>Welcome to WildDiscover</h1>

        <p class="subtitle">
          Explore birds, save your journeys and join the community
          while keeping your identity private.
        </p>

        <div class="feature-grid">
          <article class="feature-item">
            <div class="feature-icon">◌</div>
            <h2>Stay Anonymous</h2>
            <p>No personal information, email or password is required.</p>
          </article>

          <article class="feature-item">
            <div class="feature-icon">⌖</div>
            <h2>Save Your Journeys</h2>
            <p>Keep a private record of the birds and places you explore.</p>
          </article>

          <article class="feature-item">
            <div class="feature-icon">♧</div>
            <h2>Join the Community</h2>
            <p>Share discoveries and contribute without revealing your identity.</p>
          </article>
        </div>

        <button
          class="continue-button"
          type="button"
          :disabled="isGenerating"
          @click="continueAsExplorer"
        >
          {{ isGenerating ? 'Generating cryptographic session…' : 'Continue as an Explorer' }}
        </button>

        <p class="account-note">No email or password needed</p>

        <p class="protocol-note">
          Compliant with zero-knowledge open citizen science protocols · v2.4
        </p>
      </div>

      <!-- Explorer-ready screen -->
      <div v-else class="onboarding-card ready-card">
        <div class="success-icon">✓</div>

        <p class="eyebrow">ANONYMOUS SESSION CREATED</p>

        <h1>You’re Ready to Explore!</h1>

        <p class="subtitle">
          Your anonymous WildDiscover identity is ready.
        </p>

        <div class="explorer-profile">
          <div class="avatar">E</div>

          <div>
            <strong>{{ explorer?.displayName }}</strong>
            <span>{{ explorer?.level }}</span>
          </div>
        </div>

        <ul class="readiness-list">
          <li>
            <span>✓</span>
            Journal ready
          </li>

          <li>
            <span>✓</span>
            Community ready
          </li>

          <li>
            <span>✓</span>
            Contribution points ready
          </li>
        </ul>

        <button
          class="continue-button"
          type="button"
          @click="startExploring"
        >
          Start Exploring
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.onboarding-page {
  min-height: calc(100vh - 70px);
  padding: 64px 20px;
  background:
    radial-gradient(circle at top left, rgba(26, 115, 79, 0.1), transparent 36%),
    #f5f8f5;
}

.onboarding-container {
  width: 100%;
  max-width: 920px;
  margin: 0 auto;
}

.onboarding-card {
  padding: 48px;
  text-align: center;
  background: #ffffff;
  border: 1px solid #e3ebe6;
  border-radius: 20px;
  box-shadow: 0 18px 50px rgba(25, 63, 44, 0.1);
}

.brand-icon,
.success-icon {
  display: grid;
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  place-items: center;
  background: #146c4a;
  border-radius: 50%;
}

.success-icon {
  background: #2f8f63;
}

.eyebrow {
  margin-bottom: 10px;
  color: #2f8f63;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.15em;
}

h1 {
  margin-bottom: 14px;
  color: #173d2d;
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
}

.subtitle {
  max-width: 650px;
  margin: 0 auto 36px;
  color: #637069;
  font-size: 17px;
  line-height: 1.7;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 36px;
}

.feature-item {
  padding: 24px 18px;
  text-align: left;
  background: #f7faf8;
  border: 1px solid #e3ebe6;
  border-radius: 14px;
}

.feature-icon {
  margin-bottom: 16px;
  color: #146c4a;
  font-size: 30px;
}

.feature-item h2 {
  margin-bottom: 8px;
  color: #173d2d;
  font-size: 17px;
  font-weight: 700;
}

.feature-item p {
  margin: 0;
  color: #6d7872;
  font-size: 14px;
  line-height: 1.6;
}

.continue-button {
  min-width: 260px;
  padding: 14px 26px;
  color: #ffffff;
  font-weight: 600;
  background: #146c4a;
  border: 0;
  border-radius: 8px;
}

.continue-button:hover {
  background: #0f573c;
}

.continue-button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.account-note {
  margin: 14px 0 0;
  color: #637069;
  font-size: 13px;
}

.protocol-note {
  margin: 36px 0 0;
  color: #929b96;
  font-size: 12px;
}

.explorer-profile {
  display: flex;
  max-width: 380px;
  margin: 0 auto 28px;
  padding: 18px;
  text-align: left;
  align-items: center;
  gap: 14px;
  background: #f7faf8;
  border: 1px solid #dfe9e3;
  border-radius: 14px;
}

.avatar {
  display: grid;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  color: #ffffff;
  font-weight: 700;
  place-items: center;
  background: #146c4a;
  border-radius: 50%;
}

.explorer-profile strong,
.explorer-profile span {
  display: block;
}

.explorer-profile strong {
  color: #173d2d;
}

.explorer-profile span {
  margin-top: 3px;
  color: #6d7872;
  font-size: 13px;
}

.readiness-list {
  max-width: 380px;
  margin: 0 auto 32px;
  padding: 0;
  text-align: left;
  list-style: none;
}

.readiness-list li {
  display: flex;
  padding: 12px 0;
  color: #3f4f47;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #e6ece8;
}

.readiness-list span {
  color: #2f8f63;
  font-weight: 700;
}

@media (max-width: 768px) {
  .onboarding-page {
    padding: 28px 14px;
  }

  .onboarding-card {
    padding: 32px 20px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .continue-button {
    width: 100%;
    min-width: 0;
  }
}
</style>