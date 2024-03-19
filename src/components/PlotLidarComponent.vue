<template>
  <div class="container-fluid">
    <canvas id="lidar-container"></canvas>
    <div class="container">
      <div class="d-flex">
        <button class="btn byn-danger m-2" @click.prevent="stop">STOP</button>
        <button class="btn byn-primary m-2" @click.prevent="start">START</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import * as THREE from 'three';
import { onMounted, ref, inject, computed, onDeactivated } from "vue";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
const $wsServices = inject('$wsservices')
let pointsData = computed(() => { return $wsServices.getStore().getLidarData })
let cameraZ=ref(500)
let scene = null
let camera = null
let renderer = null
let material = null
let controls = null

onMounted(() => {
  $wsServices.connect()
  sceneInitialisation()
  displayPoints()
})

onDeactivated(() => {
  $wsServices.disconnect();
  $wsServices.getStore().setLidarData([]);
})

function sceneInitialisation() {
  // Create scene
  scene = new THREE.Scene();
  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1300);
  //console.log("camera: " + JSON.stringify(camera))
  // camera.position.z = cameraZ.value;
  camera.position.set(0,0, cameraZ.value)
  camera.lookAt(scene.position)
  // Create renderer
  const canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize(1080, 800)
  
  


  // Create controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.mouseButtons.LEFT = THREE.MOUSE.ROTATE;
  controls.mouseButtons.RIGHT = THREE.MOUSE.PAN;  
  controls.maxDistance = 1500;
  controls.minDistance = 0;
  // controls.rotateSpeed = 0.5;
  // controls.panSpeed = 0.5;
  // controls.screenSpacePanning = false;
  window.addEventListener('keydown', function(e) {
    if(e.code === 'KeyR')
      controls.reset();
    
  })

  const sprite = new THREE.TextureLoader().load('disc.png');
  material = new THREE.PointsMaterial({
    size: 0.1, // Adjust the size of the sprite
    map: sprite,
    vertexColors: true // Enable vertex colors
  });

 
}
function displayPoints() {
  const positions = new Float32Array(pointsData.value.length * 3); // Each point has x, y, z coordinates
  const colors = new Float32Array(pointsData.value.length* 3); // Each point has r, g, b colors
  const geometry = new THREE.BufferGeometry();
  for (let i = 0; i < pointsData.value.length; i++) {
    if ($wsServices.getStore().getLidarData[i] !== undefined)
    {
      // console.log('Display points')
      positions[i * 3] = $wsServices.getStore().getLidarData[i][0];
      positions[i * 3 + 1] = $wsServices.getStore().getLidarData[i][1];
      positions[i * 3 + 2] = $wsServices.getStore().getLidarData[i][2];

      let dst = $wsServices.getStore().getLidarData[i][4]; // distance in cm
      let clr = dst/255;
        colors[i * 3] = 1-clr;
        colors[i * 3 + 1] = clr;
        colors[i * 3 + 2] = clr;
    }
  }
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  const pointsThree = new THREE.Points(geometry, material);
  scene.add(pointsThree);
  // controls.target = new THREE.Vector3(0, 0, 0)
  // controls.update();
  animate();
  geometry.dispose(); // to save memory
  // controls.dispose()
}
function animate() {
  scene.remove.apply(scene, scene.children)
  const positions = new Float32Array(pointsData.value.length*3);
  const colors = new Float32Array(pointsData.value.length*3);
  for (let i = 0; i < pointsData.value.length; i++) {
    if ($wsServices.getStore().getLidarData[i] !== undefined)
    {
      positions[i * 3] = $wsServices.getStore().getLidarData[i][0];
      positions[i * 3 + 1] = $wsServices.getStore().getLidarData[i][1];
      positions[i * 3 + 2] = $wsServices.getStore().getLidarData[i][2];

      let dst = $wsServices.getStore().getLidarData[i][4]; // distance in cm
      let clr = dst/255;
        colors[i * 3] = 1-clr;
        colors[i * 3 + 1] = clr;
        colors[i * 3 + 2] = clr;
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geometry.needsUpdate = true
  material.needsUpdate = true
  // Create axes
  // const axesHelper = new THREE.AxesHelper(10000);
  // scene.add(axesHelper)
  const pointsThree = new THREE.Points(geometry, material);
  scene.add(pointsThree);
  camera.position.z = cameraZ.value
  // camera.position.set(0,0, cameraZ.value)
  // camera.lookAt(scene.position)
  requestAnimationFrame(animate);
  // controls.target = new THREE.Vector3(0, 0, 0)
  controls.update();
  renderer.render(scene, camera);
  geometry.dispose();  // to save memory
  // axesHelper.dispose()
}

function stop(){
  $wsServices.disconnect();
}

function start(){
  $wsServices.connect();
  displayPoints();
}

</script>

<style scoped></style>
