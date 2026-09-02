<template>
  <footer class="wild-footer">
    <div class="data-acknowledgements">
      <h2>Data Acknowledgements</h2>

      <p>
        Species occurrence data are sourced from the
        <a
          href="https://www.ala.org.au/biocache/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Atlas of Living Australia (ALA)
        </a>.
        Terrain and environmental data are sourced from the
        <a
          href="https://data.csiro.au/collection/csiro%3A66355"
          target="_blank"
          rel="noopener noreferrer"
        >
          CSIRO 90m Environmental Covariates
        </a>.
      </p>
    </div>

    <div class="footer-inner">
      <div class="footer-brand">
        WildDiscover
      </div>

      <div class="footer-copyright">
        © 2026 WildDiscover. Preserving Australian Biodiversity.
      </div>

      <div class="footer-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">Contact</a>
      </div>
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

  font-size: 15px;
  font-weight: 700;
}

.data-acknowledgements p {
  margin: 0;

  color: #555555;

  font-size: 12px;
  line-height: 1.7;
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
  font-size: 14px;
  font-weight: 700;
}

.footer-copyright {
  color: #146c4a;
  font-size: 12px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.footer-links a {
  color: #333333;
  font-size: 11px;
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
</style>