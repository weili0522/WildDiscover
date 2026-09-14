<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-overlay"></div>

      <div class="hero-content">
        <h1>
          Discover Australia’s Rare and
          <br>
          Lost Birds
        </h1>

        <p>
          Explore predicted habitats, learn about endangered birds and plan
          your own bird exploration journey.
        </p>

        <RouterLink to="/map" class="hero-button">
          Explore Map
          <span>→</span>
        </RouterLink>
      </div>
    </section>

    <!-- Feature cards -->
    <section class="explore-section">
      <div class="section-heading">
        <h2>Explore WildDiscover</h2>
        <p>Everything you need to discover, learn and explore.</p>
      </div>

      <div class="feature-grid">
        <!-- Map -->
        <article class="feature-card">
          <div class="feature-icon icon-green">◫</div>

          <h3>Habitat Predictive Map</h3>

          <p>
            Interactive GIS heatmaps modelling climate, vegetation, and
            historical encounters across Australia.
          </p>

          <div class="map-preview">
            <span class="suitability-label">● High Suitability: 84%</span>

            <div class="map-preview-text">
              <small>CONTOUR · PILBARA REGION</small>
              <strong>Triodia Spinifex Grassland</strong>
            </div>
          </div>

          <RouterLink to="/map" class="card-link">
            Explore Map
            <span>→</span>
          </RouterLink>
        </article>

        <!-- Gallery -->
        <article class="feature-card">
          <div class="feature-icon icon-orange">▣</div>

          <h3>Native Bird Gallery</h3>

          <p>
            High-resolution portraits, audio call spectrograms, and plumage
            identifiers for rare endemic species.
          </p>

          <div class="bird-preview">
            <span class="danger-label">CRITICALLY ENDANGERED</span>

            <div class="bird-preview-footer">
              <strong>Night Parrot</strong>
              <span>♬ Listen to Call</span>
            </div>
          </div>

          <RouterLink to="/gallery" class="card-link">
            Explore Birds
            <span>→</span>
          </RouterLink>
        </article>

        <!-- Journal -->
        <article class="feature-card">
          <div class="feature-icon icon-blue">▤</div>

          <h3>Investigation Journal</h3>

          <p>
            Log private coordinates, field audio, and sighting notes directly
            on your device with complete privacy.
          </p>

          <div class="journal-preview">
            <div class="journal-heading">
              <div>
                <strong>Pilbara Sector 4</strong>
                <small>2 Observations recorded</small>
              </div>

              <span>Active Zone</span>
            </div>

            <div class="guest-warning">
              ◉ Guest activity is temporary · Generate ID to save permanently
            </div>
          </div>

          <RouterLink to="/journal" class="card-link">
            View Journal
            <span>→</span>
          </RouterLink>
        </article>

        <!-- News -->
        <article class="feature-card">
          <div class="feature-icon icon-mint">⌁</div>

          <h3>Conservation News</h3>

          <p>
            Follow real-time habitat updates, community survey milestones,
            and anonymous conservation leaderboards.
          </p>

          <div class="news-preview">
            <small>BULLETIN · 2 HRS AGO</small>

            <strong>
              Plains-wanderer habitat suitability model updated
            </strong>

            <div class="news-footer">
              <span>Top Scout:</span>
              <b>Explorer_1203 (1,480 pts)</b>
            </div>
          </div>

          <RouterLink to="/community" class="card-link">
            Read News
            <span>→</span>
          </RouterLink>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  color: #1f382d;
  background: #f8faf8;
}

.hero-section {
  position: relative;
  display: flex;
  min-height: 520px;
  align-items: center;
  justify-content: center;
  background-image: url('../assets/hero.jpg');
  background-position: center;
  background-size: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(8, 30, 20, 0.43);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
  padding: 30px 20px;
  color: #ffffff;
  text-align: center;
}

.hero-content h1 {
  margin-bottom: 16px;
  font-size: clamp(38px, 5vw, 58px);
  font-weight: 700;
  line-height: 1.05;
}

.hero-content p {
  max-width: 620px;
  margin: 0 auto 26px;
  font-size: 17px;
  line-height: 1.45;
}

.hero-button {
  display: inline-flex;
  padding: 13px 25px;
  color: #ffffff;
  font-weight: 600;
  text-decoration: none;
  align-items: center;
  gap: 14px;
  background: #175c42;
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 28px;
}

.hero-button:hover {
  color: #ffffff;
  background: #104934;
}

.explore-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 72px 34px 110px;
}

.section-heading {
  margin-bottom: 46px;
  text-align: center;
}

.section-heading h2 {
  margin-bottom: 8px;
  color: #174d38;
  font-size: 34px;
  font-weight: 700;
}

.section-heading p {
  margin: 0;
  color: #626e68;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 24px;
}

.feature-card {
  display: flex;
  min-width: 0;
  padding: 25px;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e0e6e2;
  border-radius: 14px;
  box-shadow: 0 3px 10px rgba(32, 69, 51, 0.04);
}

.feature-icon {
  display: grid;
  width: 44px;
  height: 44px;
  margin-bottom: 20px;
  font-size: 20px;
  place-items: center;
  border-radius: 50%;
}

.icon-green {
  color: #205a43;
  background: #e5f0ea;
}

.icon-orange {
  color: #e4803f;
  background: #fff0e5;
}

.icon-blue {
  color: #267393;
  background: #e5f2f7;
}

.icon-mint {
  color: #2f9b70;
  background: #e3f5ec;
}

.feature-card h3 {
  margin-bottom: 11px;
  color: #174d38;
  font-size: 20px;
  font-weight: 700;
}

.feature-card > p {
  min-height: 88px;
  margin-bottom: 16px;
  color: #5e6963;
  font-size: 13px;
  line-height: 1.55;
}

.map-preview,
.bird-preview,
.journal-preview,
.news-preview {
  min-height: 130px;
  margin-bottom: 18px;
  overflow: hidden;
  border: 1px solid #e0e4e1;
  border-radius: 10px;
}

.map-preview {
  position: relative;
  display: flex;
  padding: 13px;
  align-items: flex-end;
  background:
    linear-gradient(rgba(241, 211, 190, 0.68), rgba(239, 221, 202, 0.75)),
    radial-gradient(circle at 25% 30%, #ddae8e, transparent 35%),
    #f2ded0;
}

.suitability-label {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 7px;
  color: #277854;
  font-size: 9px;
  font-weight: 700;
  background: #ffffff;
  border-radius: 8px;
}

.map-preview-text small,
.map-preview-text strong {
  display: block;
}

.map-preview-text small {
  margin-bottom: 4px;
  color: #50685c;
  font-size: 8px;
  letter-spacing: 0.08em;
}

.map-preview-text strong {
  font-size: 12px;
}

.bird-preview {
  position: relative;
  background:
    linear-gradient(to top, rgba(0, 0, 0, 0.75), transparent 55%),
    url('../assets/night-parrot.jpg') center/cover;
}

.danger-label {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 6px;
  color: #ffffff;
  font-size: 8px;
  font-weight: 700;
  background: #d94848;
  border-radius: 3px;
}

.bird-preview-footer {
  position: absolute;
  right: 10px;
  bottom: 10px;
  left: 10px;
  display: flex;
  color: #ffffff;
  font-size: 10px;
  align-items: center;
  justify-content: space-between;
}

.journal-preview,
.news-preview {
  padding: 14px;
  background: #f6f7f5;
}

.journal-heading {
  display: flex;
  margin-bottom: 22px;
  align-items: flex-start;
  justify-content: space-between;
}

.journal-heading strong,
.journal-heading small {
  display: block;
}

.journal-heading strong {
  font-size: 11px;
}

.journal-heading small {
  margin-top: 4px;
  color: #69746e;
  font-size: 9px;
}

.journal-heading > span {
  padding: 4px 6px;
  color: #27865b;
  font-size: 8px;
  background: #dff3e8;
  border-radius: 4px;
}

.guest-warning {
  padding: 10px;
  color: #795638;
  font-size: 9px;
  line-height: 1.4;
  background: #fff0e4;
  border: 1px solid #efc9a8;
  border-radius: 7px;
}

.news-preview > small {
  display: block;
  margin-bottom: 12px;
  color: #36a06f;
  font-size: 8px;
  font-weight: 700;
}

.news-preview > strong {
  display: block;
  min-height: 45px;
  font-size: 10px;
  line-height: 1.45;
}

.news-footer {
  display: flex;
  margin-top: 10px;
  padding-top: 10px;
  font-size: 8px;
  justify-content: space-between;
  border-top: 1px solid #dfe4e0;
}

.card-link {
  display: flex;
  margin-top: auto;
  padding: 11px 13px;
  color: #24543f;
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
  align-items: center;
  justify-content: space-between;
  background: #eef1ee;
  border-radius: 8px;
}

.card-link:hover {
  color: #ffffff;
  background: #245c47;
}

@media (max-width: 1100px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 650px) {
  .hero-section {
    min-height: 460px;
  }

  .hero-content h1 {
    font-size: 38px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .explore-section {
    padding: 52px 18px 72px;
  }

  .feature-card > p {
    min-height: auto;
  }
}
</style>