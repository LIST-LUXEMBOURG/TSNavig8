export class WSServices {

    constructor(store, options) {
        this.ws = null
        this.options = options
        this.store = store
        this.setLidarData = null
        this.reconnectInterval = options.reconnectInterval || 1000
    }

    connect() {
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
            // this.ws.send("test")
            if (points_received.point_cloud) {
                let data_temp = JSON.parse(points_received.point_cloud)
                this.getStore().setLidarData(data_temp)
            }
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

    getStore() {
        return this.store;
    }

    enableTas() {
        if (this.ws != null) {
            this.ws.send('enable-tas')
        }
    }
    disableTas() {
        if (this.ws != null) {
            this.ws.send('disable-tas')
        }
    }
    enableNoise() {
        if (this.ws != null) {
            this.ws.send('enable-noise')
        }
    }
    disableNoise() {
        if (this.ws != null) {
            this.ws.send('disable-noise')
        }
    }

    sendTas(jsonFile) {
        if (this.ws != null) {
            this.ws.send(JSON.stringify(jsonFile))
        }
    }

    configureNoise(text) {
        if (this.ws != null) {
            this.ws.send(text)
        }
    }

    negativeTest() {
        if (this.ws != null) {
            this.ws.send('negative-tas')
        }
    }

    resetTas() {
        if (this.ws != null) {
            this.ws.send('reset-tas')
        }
    }

}
