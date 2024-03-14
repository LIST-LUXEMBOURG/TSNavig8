<template>
  <div class="d-flex flex-column">
    <!-- <p>{{ pointsData }}</p>  -->
    <canvas id="lidar-container"></canvas>
    <!--    <p></p>-->
    <button class="btn btn-primary m-2" @click="updateScene">increase</button>
  </div>
</template>

<script setup>
import * as THREE from 'three';
import { onMounted, ref, inject, computed } from "vue";
import { usePointsStore } from "@/store/pointsStore";

const $wsServices = inject('$wsServices')
const store = usePointsStore()
let pointsData = computed(() => { return store.getLidarData })

function updateScene() {
  console.log("pointsData: " + pointsData.value)
  const positions = new Float32Array(pointsData.value.length * 3); // Each point has x, y, z coordinates
  const colors = new Float32Array(pointsData.value.length * 3); // Each point has r, g, b colors
  for (let i = 0; i < pointsData.value.length; i++) {
    positions[i * 3] = pointsData.value[i][0];
    positions[i * 3 + 1] = pointsData.value[i][1];
    positions[i * 3 + 2] = pointsData.value[i][2];

    let dst = pointsData.value[i][4]; // distance in cm
    // let refl = pointsData.value[i][3]; // reflectivity (intensity)

    // console.log('distance: ', pointsData.value[i][4])
    let clr = dst/255;
      colors[i * 3] = 1-clr;
      colors[i * 3 + 1] = clr;
      colors[i * 3 + 2] =clr ;
  }
  geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
  // geometry.needsUpdate = true;
  material = new THREE.PointsMaterial({
    size: 0.1, // Adjust the size of the sprite
    map: sprite,
    vertexColors: true // Enable vertex colors
  });

  pointsThree = new THREE.Points(geometry, material);

  console.log("pointsThree: " + JSON.stringify(pointsThree))
  scene.add(pointsThree);
  const tmp = scene.toJSON()['geometries'][0]['data']['attributes']['position']['array']
  console.log("scene " + JSON.stringify(tmp).length)

  animate()
  //console.log('scene ' + JSON.stringify(scene))
}
//console.log("points: " + JSON.stringify(points))
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

  initCanvas();
  // updateScene()
  // setInterval(updateScene(), 10000)

})

function initCanvas() {
  // Create scene
  scene = new THREE.Scene();

  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  //console.log("camera: " + JSON.stringify(camera))
  camera.position.z = 400;

  // Create renderer
  canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize(window.innerWidth/2, 2*window.innerHeight/3)
  // geometry = new THREE.BufferGeometry(); // if you put it here, it contains only a set of points.

  sprite = new THREE.TextureLoader().load('disc.png');
  animate()
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  console.log('animate!')
}

</script>

<style scoped></style>
