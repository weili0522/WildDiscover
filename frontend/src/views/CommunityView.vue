<script setup>
import NewsFeed from '../components/NewsFeed.vue'
import LeaderboardView from '../components/LeaderboardView.vue'
</script>

<template>
  <main class="community-page">
    <div class="community-container">
      <header class="community-header">
        <p class="eyebrow">COMMUNITY CONSERVATION NETWORK</p>

        <h1>Conservation News</h1>

        <p>
          Stay updated with recent bird rediscoveries, habitat research and
          conservation news from trusted sources.
        </p>
      </header>

      <div class="community-layout">
        <NewsFeed />
        <LeaderboardView />
      </div>
    </div>
  </main>
</template>

<style scoped>
.community-page {
  min-height: calc(100vh - 80px);
  padding: 48px 24px 80px;
  background: #fbfcfa;
  color: #193f30;
}

.community-container {
  width: min(1180px, 100%);
  margin: 0 auto;
}

.community-header {
  margin-bottom: 30px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2b825d;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.09em;
}

.community-header h1 {
  margin: 0 0 9px;
  color: #173f2f;
  font-size: clamp(34px, 4vw, 48px);
  line-height: 1.05;
}

.community-header > p:last-child {
  max-width: 680px;
  margin: 0;
  color: #69776f;
  font-size: 14px;
  line-height: 1.55;
}

.community-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: 24px;
  align-items: start;
}

@media (max-width: 900px) {
  .community-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .community-page {
    padding: 32px 15px 60px;
  }

  .community-header {
    margin-bottom: 22px;
  }
}
</style>