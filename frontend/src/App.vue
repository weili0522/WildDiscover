<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

const route = useRoute()

const showFooter = computed(() => route.name !== 'map')
</script>

<template>
  <div id="app">
    <Navbar />

    <main class="page-content">
      <RouterView />
    </main>

    <Footer v-if="showFooter" />
  </div>
</template>

<style scoped>
.page-content {
  flex: 1;
}
</style>