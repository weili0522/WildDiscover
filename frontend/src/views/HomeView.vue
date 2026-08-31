<template>
  <div class="home-page">

    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-overlay"></div>

      <div class="hero-content">
        <h1>
          Discover Australia's Biodiversity
          <br />
          Around You
        </h1>

        <p>
          Explore predicted habitats, track climate-displaced species,
          and support biodiversity discovery.
        </p>

        <div class="hero-buttons">
          <RouterLink to="/map" class="btn btn-map">
             Explore Map
          </RouterLink>

          <RouterLink to="/gallery" class="btn btn-gallery">
             View Gallery
          </RouterLink>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.hero-section {
  position: relative;
  min-height: calc(100vh - 140px);
  background-image: url('../assets/hero.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* dark layer over image */
.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.38);
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  max-width: 760px;
  padding: 20px;
}

.hero-content h1 {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.05;
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 18px;
  line-height: 1.5;
  max-width: 650px;
  margin: 0 auto 30px;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.hero-buttons .btn {
  min-width: 150px;
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: 500;
}

.btn-map {
  background-color: #146c4a;
  color: white;
  border: none;
}

.btn-map:hover {
  background-color: #0f573c;
  color: white;
}

.btn-gallery {
  background-color: white;
  color: #333;
  border: none;
}

.btn-gallery:hover {
  background-color: #f1f1f1;
  color: #146c4a;
}
</style>