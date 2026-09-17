<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExplorer } from '../composables/useExplorer'

const router = useRouter()
const { explorer, registerAndLogin, login, startGuestSession } = useExplorer()

const currentStep = ref(explorer.value ? 'ready' : 'welcome')
const isGenerating = ref(false)
const isSignInMode = ref(false)

const generatedUsername = ref('')
const password = ref('')

onMounted(() => {
  generatedUsername.value = `Explorer_${Math.floor(1000 + Math.random() * 9000)}`
})

async function handleAuth() {
  if (!password.value) return alert('Please enter a password')
  if (isSignInMode.value && !generatedUsername.value) return alert('Please enter your username')
  
  isGenerating.value = true
  try {
    if (isSignInMode.value) {
      await login(generatedUsername.value, password.value)
    } else {
      await registerAndLogin(generatedUsername.value, password.value)
    }
    currentStep.value = 'ready'
  } catch (e) {
    alert('Authentication failed. Please check your credentials.')
  } finally {
    isGenerating.value = false
  }
}

function handleGuest() {
  startGuestSession()
  router.push('/map')
}

function startExploring() {
  router.push('/map')
}
</script>

<template>
  <section class="onboarding-page">
    <div class="onboarding-container">
      <div v-if="currentStep === 'welcome'" class="onboarding-card">
        <div class="brand-icon">W</div>
        <p class="eyebrow">PRIVATE EXPLORATION</p>
        <h1>Welcome to WildDiscover</h1>
        <p class="subtitle">
          Explore birds, save your journeys and join the community
          while keeping your identity private.
        </p>

        <div class="auth-form">
          <div class="form-group">
            <label>{{ isSignInMode ? 'Your Username' : 'Your Auto-Generated Username' }}</label>
            <input 
              type="text" 
              v-model="generatedUsername" 
              :disabled="!isSignInMode" 
              class="auth-input" 
              :class="{ 'disabled-input': !isSignInMode }" 
              placeholder="Enter your username"
            />
          </div>
          <div class="form-group">
            <label>{{ isSignInMode ? 'Your Password' : 'Set a Password' }}</label>
            <input type="password" v-model="password" placeholder="Enter your secure password" class="auth-input" />
          </div>
        </div>

        <div class="action-buttons">
          <button
            class="continue-button"
            type="button"
            :disabled="isGenerating || !password"
            @click="handleAuth"
          >
            {{ isGenerating ? (isSignInMode ? 'Signing In...' : 'Creating Account...') : (isSignInMode ? 'Sign In' : 'Create Account') }}
          </button>
          
          <button class="toggle-mode-button" type="button" @click="isSignInMode = !isSignInMode">
            {{ isSignInMode ? "Need an account? Create one" : "Already have an account? Sign in" }}
          </button>
          
          <button class="guest-button" type="button" @click="handleGuest">
            Continue as Guest
          </button>
        </div>

        <p class="account-note" v-if="!isSignInMode">No email needed. Keep your password safe!</p>
      </div>

      <div v-else class="onboarding-card ready-card">
        <div class="success-icon">✓</div>
        <p class="eyebrow">{{ isSignInMode ? "LOGGED IN" : "ACCOUNT CREATED" }}</p>
        <h1>You’re Ready to Explore!</h1>
        <p class="subtitle">Your anonymous WildDiscover identity is ready.</p>
        <div class="explorer-profile">
          <div class="avatar">E</div>
          <div>
            <strong>{{ explorer?.displayName }}</strong>
            <span>{{ explorer?.level }}</span>
          </div>
        </div>
        <ul class="readiness-list">
          <li><span>✓</span> Journal ready</li>
          <li><span>✓</span> Community ready</li>
          <li><span>✓</span> Contribution points ready</li>
        </ul>
        <button class="continue-button" type="button" @click="startExploring">
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
  font-size: 31px;
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
  font-size: 15px;
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
  font-size: 20px;
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
  font-size: 33px;
}

.feature-item h2 {
  margin-bottom: 8px;
  color: #173d2d;
  font-size: 20px;
  font-weight: 700;
}

.feature-item p {
  margin: 0;
  color: #6d7872;
  font-size: 17px;
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
  font-size: 16px;
}

.protocol-note {
  margin: 36px 0 0;
  color: #929b96;
  font-size: 15px;
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
  font-size: 16px;
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

.auth-form {
  max-width: 320px;
  margin: 0 auto 30px;
  text-align: left;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 16px;
  color: #637069;
  margin-bottom: 6px;
  font-weight: bold;
}
.auth-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dce4df;
  border-radius: 8px;
  font-size: 18px;
}
.disabled-input {
  background: #f5f8f5;
  color: #173d2d;
  font-weight: bold;
}
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}
.guest-button {
  padding: 14px 26px;
  color: #146c4a;
  font-weight: 600;
  background: transparent;
  border: 1px solid #146c4a;
  border-radius: 8px;
  cursor: pointer;
}
.guest-button:hover {
  background: #f5f8f5;
}

</style><style scoped>
.toggle-mode-button {
  background: transparent;
  border: none;
  color: #173d2d;
  font-weight: 500;
  cursor: pointer;
  margin-top: 8px;
  text-decoration: underline;
  font-size: 17px;
}
</style>
