import re

with open('frontend/src/views/ProfileView.vue', 'r') as f:
    content = f.read()

template_pattern = r'<div class="dashboard-grid">.*?<aside class="side-column">'
new_template = """<div class="dashboard-grid">
        <div class="main-column">
          <section class="dashboard-card level-card" style="position: relative;">
            <h2>
              ⌁ Level Progress
              <span class="tooltip-icon" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">i</span>
              <div class="levels-tooltip" v-if="showTooltip">
                <h4>Level Thresholds</h4>
                <ul>
                  <li v-for="(lvl, idx) in LEVELS" :key="lvl.name">
                    Lvl {{ idx + 1 }} ({{ lvl.name }}): {{ lvl.threshold }}+ pts
                  </li>
                </ul>
              </div>
            </h2>

            <div class="level-row">
              <div>
                <strong>{{ currentLevel.name }}</strong>
                <span>Level {{ currentLevelIndex + 1 }}</span>
              </div>

              <p v-if="nextLevel">
                Next:
                <strong>{{ nextLevel.name }}</strong>
                <span>Level {{ currentLevelIndex + 2 }}</span>
              </p>
              <p v-else>
                <strong>Max Level Reached!</strong>
              </p>
            </div>

            <div
              class="progress-track"
              role="progressbar"
            >
              <div
                class="progress-value"
                :style="{ width: `${levelProgress}%` }"
              ></div>
            </div>

            <div class="progress-details">
              <strong v-if="nextLevel">
                {{ profileData.points }} /
                {{ nextLevel.threshold }} points
                ({{ levelProgress }}%)
              </strong>
              <strong v-else>
                {{ profileData.points }} points (Max!)
              </strong>

              <span v-if="nextLevel">
                {{ pointsRemaining }} points needed to unlock {{ nextLevel.name }} badge.
              </span>
            </div>
          </section>

          <section class="activity-section">
            <h2 class="section-title">⌁ My Planned Trips</h2>

            <div v-if="futureInvestigations.length === 0" style="padding: 1rem; color: #5a7566">
              No planned trips found in the future. Check out the Map to plan a new one!
            </div>
            
            <article v-for="inv in futureInvestigations" :key="inv.id" class="dashboard-card investigation-card">
              <div class="investigation-heading">
                <h3>◎ Upcoming Investigation</h3>
                <span class="planned-badge">● Status: Planned</span>
              </div>

              <div class="investigation-content">
                <div class="bird-image-wrapper">
                  <img
                    :src="inv.image"
                    :alt="inv.commonName"
                  />
                  <em>{{ inv.scientificName }}</em>
                </div>

                <div class="investigation-info">
                  <div class="title-row">
                    <h2>{{ inv.commonName }}</h2>
                    <span class="conservation-badge" style="background-color: #ffcccc; color: #b30000; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;">
                      {{ inv.statusClass }}
                    </span>
                  </div>

                  <div class="details-grid" style="margin-top: 1rem;">
                    <div>
                      <span>Target Zone:</span>
                      <strong>Zone #{{ inv.id }}</strong>
                    </div>

                    <div>
                      <span>Target Date:</span>
                      <strong>{{ inv.exploration_date }}</strong>
                    </div>
                  </div>

                  <p class="description">
                    Planned exploration to search for the {{ inv.commonName }}. Ensure environmental conditions and sensor arrays are ready for the field trip.
                  </p>

                  <div class="card-footer">
                    <RouterLink
                      to="/journal"
                      class="view-journal-link"
                    >
                      View My Journal →
                    </RouterLink>

                    <span class="log-number">Expedition Log #{{ inv.id }}</span>
                  </div>
                </div>
              </div>
            </article>
          </section>
        </div>

        <aside class="side-column">"""
content = re.sub(template_pattern, new_template, content, flags=re.DOTALL)

sidebar_pattern = r'<aside class="side-column">.*?</aside>'
new_sidebar = """<aside class="side-column">
          <section class="dashboard-card rank-card">
            <h2>♜ Community Rank</h2>

            <div class="rank-display">
              <span>NATIONAL POSITION</span>
              <strong>#{{ profileData.rank }}</strong>
              <p>
                Contribution Score:
                <b>{{ profileData.points }} pts</b>
              </p>
              <small>
                Top {{ Math.max(1, Math.round((profileData.rank / profileData.total_users) * 100)) }}% of Active Conservation Observers
              </small>
            </div>
          </section>

          <section class="dashboard-card contribution-card">
            <div class="contribution-heading">
              <h2>◎ Contribution Points</h2>
              <strong>{{ profileData.points }} pts</strong>
            </div>

            <p>
              Points are earned through verified scientific contributions and
              fieldwork.
            </p>

            <ul>
              <li>
                <span>◉ Complete an Exploration</span>
                <strong>+20 pts</strong>
              </li>

              <li>
                <span>▣ Add an Observation</span>
                <strong>+10 pts</strong>
              </li>

              <li>
                <span>♫ Complete Bird Call Challenge</span>
                <strong>+5 pts</strong>
              </li>
            </ul>
          </section>
        </aside>"""
content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)

style_add = """<style scoped>
.tooltip-icon {
  display: inline-block;
  margin-left: 8px;
  background-color: #2b7a54;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 12px;
  line-height: 18px;
  text-align: center;
  cursor: pointer;
  font-weight: bold;
}
.levels-tooltip {
  position: absolute;
  top: 40px;
  left: 20px;
  background-color: #1a231f;
  color: white;
  padding: 12px;
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  min-width: 250px;
}
.levels-tooltip h4 {
  margin: 0 0 8px 0;
  color: #a4ceb3;
  font-size: 0.9rem;
}
.levels-tooltip ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.levels-tooltip li {
  margin-bottom: 4px;
  font-size: 0.85rem;
  font-weight: normal;
}
</style>
"""

content = content + "\n" + style_add

with open('frontend/src/views/ProfileView.vue', 'w') as f:
    f.write(content)

