<template>
  <footer class="wild-footer">
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
}
</style>