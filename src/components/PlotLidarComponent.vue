<template>
  <div class="d-flex flex-column">
    <p>{{ pointsData }}</p>
    <canvas id="lidar-container"></canvas>
<!--    <p></p>-->
    <button class="btn btn-primary m-2" @click="increase">increase</button>
  </div>
  </template>

  <script setup>
  import * as THREE from 'three';
  import {onMounted, ref, inject, computed} from "vue";
  import {usePointsStore} from "@/store/pointsStore";

  const $wsServices = inject('$wsServices')
  const store = usePointsStore()
  let pointsData = computed( () => {return store.getLidarData} )
  //console.log("points: " + JSON.stringify(points))

  let p = ref(0)

  let canvas = null
  let scene = null
  let camera = null
  let renderer = null
  let geometry = null
  let sprite = null
  let material = ref(null)
  let pointsThree = ref(null)

  onMounted(() => {
    $wsServices.connect()

    init();
//    store.setLidarData([10, 20, 30])
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
      canvas = document.getElementById('lidar-container');
      renderer = new THREE.WebGLRenderer({antialias: true, canvas:canvas});
//      renderer.setSize(window.innerWidth/2, window.innerHeight/2);

//      console.log("renderer: " + JSON.stringify(renderer))
//      document.getElementById('container').appendChild(renderer.domElement);

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

      pointsThree = new THREE.Points(geometry, material);
      scene.add(pointsThree);

      // Start rendering loop
      animate();
  }

  function increase() {
    store.setLidarData([p.value, p.value*2, p.value*3])
    p.value++
  }
  </script>

  <style scoped>
  </style>
