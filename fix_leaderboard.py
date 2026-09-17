import re

with open('frontend/src/components/LeaderboardView.vue', 'r') as f:
    content = f.read()

script_pattern = r'<script setup>.*?</script>'
new_script = """<script setup>
import { ref, onMounted } from 'vue'

const rankBadges = {
  1: '🥇',
  2: '🥈',
  3: '🥉'
}

const leaderboardUsers = ref([])

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/v1/leaderboard')
    if (res.ok) {
      leaderboardUsers.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to fetch leaderboard', e)
  }
})

function getRankBadge(rank) {
  return rankBadges[rank] || rank
}
</script>"""

content = re.sub(script_pattern, new_script, content, flags=re.DOTALL)

# Template updates
content = content.replace("v-for=\"user in leaderboardData.users\"", "v-for=\"(user, index) in leaderboardUsers\"")
content = content.replace(":key=\"user.displayName\"", ":key=\"user.id\"")
content = content.replace("user.rank <= 3", "(index + 1) <= 3")
content = content.replace("getRankBadge(user.rank)", "getRankBadge(index + 1)")
content = content.replace("user.displayName", "user.username")

# We can remove the level and progress bar since the backend only returns points (unless we calculate it on frontend, but it's okay to just show points)
# Actually, let's keep the template simple. 

template_level_pattern = r'<div class="scout-progress">.*?</div>'
new_level = """<div class="scout-progress" style="display: flex; align-items: center; justify-content: space-between;">
            <div class="score-display">
              <strong>{{ user.points }}</strong>
              <span>pts</span>
            </div>
          </div>"""
content = re.sub(template_level_pattern, new_level, content, flags=re.DOTALL)

with open('frontend/src/components/LeaderboardView.vue', 'w') as f:
    f.write(content)
