/*
  © 2024 - Luxembourg Institute of Science and Technology. All Rights Reserved
  This program is licensed under AGPL V3.0 License -  https://www.gnu.org/licenses/agpl-3.0.txt
*/
export class WSTServices {

    constructor(options) {
        this.ws = null
        this.options = options
        this.reconnectInterval = options.reconnectInterval || 1000
    }

    connect() {
        if (this.ws == null) {
            this.ws = new WebSocket(this.options.url)
            console.log("---New web socket instance is created")
            console.log("listening on url: " + this.options.url)
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
    }

    disconnect() {
        if (this.ws != null) {
            this.ws.close()
            this.ws = null
            console.log("web socket instance is destroyed!")
        }
    }

}
