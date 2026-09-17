<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const rankBadges = {
  1: '🥇',
  2: '🥈',
  3: '🥉'
}

const leaderboardUsers = ref([])

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/leaderboard`)
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
</script>

<template>
  <aside class="leaderboard">
    <header class="leaderboard-header">
      <div>
        <div class="title-row">
          <h2>Top Conservation Scouts</h2>
          <span class="top-badge">Top 10</span>
        </div>

        <p>Rankings based on verified exploration contributions.</p>
      </div>

      <div class="trophy" aria-hidden="true">🏆</div>
    </header>

    

    <ol class="ranking-list">
      <li
        v-for="(user, index) in leaderboardUsers"
        :key="user.id"
        class="ranking-item"
        :class="{ 'top-three': (index + 1) <= 3 }"
      >
        <div
          class="rank-number"
          :class="`rank-${index + 1}`"
          :aria-label="`Rank ${index + 1}`"
        >
          {{ getRankBadge(index + 1) }}
        </div>

        <div class="explorer-avatar">
          {{ user.username ? user.username.slice(-2).toUpperCase() : "??" }}
        </div>

        <div class="explorer-details">
          <strong>{{ user.username }}</strong>
          <span>Explorer</span>
        </div>

        <strong class="points">
          {{ user.points.toLocaleString() }} pts
        </strong>
      </li>
    </ol>

    
  </aside>
</template>

<style scoped>
.leaderboard {
  position: sticky;
  top: 95px;
  overflow: hidden;
  border: 1px solid #e0e8e3;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 6px 22px rgb(25 68 48 / 6%);
}

.leaderboard-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 20px 18px 10px;
}

.title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.title-row h2 {
  margin: 0;
  color: #244336;
  font-size: 20px;
}

.top-badge {
  padding: 4px 8px;
  border-radius: 14px;
  background: #e5f7ed;
  color: #267a57;
  font-size: 12px;
  font-weight: 800;
}

.leaderboard-header p {
  margin: 7px 0 0;
  color: #7a8881;
  font-size: 13px;
  line-height: 1.4;
}

.trophy {
  display: grid;
  flex: 0 0 38px;
  width: 38px;
  height: 38px;
  place-items: center;
  border-radius: 10px;
  background: #fff4d8;
  font-size: 21px;
}

.update-label {
  margin: 0;
  padding: 0 18px 13px;
  color: #4a6658;
  font-size: 13px;
  font-weight: 700;
}

.info {
  display: inline-grid;
  width: 15px;
  height: 15px;
  place-items: center;
  border: 1px solid #9fb1a7;
  border-radius: 50%;
  color: #698076;
  cursor: help;
}

.ranking-list {
  display: grid;
  gap: 5px;
  margin: 0;
  padding: 0 12px 14px;
  list-style: none;
}

.ranking-item {
  display: grid;
  grid-template-columns: 28px 31px minmax(0, 1fr) auto;
  align-items: center;
  gap: 8px;
  min-height: 47px;
  padding: 7px 8px;
  border-radius: 9px;
  background: #fafbfa;
}

.ranking-item.top-three {
  border: 1px solid #f0dfad;
  background: #fffaf0;
}

.rank-number {
  display: grid;
  width: 25px;
  height: 25px;
  place-items: center;
  border-radius: 50%;
  background: #eef1ef;
  color: #56675f;
  font-size: 13px;
  font-weight: 800;
}

.rank-1,
.rank-2,
.rank-3 {
  background: transparent;
  font-size: 20px;
}

.explorer-avatar {
  display: grid;
  width: 31px;
  height: 31px;
  place-items: center;
  border-radius: 50%;
  background: #e2eee8;
  color: #277a56;
  font-size: 12px;
  font-weight: 800;
}

.explorer-details {
  display: grid;
  min-width: 0;
  gap: 2px;
}

.explorer-details strong {
  overflow: hidden;
  color: #2c4539;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.explorer-details span {
  overflow: hidden;
  color: #849088;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.points {
  color: #294b3c;
  font-size: 12px;
  white-space: nowrap;
}

.current-user-section {
  padding: 14px;
  border-top: 1px solid #e1e8e4;
  background: #f6faf7;
}

.current-user-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 9px;
  color: #307a59;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.07em;
}

.percentile {
  padding: 4px 8px;
  border-radius: 12px;
  background: #d9f5e5;
  letter-spacing: normal;
}

.current-user-card {
  display: grid;
  grid-template-columns: 28px 32px minmax(0, 1fr) auto;
  align-items: center;
  gap: 8px;
  padding: 10px;
  border: 1px solid #bbdfcc;
  border-radius: 9px;
  background: white;
}

.current-rank {
  color: #225d43;
  font-size: 14px;
  font-weight: 900;
}

.current-avatar {
  background: #ccebd9;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 12px;
  color: #5e7067;
  font-size: 11px;
}

.progress-track {
  height: 6px;
  margin-top: 7px;
  overflow: hidden;
  border-radius: 12px;
  background: #d9e5df;
}

.progress-value {
  height: 100%;
  border-radius: inherit;
  background: #26805a;
}

.points-needed {
  margin: 7px 0 0;
  color: #809087;
  font-size: 11px;
  text-align: right;
}

@media (max-width: 900px) {
  .leaderboard {
    position: static;
  }
}
</style>