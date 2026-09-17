import re

with open('frontend/src/views/BirdCallChallengeView.vue', 'r') as f:
    content = f.read()

# Add useExplorer
content = content.replace("import { useAudio } from '../composables/useAudio'", "import { useAudio } from '../composables/useAudio'\nimport { useExplorer } from '../composables/useExplorer'")
content = content.replace("const { currentlyPlayingId", "const { explorer } = useExplorer()\nconst { currentlyPlayingId")

submit_pattern = r'function submitAnswer\(\) \{\n  if \(!selectedAnswer.value\) return\n  submitted.value = true\n  // Let the full soundscape play if they want, or we can stop it. Let\'s keep it playing.\n\}'
new_submit = """async function submitAnswer() {
  if (!selectedAnswer.value) return
  submitted.value = true
  
  if (isCorrect.value && explorer.value) {
    try {
      await fetch('http://localhost:8000/api/v1/challenge/success', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: explorer.value.displayName })
      })
    } catch (e) {
      console.error('Failed to save challenge points', e)
    }
  }
}"""
content = re.sub(submit_pattern, new_submit, content)

with open('frontend/src/views/BirdCallChallengeView.vue', 'w') as f:
    f.write(content)
