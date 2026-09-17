<script setup>
import { ref } from 'vue'

const showAcknowledgements = ref(false)
</script>

<template>
  <footer class="wild-footer">
    <div v-show="showAcknowledgements" class="data-acknowledgements">
      <h2>Data Acknowledgements</h2>

      <p>
        <strong>Habitat &amp; Environment Data:</strong> Species occurrence data are sourced from the
        <a href="https://www.ala.org.au/biocache/" target="_blank" rel="noopener noreferrer">Atlas of Living Australia (ALA)</a>.
        Terrain and environmental data are sourced from the
        <a href="https://data.csiro.au/collection/csiro%3A66355" target="_blank" rel="noopener noreferrer">CSIRO 90m Environmental Covariates</a>
        and <a href="https://data.csiro.au/collection/csiro:65549" target="_blank" rel="noopener noreferrer">CSIRO HCAS data</a>.
      </p>

      <p>
        <strong>Viewing Points:</strong> Map viewing points are sourced via
        <a href="https://www.openstreetmap.org/" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> and
        <a href="https://overpass-turbo.eu/" target="_blank" rel="noopener noreferrer">Overpass Turbo</a>.
      </p>

      <p>
        <strong>Bird Audio (<a href="https://xeno-canto.org/" target="_blank" rel="noopener noreferrer">Xeno-canto</a>, CC BY-NC-SA 4.0):</strong> All audio clips edited to 10 seconds.
      </p>
      <ul class="audio-credits">
        <li><a href="https://xeno-canto.org/380407" target="_blank" rel="noopener noreferrer">Night Parrot call</a> — Nigel Jackett, XC380407</li>
        <li><a href="https://xeno-canto.org/488068" target="_blank" rel="noopener noreferrer">Princess Parrot flight call</a> — Mark Carter, XC488068</li>
        <li><a href="https://xeno-canto.org/1024916" target="_blank" rel="noopener noreferrer">Plains-wanderer dawn song</a> — Gregor Smith, XC1024916</li>
        <li><a href="https://xeno-canto.org/884279" target="_blank" rel="noopener noreferrer">Rufous Scrub-bird song</a> — Remco Hofland, XC884279</li>
        <li><a href="https://xeno-canto.org/679740" target="_blank" rel="noopener noreferrer">Malleefowl</a> — XC679740</li>
        <li><a href="https://xeno-canto.org/642677" target="_blank" rel="noopener noreferrer">Dusky Grasswren call/song</a> — Christopher Watson, XC642677</li>
      </ul>
    </div>

    <div class="footer-inner">
      <div class="footer-brand" style="flex: 1;">
        WildDiscover
      </div>
      
      <div style="flex: 1; display: flex; justify-content: center;">
        <button class="footer-ack-btn" @click="showAcknowledgements = !showAcknowledgements">
          Data Acknowledgements
        </button>
      </div>
      
      <div style="flex: 1;"></div>
    </div>
  </footer>
</template>

<style scoped>
.wild-footer {
  background-color: #ffffff;
  border-top: 1px solid #eeeeee;
}

.data-acknowledgements {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px 40px 20px;

  text-align: center;

  border-bottom: 1px solid #eeeeee;
}

.data-acknowledgements h2 {
  margin: 0 0 10px;

  color: #146c4a;

  font-size: 18px;
  font-weight: 700;
}


.data-acknowledgements p {
  margin: 0 0 10px;
  color: #555555;
  font-size: 15px;
  line-height: 1.7;
}

.data-acknowledgements strong {
  color: #333333;
}

.audio-credits {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.audio-credits li {
  font-size: 14px;
  color: #555;
  background: #f7f9f7;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #eeeeee;
}


.data-acknowledgements a {
  color: #146c4a;
  font-weight: 600;
  text-decoration: underline;
}

.data-acknowledgements a:hover {
  color: #0e5037;
}

.footer-inner {
  min-height: 86px;
  padding: 0 40px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 30px;
}

.footer-brand {
  color: #146c4a;
  font-size: 17px;
  font-weight: 700;
}

.footer-copyright {
  color: #146c4a;
  font-size: 15px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.footer-links a {
  color: #333333;
  font-size: 14px;
  text-decoration: none;
}

.footer-links a:hover {
  color: #146c4a;
}

@media (max-width: 768px) {
  .footer-inner {
    padding: 24px 20px;
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .footer-links {
    gap: 16px;
  }

  .data-acknowledgements {
  padding: 22px 20px;
  }
}

.footer-ack-btn {
  background: transparent;
  border: none;
  color: #555;
  font-size: 15px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 20px;
  transition: background 0.2s;
}

.footer-ack-btn:hover {
  background: #f0f4f2;
  color: #146c4a;
}

</style>