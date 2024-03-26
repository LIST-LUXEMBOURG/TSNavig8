import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue';
import { WSServices } from "@/wsservices/WebSocketServices";
import { WSTServices } from "@/wsservices/WebSocketThroughputServices";
import { usePointsStore } from "@/store/pointsStore";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
const lidarDataStore = usePointsStore()
app.provide("$wsservices", new WSServices(lidarDataStore, { url: "ws://10.150.2.5:8765" }))
app.provide("$wstservices", new WSTServices({ url: "ws://10.150.2.5:9000" }))
app.mount('#app')
