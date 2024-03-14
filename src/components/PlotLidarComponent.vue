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


//console.log("points: " + JSON.stringify(points))
let canvas = null
let scene = null
let camera = null
let renderer = null
let geometry = null
let sprite = null
let material = ref(null)
let pointsThree = ref(null)
let counter = 0

onMounted(() => {
  $wsServices.connect()

  initCanvas();
  // watch(pointsData, () => {
  //   updateScene()
  // })
//     // setInterval(updateScene, 10);
  
// })
   // Clean the scene every 20 seconds
   
  // updateScene()
  // setInterval(clearScene(), 500)

})
function clearScene() {
  console.log("Clearing scene...");
  scene = new THREE.Scene();
  geometry = new THREE.BufferGeometry();
  // scene.remove(pointsThree.value);
  // pointsThree.value = null;
  // setTimeout(1000);
}

function initCanvas() {
  // Create scene
  scene = new THREE.Scene();

  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  //console.log("camera: " + JSON.stringify(camera))
  camera.position.z = 500;

  // Create renderer
  canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize(window.innerWidth/2, 3*window.innerHeight/4)
  // geometry = new THREE.BufferGeometry(); // if you put it here, it contains only a set of points.

  sprite = new THREE.TextureLoader().load('disc.png');
  material = new THREE.PointsMaterial({
    size: 0.1, // Adjust the size of the sprite
    map: sprite,
    vertexColors: true // Enable vertex colors
  });
  animate()
 
}
function updateScene() {
   // Clear the scene
  //  scene.remove(pointsThree.value);
  // scene = new THREE.Scene();
  // console.log("pointsData: " + pointsData.value)
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
  geometry.needsUpdate = true;
 
  pointsThree = new THREE.Points(geometry, material);
  scene.add(pointsThree);
  
  animate()
  counter++;
  // console.log("counter ", counter)
  if (counter==10){
    counter=0;
    clearScene();
  }
}
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  // setInterval(clearScene, 1000);

  // setTimeout(1000000);

  // console.log('animate!')
}

</script>

<style scoped></style>
