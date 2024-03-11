<template>
    <div ref="container" id="container"></div>
  </template>

  <script setup>
  import * as THREE from 'three';
  import {onMounted, ref, inject} from "vue";
  //import {usePointsStore} from "@/store/pointsStore";

  const $wsServices = inject('$wsServices')
  //const store = usePointsStore()
  //const $points = store.getLidarData

  let scene = null
  let camera = null
  let renderer = null
  let geometry = null
  let sprite = null
  let material = ref(null)
  let points = ref(null)

  onMounted(() => {
    $wsServices.connect()
    init();
  })

  const animate = () => {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  function init() {

      // Create scene
      scene = new THREE.Scene();

      // Create camera
      camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
//      console.log("camera: " + JSON.stringify(camera))
      camera.position.z = 10;

      // Create renderer
      renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth/2, window.innerHeight/2);
//      console.log("renderer: " + JSON.stringify(renderer))
      document.getElementById('container').appendChild(renderer.domElement);

      const numPoints=100
      const positions = new Float32Array(numPoints * 3); // Each point has x, y, z coordinates
      const colors = new Float32Array(numPoints * 3); // Each point has r, g, b colors

      for (let i = 0; i < numPoints; i++) {
        // Generate random point coordinates
        const x = Math.random() * 20 - 10; // Adjust range as needed
        const y = Math.random() * 20 - 10;
        const z = Math.random() * 20 - 10;

        // Set position data
        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        // Set color data (white)
        colors[i * 3] = 1.0;
        colors[i * 3 + 1] = 1.0;
        colors[i * 3 + 2] = 1.0;
      }

      geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
//      console.log("geometry: " + JSON.stringify(geometry))

      // Create a sprite material for changing the shape of the points
      sprite = new THREE.TextureLoader().load( 'disc.png' );
      // sprite.colorSpace = THREE.SRGBColorSpace;
      material = new THREE.PointsMaterial({
        size: 0.1, // Adjust the size of the sprite
        map: sprite,
        vertexColors: true // Enable vertex colors
      });

      points = new THREE.Points(geometry, material);
      scene.add(points);

      // Start rendering loop
      animate();
  }

  </script>

  <style scoped>
  </style>
