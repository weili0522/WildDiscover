import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import './style.css'

// Removed JavaScript security popup since Vercel middleware is handling auth.

createApp(App)
  .use(router)
  .mount('#app')
