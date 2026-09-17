<script setup>

import { useRoute } from 'vue-router'

import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

const route = useRoute()


</script>

<template>
  <div id="app">
    <Navbar />

    <main class="page-content">
      <RouterView />
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.page-content {
  flex: 1;
}
</style>