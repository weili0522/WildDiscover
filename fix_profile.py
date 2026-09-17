import re

with open('frontend/src/views/ProfileView.vue', 'r') as f:
    content = f.read()

# Replace script setup
script_pattern = r'<script setup>.*?</script>'
new_script = """<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExplorer } from '../composables/useExplorer'
import { gallerySpecies } from '../mocks/gallery'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import malleefowlImage from '../assets/malleefowl.jpg'
import duskyGrasswrenImage from '../assets/dusky-grasswren.jpg'

const imageMap = {
  'night-parrot.jpg': nightParrotImage,
  'princess-parrot.jpg': princessParrotImage,
  'plains-wanderer.jpg': plainsWandererImage,
  'rufous-scrub-bird.jpg': rufousScrubBirdImage,
  'malleefowl.jpg': malleefowlImage,
  'dusky-grasswren.jpg': duskyGrasswrenImage
}

const router = useRouter()
const { explorer, hasExplorerSession } = useExplorer()

const profileData = ref({
  points: 0,
  rank: 0,
  total_users: 1,
  investigations: []
})

const displayName = computed(() => explorer.value?.displayName || 'Guest')
const explorerId = computed(() => explorer.value?.id?.toUpperCase() || 'EXP-GUEST')

const LEVELS = [
  { name: 'Novice Observer', threshold: 0 },
  { name: 'Field Enthusiast', threshold: 100 },
  { name: 'Conservation Scout', threshold: 300 },
  { name: 'Species Tracker', threshold: 600 },
  { name: 'Master Ecologist', threshold: 1000 }
]

const currentLevelIndex = computed(() => {
  const pts = profileData.value.points
  let idx = 0
  for (let i = 0; i < LEVELS.length; i++) {
    if (pts >= LEVELS[i].threshold) idx = i
  }
  return idx
})

const currentLevel = computed(() => LEVELS[currentLevelIndex.value])
const nextLevel = computed(() => {
  return currentLevelIndex.value < LEVELS.length - 1 
    ? LEVELS[currentLevelIndex.value + 1] 
    : null
})

const levelProgress = computed(() => {
  if (!nextLevel.value) return 100
  const currentThreshold = currentLevel.value.threshold
  const nextThreshold = nextLevel.value.threshold
  const pointsIntoLevel = profileData.value.points - currentThreshold
  const pointsRequired = nextThreshold - currentThreshold
  return Math.min(Math.round((pointsIntoLevel / pointsRequired) * 100), 100)
})

const pointsRemaining = computed(() => {
  if (!nextLevel.value) return 0
  return Math.max(nextLevel.value.threshold - profileData.value.points, 0)
})

// Filter investigations to only show future ones
const futureInvestigations = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  return profileData.value.investigations
    .filter(inv => {
      const invDate = new Date(inv.exploration_date)
      return invDate >= today
    })
    .map(inv => {
      // Find species info
      const species = gallerySpecies.find(s => s.id === inv.species_id)
      return {
        ...inv,
        commonName: species ? species.name : 'Unknown Bird',
        scientificName: species ? species.scientificName : '',
        statusClass: species ? species.statusClass : 'Endangered',
        image: species ? imageMap[species.image] : nightParrotImage
      }
    })
})

const showTooltip = ref(false)

onMounted(async () => {
  if (!hasExplorerSession.value) return
  
  try {
    const res = await fetch(`http://localhost:8000/api/v1/profile/${explorer.value.displayName}`)
    if (res.ok) {
      profileData.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to fetch profile', e)
  }
})
</script>"""
content = re.sub(script_pattern, new_script, content, flags=re.DOTALL)

with open('frontend/src/views/ProfileView.vue', 'w') as f:
    f.write(content)
