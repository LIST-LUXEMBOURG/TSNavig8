<template>
  <div >
    <h3>This is the WebSocket component.</h3>
    <!-- <p>{{receivedData}}</p> -->
  </div>
</template>

<script>

export default {
  data() {
    return {
      receivedData: [],
    };
  },
  mounted() {
    const serverUrl = "ws://10.121.11.69:8765";

    const socket = new WebSocket(serverUrl);

    socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    socket.onmessage = (event) => {
      // Parse the incoming JSON data
      const data = JSON.parse(event.data);
      
      // Check if the received data contains 'point_cloud' property
      if (data.point_cloud) {
        this.receivedData = data.point_cloud;      
        
      } else {
          console.warn("Received data does not contain 'point_cloud' property");
      }
    };

    socket.onerror = (error) => {
      console.error(`WebSocket error: ${error}`);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  },
}
</script>
<style scoped>
/* Add scoped styles if needed */
</style>
