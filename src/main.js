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

const config = require('../config.json'); 
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
const lidarDataStore = usePointsStore()
app.provide("$wsservices", new WSServices(lidarDataStore, { url: `ws://${config.lidar_server.host}:${config.lidar_server.port}` }))
app.provide("$wstservices", new WSTServices({ url: `ws://${config.throughput_server.host}:${config.throughput_server.port}`}))
app.provide("$wscservices", new WSCServices({ url: `ws://${config.config_server.host}:${config.config_server.port}` }))

app.mount('#app')
