import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import './assets/tailwind.css'
import VueViewer from "v-viewer";
import 'viewerjs/dist/viewer.css'
import store from "./store"

// Start Vue
Vue.config.productionTip = false
Vue.use(VueViewer)
new Vue({
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
