<template>
  <nav class="navbar navbar-expand-lg bg-white wild-navbar">
    <div class="container-fluid px-4 px-lg-5">

      <!-- Logo -->
      <RouterLink class="navbar-brand" to="/">
        WildDiscover
      </RouterLink>

      <!-- Mobile button -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#wildNavbar"
        aria-controls="wildNavbar"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation -->
      <div class="collapse navbar-collapse" id="wildNavbar">
        <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-4">

          <li class="nav-item">
            <RouterLink
              to="/map"
              class="nav-link"
            >
              Map
            </RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink
              to="/gallery"
              class="nav-link"
            >
              Gallery
            </RouterLink>
          </li>

        </ul>
      </div>

    </div>
  </nav>
</template>

<style scoped>
.wild-navbar {
  min-height: 70px;
  border-bottom: 1px solid #eeeeee;
}

.navbar-brand {
  color: #146c4a;
  font-size: 24px;
  font-weight: 700;
  text-decoration: none;
}

.navbar-brand:hover {
  color: #146c4a;
}

.nav-link {
  position: relative;
  color: #333333;
  font-size: 15px;
  font-weight: 500;
  padding: 23px 0 18px !important;
}

.nav-link:hover {
  color: #146c4a;
}

/* Active route */
.nav-link.router-link-active {
  color: #146c4a;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;

  left: 0;
  right: 0;
  bottom: 10px;

  height: 2px;
  background-color: #146c4a;
}
</style>