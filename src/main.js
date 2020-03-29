/*!

=========================================================
* Vue Argon Dashboard - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import ArgonDashboard from './plugins/argon-dashboard'

import BootstrapVue from "bootstrap-vue"
import Vuex from 'vuex'

import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'

Vue.config.productionTip = false;

Vue.use(BootstrapVue);

Vue.use(VueLayers, {
  // global data projection, see https://vuelayers.github.io/#/quickstart?id=global-data-projection
  // dataProjection: 'EPSG:4326',
});

// Make sure to call Vue.use(Vuex) first if using a module system

Vue.use(Vuex);
const store = new Vuex.Store({
  state: {
    count: 0,
    statType: 'avg',
    activeSensor: null,
    serviceUrl: "http://localhost/lora/get.php",
    mapmove: true
  },
  mutations: {
    increment (state) {
      state.count++
    },
    setStat(state, type) {
      state.statType = type
    },
    setActiveSensor(state, sensor) {
      state.activeSensor = sensor;
    },
    changeMapMove(state) {
      state.mapmove = !state.mapmove;
    },
    setMapMove(state, mapmove) {
      state.mapmove = mapmove;
    }
  }
});

Vue.use(ArgonDashboard);
new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app');
