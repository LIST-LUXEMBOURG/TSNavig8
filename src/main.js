import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue'
import { WSServices} from "@/wsservices/WebSocketServices";
import {usePointsStore} from "@/store/pointsStore";
import 'bootstrap/dist/css/bootstrap.css'

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
const lidarDataStore = usePointsStore()
app.provide("$wsservices", new WSServices(lidarDataStore, {url: "ws://10.121.11.69:8765"}))
// app.provide("$lidarDataStore", lidarStore)
app.mount('#app')
