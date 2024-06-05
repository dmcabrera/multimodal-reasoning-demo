// Imports
import 'bootstrap/dist/js/bootstrap.js'
import 'bootstrap/dist/css/bootstrap.css'
import { createApp } from 'vue/dist/vue.esm-bundler' // <--- 1
//import { createApp } from 'vue'
import App from './App.vue'
import i18n from "./i18n" // <--- 2

// Instancio la app
createApp(App).
  use(i18n). // <--- 3
  mount('#app')


