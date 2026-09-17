import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const STORAGE_KEY = 'wilddiscover_explorer'

function loadExplorer() {
  try {
    const savedExplorer = localStorage.getItem(STORAGE_KEY)
    return savedExplorer ? JSON.parse(savedExplorer) : null
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return null
  }
}

const explorer = ref(loadExplorer())

export function useExplorer() {
  const hasExplorerSession = computed(() => explorer.value !== null)
  const isGuest = computed(() => !explorer.value || explorer.value.isGuest === true)


  async function login(username, password) {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      if (!res.ok) throw new Error('Auth failed')
      const data = await res.json()
      explorer.value = {
        id: `explorer-${Math.floor(Math.random() * 10000)}`,
        displayName: username,
        level: 'Novice Explorer',
        points: 0,
        isGuest: false,
        token: data.access_token
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(explorer.value))
    } catch (e) {
      console.error('Login error', e)
      throw e
    }
  }

  async function registerAndLogin(username, password) {

    try {
      // Mock hitting backend register
      const regRes = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      if (!regRes.ok) throw new Error('Registration failed')

      // Mock hitting backend login
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      if (!res.ok) throw new Error('Auth failed')
      const data = await res.json()

      explorer.value = {
        id: `explorer-${Math.floor(Math.random() * 10000)}`,
        displayName: username,
        level: 'Novice Explorer',
        points: 0,
        isGuest: false,
        token: data.access_token
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(explorer.value))
    } catch (e) {
      console.error('Auth error', e)
    }
  }

  function startGuestSession() {
    explorer.value = {
      id: 'guest',
      displayName: 'Guest Explorer',
      level: 'Observer',
      points: 0,
      isGuest: true
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(explorer.value))
  }

  function clearExplorerSession() {
    explorer.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    explorer,
    hasExplorerSession,
    isGuest,
    registerAndLogin,
    login,
    startGuestSession,
    clearExplorerSession
  }
}
