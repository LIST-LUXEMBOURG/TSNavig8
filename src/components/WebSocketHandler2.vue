<template>
  <div>
    <h3>This is the WebSocket component.</h3>
    <div ref="container"></div>
  </div>
</template>

<script>
import * as THREE from 'three';

export default {
  data() {
    return {
      receivedData: [],
      scene: null,
      camera: null,
      renderer: null,
      geometry: null,
      sprite: null,
      material: null,
      points: null,
      animationId: null
    };
  },
  mounted() {
    // const serverUrl = "ws://10.121.11.69:8765";
    //
    // const socket = new WebSocket(serverUrl);
    //
    // socket.onopen = () => {
    //   console.log("WebSocket connection established");
    // };

    // socket.onmessage = (event) => {
    //   const data = JSON.parse(event.data);
    //   if (data.point_cloud) {
    //     this.receivedData = JSON.parse(data.point_cloud);
    //     // console.log(this.receivedData);
    //     // console.log(Array.isArray(this.receivedData))
    //     this.plot();
    //   } else {
    //     console.warn("Received data does not contain 'point_cloud' property");
    //   }
    // };
    //
    // socket.onerror = (error) => {
    //   console.error(`WebSocket error: ${error}`);
    // };
    //
    // socket.onclose = () => {
    //   console.log("WebSocket connection closed");
    // };
  },
  methods: {
    plot() {
      if (!this.scene) {
        // Create scene
        this.scene = new THREE.Scene();

        // Create camera
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.z = 10;

        // Create renderer
        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(window.innerWidth / 2, window.innerHeight / 2);
        this.$refs.container.appendChild(this.renderer.domElement);

        // Create geometry and material for points
        this.geometry = new THREE.BufferGeometry();
        this.sprite = new THREE.TextureLoader().load( '@assets/disc.png' );
        this.material = new THREE.PointsMaterial({
            size: 0.1, // Adjust the size of the sprite
            map: this.sprite,
            vertexColors: true // Enable vertex colors
         });
        // Create points object and add it to the scene
        this.points = new THREE.Points(this.geometry, this.material);
        this.scene.add(this.points);

        this.startAnimation();
      } else {
        // Update existing geometry with new data
        let positions = new Float32Array(this.receivedData.length * 3);
        // console.log(" this.receivedData[0][0]: " +  this.receivedData[0][0])
        for (let i = 0; i < this.receivedData.length; i++) {

          positions[i * 3] = this.receivedData[i][0];
          positions[i * 3 + 1] = this.receivedData[i][1];
          positions[i * 3 + 2] = this.receivedData[i][2];
        }
        this.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        // console.log("AA: " + JSON.stringify(this.geometry))
        this.geometry.needsUpdate = true;

      }
    },
    startAnimation() {
      // Start rendering loop
      this.animationId = requestAnimationFrame(this.animate);
    },
    animate() {
      // Update any animations or changes here
      this.renderer.render(this.scene, this.camera);
      this.animationId = requestAnimationFrame(this.animate); // Continue the animation loop
    },
  }
};
</script>

<style scoped>
/* Add scoped styles if needed */
</style>
