import {inject} from "vue";

export class WSServices {

    constructor(options) {
        this.ws = null
        this.options = options
        this.store = null
        this.setLidarData = null
        this.id_client = -1
        this.reconnectInterval = options.reconnectInterval || 1000
    }

    connect() {
        this.store = inject("$lidarDataStore")
        this.setLidarData = this.store
        if (this.ws == null) {
            this.ws = new WebSocket(this.options.url)
            console.log("New web socket instance is created")
            console.log("listening on url: " + this.options.url)
            console.log("using store: " + JSON.stringify(this.store))
        }
        else {
            console.log("Reusing existing web socket instance")
        }

        this.ws.onopen = () => {
            this.reconnectInterval = this.options.reconnectInterval || 1000
            console.log("Connection to server is established!")
        }

        this.ws.onclose = (event) => {
            if (event) {
                console.log("event.code: " + event.code)
                // Event.code 1006 is our normal close event
                if (event.code !== 1006) {
                    console.log("reconnection ...")
                    let maxReconnectInterval = this.options.maxReconnectInterval || 3000
                    setTimeout(() => {
                        if (this.reconnectInterval < maxReconnectInterval) {
                            // Reconnect interval can't be > x seconds
                            this.reconnectInterval += 1000
                        }
                    }, this.reconnectInterval)
                }
                else {
                    console.log("event.code == 1006")
                    console.log("web socket connection is closed")
                }
            }
        }

        this.ws.onerror = (error) => {
            console.error(error)
        }

        this.ws.onmessage = (event) => {
            const points_received = JSON.parse(event.data)
            console.log("received data from LIDAR: " + points_received)
            this.setLidarData(points_received)
        }
    }

    disconnect() {
        if (this.ws != null) {
            this.ws.close()
            this.ws = null
            // this.store.clearMsgAlerts()
            console.log("web socket instance is destroyed!")
        }
    }
}
