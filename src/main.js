import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import './assets/tailwind.css'
import VueHighlightJS from 'vue-highlightjs'

Vue.config.productionTip = false

Vue.use(VueHighlightJS)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
