import { ref, computed } from 'vue'
import { mockExplorer } from '../mocks/user'

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

  function startExplorerSession() {
    explorer.value = { ...mockExplorer }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(explorer.value))
  }

  function clearExplorerSession() {
    explorer.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    explorer,
    hasExplorerSession,
    startExplorerSession,
    clearExplorerSession
  }
}