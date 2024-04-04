import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue';
import { WSServices } from "@/wsservices/WebSocketServices";
import { WSTServices } from "@/wsservices/WebSocketThroughputServices";
import { WSCServices } from "@/wsservices/WebSocketConfigServices";
import { usePointsStore } from "@/store/pointsStore";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
const lidarDataStore = usePointsStore()

// console.log('lidar host', process.env.VUE_APP_LIDAR_SERVER_HOST)
app.provide("$wsservices", new WSServices(lidarDataStore, { url: `ws://${process.env.VUE_APP_LIDAR_SERVER_HOST}:${process.env.VUE_APP_LIDAR_SERVER_PORT}` }))
app.provide("$wstservices", new WSTServices({ url: `ws://${process.env.VUE_APP_THROUGHPUT_SERVER_HOST}:${process.env.VUE_APP_THROUGHPUT_SERVER_PORT}`}))
app.provide("$wscservices", new WSCServices({ url: `ws://${process.env.VUE_APP_CONFIG_SERVER_HOST}:${process.env.VUE_APP_CONFIG_SERVER_PORT}` }))

app.mount('#app')
