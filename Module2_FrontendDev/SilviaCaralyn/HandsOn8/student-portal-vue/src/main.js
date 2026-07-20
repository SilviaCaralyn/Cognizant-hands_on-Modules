import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Step 150: global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error captured:', err, info)
}

app.mount('#app')
