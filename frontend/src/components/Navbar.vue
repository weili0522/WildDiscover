<script setup>
import { useRouter } from 'vue-router'
import { useExplorer } from '../composables/useExplorer'

const router = useRouter()
const { explorer, hasExplorerSession, clearExplorerSession } = useExplorer()

function handleLogout() {
  clearExplorerSession()
  router.push('/')
}
</script>

<template>
  <header>
    <!-- Guest information banner -->
    <div v-if="!hasExplorerSession" class="guest-banner">
      <div class="container-fluid px-4 px-lg-5 banner-content">
        <span>
          ◇ You are currently browsing as a guest. Your local explorations
          are stored only on this device. Generate an Anonymous ID anytime
          to keep them permanently.
        </span>

        <button
          class="banner-close"
          type="button"
          aria-label="Close notice"
        >
          ×
        </button>
      </div>
    </div>

    <nav class="navbar navbar-expand-lg bg-white wild-navbar">
      <div class="container-fluid px-4 px-lg-5">
        <RouterLink class="navbar-brand" to="/">
          WildDiscover
        </RouterLink>

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

        <div id="wildNavbar" class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-4">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">
                Home
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/map" class="nav-link">
                Map
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/gallery" class="nav-link">
                Gallery
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/journal" class="nav-link">
                Journal
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink to="/community" class="nav-link">
                Community
              </RouterLink>
            </li>

            <!-- Guest identity control -->
            <li
              v-if="!hasExplorerSession"
              class="identity-control guest-control"
            >
              <span class="guest-status">
                <span class="status-dot"></span>
                Browsing as Guest
              </span>

              <RouterLink
                to="/onboarding"
                class="generate-button"
              >
                ◇ Generate Anonymous ID
              </RouterLink>
            </li>

            <!-- Generated explorer identity -->
            <li v-else class="identity-control explorer-control">
              <span class="status-dot"></span>
              <span>{{ explorer?.displayName }}</span>
            </li>

            <li v-if="hasExplorerSession" class="nav-item">
              <button class="nav-link logout-btn" @click="handleLogout">
                Logout
              </button>
            </li>

            <li class="nav-item">
              <RouterLink
                to="/profile"
                class="profile-icon"
                aria-label="Open explorer profile"
                title="My Explorer Profile"
              >
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
                  <path d="M4.5 20c.7-4 3.2-6 7.5-6s6.8 2 7.5 6" />
                </svg>
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.guest-banner {
  color: #ffffff;
  background: #245c47;
}

.banner-content {
  position: relative;
  display: flex;
  min-height: 48px;
  padding-top: 10px;
  padding-bottom: 10px;
  font-size: 16px;
  line-height: 1.5;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.banner-content > span {
  max-width: 920px;
}

.banner-close {
  position: absolute;
  right: 24px;
  color: #dce9e3;
  font-size: 25px;
  line-height: 1;
  background: transparent;
  border: 0;
}

.wild-navbar {
  min-height: 70px;
  border-bottom: 1px solid #eeeeee;
}

.navbar-brand {
  color: #146c4a;
  font-size: 27px;
  font-weight: 700;
  text-decoration: none;
}

.navbar-brand:hover {
  color: #146c4a;
}

.nav-link {
  position: relative;
  color: #333333;
  font-size: 18px;
  font-weight: 500;
  padding: 23px 0 18px !important;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #146c4a;
}

.nav-link.router-link-active::after {
  position: absolute;
  right: 0;
  bottom: 10px;
  left: 0;
  height: 2px;
  content: '';
  background: #146c4a;
}

.identity-control {
  display: flex;
  min-height: 38px;
  padding: 4px;
  align-items: center;
  border: 1px solid #dce4df;
  border-radius: 22px;
}

.guest-status {
  display: flex;
  padding: 0 10px;
  color: #68736d;
  font-size: 15px;
  align-items: center;
  gap: 7px;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  background: #54c48a;
  border-radius: 50%;
}

.generate-button {
  padding: 7px 14px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  background: #245c47;
  border-radius: 18px;
}

.generate-button:hover {
  color: #ffffff;
  background: #174936;
}

.explorer-control {
  padding: 8px 14px;
  color: #245c47;
  font-size: 16px;
  font-weight: 600;
  gap: 8px;
}

.profile-icon {
  display: inline-flex;
  flex: 0 0 46px;
  width: 46px;
  height: 46px;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 50%;
  background: #176b48;
  color: #ffffff;
  text-decoration: none;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.profile-icon svg {
  display: block;
  width: 23px;
  height: 23px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.profile-icon:hover {
  color: #ffffff;
  background: #0f5739;
  transform: translateY(-1px);
}

.profile-icon.router-link-active {
  color: #ffffff;
  box-shadow: 0 0 0 3px rgb(66 177 127 / 22%);
}

@media (max-width: 991px) {
  .navbar-nav {
    padding: 16px 0;
    align-items: stretch !important;
  }

  .nav-link {
    padding: 10px 0 !important;
  }

  .nav-link.router-link-active::after {
    display: none;
  }

  .identity-control {
    margin-top: 10px;
    justify-content: space-between;
  }

  .profile-icon {
    margin-top: 10px;
  }
}
</style><style scoped>
.logout-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
}
</style>
