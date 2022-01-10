import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import './assets/tailwind.css'
import VueHighlightJS from 'vue-highlightjs'
import VueViewer from "v-viewer";
import 'viewerjs/dist/viewer.css'
import store from "./store"

Vue.config.productionTip = false

Vue.use(VueHighlightJS)

Vue.use(VueViewer)

new Vue({
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
