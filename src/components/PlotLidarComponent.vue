<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-2">
        <div class="d-flex flex-column">
          <button class="btn btn-success m-2" id="startButton" @click.prevent="start">START LIDAR</button>
          <button class="btn btn-danger m-2" id="stopButton" @click.prevent="stop">STOP LIDAR</button>
          <button class="btn btn-success m-2" id="enableTraffic" @click.prevent="enableNoise">GENERATE TRAFFIC</button>
          <button class="btn btn-danger m-2" id="disableTraffic" @click.prevent="disableNoise">STOP TRAFFIC</button>
          <button class="btn btn-success m-2" id="enableTas" @click.prevent="enableTas">ENABLE TAS</button>
          <button class="btn btn-danger m-2" id="disableTas" @click.prevent="disableTas">DISABLE TAS</button>
          <button class="btn btn-success m-2" id="negativeTest" @click.prevent="negativeTest">NEGATIVE TEST</button>
          <button class="btn btn-success m-2" id="resetTas" @click.prevent="resetTas">DEFAULT TAS</button>
        </div>
      </div>
      
      <div class="col-md-8">
        <h3>Lidar Vizualization</h3>
        <canvas id="lidar-container"></canvas>
      </div>
    </div>
  </div>
</template>


<script setup>
import * as THREE from 'three';
import { onMounted, ref, inject, computed, onDeactivated } from "vue";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
const $wsServices = inject('$wsservices')
let pointsData = computed(() => { return $wsServices.getStore().getLidarData })
let cameraZ = ref(500)
let scene = null
let camera = null
let renderer = null
let material = null
let controls = null
let lidarRunning = true
let tasRunning = false
let trafficRunning = false

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
  updateButtonStates();
  // updateTasButtonStates();
  // Create scene
  scene = new THREE.Scene();
  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1300);
  camera.position.set(0, 0, cameraZ.value)
  camera.lookAt(scene.position)
  // Create renderer
  const canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize( window.innerWidth / 2, 2 * window.innerHeight / 3)

  // Create controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.mouseButtons.LEFT = THREE.MOUSE.ROTATE;
  controls.mouseButtons.RIGHT = THREE.MOUSE.PAN;
  controls.maxDistance = 1500;
  // controls.minDistance = 0;
  // controls.rotateSpeed = 0.5;
  // controls.panSpeed = 0.5;
  // controls.screenSpacePanning = false;
  window.addEventListener('keydown', function (e) {
    if (e.code === 'KeyR')
      controls.reset();

  })

  const sprite = new THREE.TextureLoader().load('disc.png');
  material = new THREE.PointsMaterial({
    size: 2, // Adjust the size of the sprite
    map: sprite,
    vertexColors: true // Enable vertex colors
  });
}
function displayPoints() {
  const positions = new Float32Array(pointsData.value.length * 3); // Each point has x, y, z coordinates
  const colors = new Float32Array(pointsData.value.length * 3); // Each point has r, g, b colors
  const geometry = new THREE.BufferGeometry();
  for (let i = 0; i < pointsData.value.length; i++) {
    if ($wsServices.getStore().getLidarData[i] !== undefined) {
      // console.log('Display points')
      positions[i * 3] = $wsServices.getStore().getLidarData[i][0];
      positions[i * 3 + 1] = $wsServices.getStore().getLidarData[i][1];
      positions[i * 3 + 2] = $wsServices.getStore().getLidarData[i][2];

      let dst = $wsServices.getStore().getLidarData[i][4]; // distance in cm
      let clr = dst / 255;
      colors[i * 3] = 1 - clr;
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
  const positions = new Float32Array(pointsData.value.length * 3);
  const colors = new Float32Array(pointsData.value.length * 3);
  for (let i = 0; i < pointsData.value.length; i++) {
    if ($wsServices.getStore().getLidarData[i] !== undefined) {
      positions[i * 3] = $wsServices.getStore().getLidarData[i][0];
      positions[i * 3 + 1] = $wsServices.getStore().getLidarData[i][1];
      positions[i * 3 + 2] = $wsServices.getStore().getLidarData[i][2];

      let dst = $wsServices.getStore().getLidarData[i][4]; // distance in cm
      let clr = dst / 255;
      colors[i * 3] = 1 - clr;
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

function stop() {
  lidarRunning = false;
  $wsServices.disconnect();
  updateButtonStates();
}

function start() {
  lidarRunning = true;
  $wsServices.connect();
  displayPoints();
  updateButtonStates();
}

function updateButtonStates() {
  updateButtonState("startButton", lidarRunning);
  updateButtonState("stopButton", !lidarRunning);
  updateButtonState("enableTraffic", trafficRunning);
  updateButtonState("disableTraffic", !trafficRunning);
  updateButtonState("enableTas", tasRunning);
  updateButtonState("negativeTest", tasRunning);
  updateButtonState("resetTas", tasRunning);
  updateButtonState("disableTas", !tasRunning);
}

function updateButtonState(buttonId, running) {
  document.getElementById(buttonId).disabled = running;
}

function enableTas() {
  tasRunning = true;
  $wsServices.enableTas();
  updateButtonStates();
}

function disableTas() {
  tasRunning = false;
  $wsServices.disableTas();
  updateButtonStates();
}

function enableNoise() {
  trafficRunning = true;
  $wsServices.enableNoise();
  updateButtonStates();
}

function disableNoise() {
  trafficRunning = false;
  $wsServices.disableNoise();
  updateButtonStates();
}

function negativeTest() {
  tasRunning = true;
  trafficRunning = true;
  $wsServices.negativeTest();
  updateButtonStates();
}

function resetTas() {
  tasRunning = true;
  $wsServices.resetTas();
  updateButtonStates();
}
</script>

<style scoped></style>
