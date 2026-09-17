import { createRouter, createWebHistory } from 'vue-router'

import OnboardingView from '../views/OnboardingView.vue'
import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'
import GalleryView from '../views/GalleryView.vue'
import SightingsView from '../views/SightingsView.vue'
import JournalView from '../views/JournalView.vue'
import ExplorationDetailView from '../views/ExplorationDetailView.vue'
import CompletedExplorationView from '../views/CompletedExplorationView.vue'
import BirdCallChallengeView from '../views/BirdCallChallengeView.vue'
import CommunityView from '../views/CommunityView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/map',
      name: 'map',
      component: MapView
    },
    {
      path: '/gallery',
      name: 'gallery',
      component: GalleryView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/gallery/challenge',
      name: 'bird-call-challenge',
      component: BirdCallChallengeView
    },
    {
      path: '/journal',
      name: 'journal',
      component: JournalView
    },
    {
      path: '/journal/:investigationId/summary',
      name: 'completed-exploration',
      component: CompletedExplorationView
    },
    {
      path: '/journal/:investigationId',
      name: 'exploration-detail',
      component: ExplorationDetailView
    },
    {
      path: '/journal/:investigationId',
      name: 'exploration-detail',
      component: ExplorationDetailView
    },
    {
      path: '/gallery/night-parrot/sightings',
      name: 'sightings',
      component: SightingsView
    }
  ]
})

export default router