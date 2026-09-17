import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import './style.css'

// --- Quick Security Popup ---
const EXPECTED_PASSWORD = import.meta.env.VITE_SITE_PASSWORD || 'admin'

if (!sessionStorage.getItem('site_auth')) {
  let attempts = 0
  let authenticated = false
  
  while (attempts < 3 && !authenticated) {
    const pass = window.prompt('Restricted Access. Please enter the site password:')
    if (pass === EXPECTED_PASSWORD) {
      sessionStorage.setItem('site_auth', 'true')
      authenticated = true
    } else if (pass === null) {
      break // User clicked cancel
    } else {
      attempts++
      if (attempts < 3) {
        window.alert('Incorrect password. Please try again.')
      }
    }
  }

  if (!authenticated) {
    document.body.innerHTML = `
      <div style="padding: 50px; font-family: sans-serif; text-align: center; color: #14533a;">
        <h1>🔒 401 Unauthorized</h1>
        <p>You do not have access to this deployment.</p>
        <button onclick="location.reload()" style="padding: 10px 20px; background: #287b57; color: white; border: none; border-radius: 6px; cursor: pointer; margin-top: 15px;">Try Again</button>
      </div>
    `
    throw new Error('Unauthorized access')
  }
}
// ----------------------------

createApp(App)
  .use(router)
  .mount('#app')
