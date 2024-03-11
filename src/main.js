import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue'
import { WSServices} from "@/wsservices/WebSocketServices";
import {usePointsStore} from "@/store/pointsStore";

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
const lidarStore = usePointsStore()
app.provide("$wsServices", new WSServices({url: "ws://10.121.11.69:8765"}, { lidarStore }))
app.mount('#app')
