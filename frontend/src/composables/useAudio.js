import { ref, onUnmounted } from 'vue'

const currentlyPlayingId = ref(null)
const currentTime = ref(0)
const duration = ref(0)
let currentAudioElement = null

export function useAudio() {
  function stopAudio() {
    if (currentAudioElement) {
      currentAudioElement.pause()
      currentAudioElement.currentTime = 0
      currentAudioElement = null
    }
    currentlyPlayingId.value = null
    currentTime.value = 0
    duration.value = 0
  }

  function playAudio(speciesId) {
    if (currentlyPlayingId.value === speciesId) {
      stopAudio()
      return
    }

    stopAudio()

    currentlyPlayingId.value = speciesId
    currentAudioElement = new Audio(`/audio/${speciesId}.mp3`)
    
    currentAudioElement.addEventListener('loadedmetadata', () => {
      duration.value = currentAudioElement.duration
    })
    
    currentAudioElement.addEventListener('timeupdate', () => {
      currentTime.value = currentAudioElement.currentTime
    })

    currentAudioElement.play().catch(e => {
      console.error('Audio playback failed', e)
      currentlyPlayingId.value = null
    })

    currentAudioElement.addEventListener('ended', () => {
      currentlyPlayingId.value = null
      currentAudioElement = null
      currentTime.value = 0
    })
  }

  return {
    currentlyPlayingId,
    currentTime,
    duration,
    playAudio,
    stopAudio
  }
}
