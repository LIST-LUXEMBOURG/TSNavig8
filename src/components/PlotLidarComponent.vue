<!-- 
  © 2024 - Luxembourg Institute of Science and Technology. All Rights Reserved
  This program is licensed under AGPL V3.0 License -  https://www.gnu.org/licenses/agpl-3.0.txt
-->
<template>
  <div class="d-flex flex-column mt-2" id="lidar-wrapper">
    <div class="d-flex flex-row flex-grow-1 justify-content-center">
      <h3 class="title">Lidar Visualization</h3>
    </div>
    <div class="d-flex flex-row flex-grow-1 justify-content-center">
      <button :class="buttonClass" @click="toggleLidar" id="lidarButton"
              data-bs-toggle="tooltip" data-bs-placement="top"
              data-bs-custom-class="custom-tooltip"
              data-bs-title="Start/Stop lidar">
        <i class="bi bi-radar"></i>
      </button>
      <button :class="trafficButtonClass" @click="toggleTraffic" id="trafficButton"
              data-bs-toggle="tooltip" data-bs-placement="top"
              data-bs-custom-class="custom-tooltip"
              data-bs-title="Start/Stop traffic">
        <i class="bi bi-activity"></i>
      </button>
      <button :class="tasButtonClass" @click="toggleTas" id="tasButton"
              data-bs-toggle="tooltip" data-bs-placement="top"
              data-bs-custom-class="custom-tooltip"
              data-bs-title="Enable/Disable TAS">
        <i class="bi bi-list-ol"></i>
      </button>

      <button class="negativeButtonClass" @click="toggleNegative" id="negativeTest"
              data-bs-toggle="tooltip" data-bs-placement="top"
              data-bs-custom-class="custom-tooltip"
              data-bs-title="Enable/Disable Negative TAS">
        <i class="bi bi-x-circle"></i>
      </button>
      <button class="btn btn-success m-2 button-rounded" id="resetTas" @click.prevent="resetTas"
              data-bs-toggle="tooltip" data-bs-placement="top"
              data-bs-custom-class="custom-tooltip"
              data-bs-title="Reset TAS">
        <i class="bi bi-arrow-counterclockwise"></i>
      </button>
    </div>
    <div id="loadingOverlay" class="loading-overlay" style="display: none;">
      <div class="loading-wheel"></div>
    </div>

    <div class="d-flex flex-row flex-grow-1">
      <canvas id="lidar-container"></canvas>
     
    </div>

  </div>
</template>


<script setup>
import { Tooltip } from 'bootstrap';
import * as THREE from 'three';
import { onMounted, ref, inject, computed, onDeactivated } from "vue";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
const $wsServices = inject('$wsservices')
const $wsConfServices = inject('$wscservices');

let pointsData = computed(() => { return $wsServices.getStore().getLidarData })
let cameraZ = ref(500)
let scene = null
let camera = null
let renderer = null
let material = null
let controls = null
let lidarRunning = true;
let tasRunning = false
let trafficRunning = false
let negativeRunning = false

let tooltipLidarEl = null
let tooltipLidar = null

let tooltipTrafficEl = null
let tooltipTraffic = null

let tooltipTasEl = null
let tooltipTas = null

let tooltipNegativeEl = null
let tooltipNegative = null

let tooltipResetEl = null
let tooltipReset = null


const onMessage = (event) => {
  // Show loading overlay
  const message = JSON.parse(event.data)
  // console.log(message)
  if (message.status == "button_success") {
    console.log("The button should change the state")
    // console.log("Traffic running", trafficRunning)
    hideLoading();
    updateButtonStates();

  }
  else if(message.status == "button_error") {
    console.log("Error")
  } 
}
onMounted(() => {
  tooltipLidarEl = document.getElementById('lidarButton')
  tooltipLidar = Tooltip.getOrCreateInstance(tooltipLidarEl)
 
  tooltipTrafficEl = document.getElementById('trafficButton')
  tooltipTraffic = Tooltip.getOrCreateInstance(tooltipTrafficEl)
  
  tooltipTasEl = document.getElementById('tasButton')
  tooltipTas = Tooltip.getOrCreateInstance(tooltipTasEl)
 
  tooltipNegativeEl = document.getElementById('negativeTest')
  tooltipNegative = Tooltip.getOrCreateInstance(tooltipNegativeEl)
  
  tooltipResetEl = document.getElementById('resetTas')
  tooltipReset = Tooltip.getOrCreateInstance(tooltipResetEl)

  tooltipLidar.hide()
  tooltipTraffic.hide()
  tooltipTas.hide()
  tooltipNegative.hide()
  tooltipReset.hide()

  $wsServices.connect()
  $wsConfServices.connect()
  $wsConfServices.ws.onmessage = onMessage;

  sceneInitialisation()
  displayPoints()

})

onDeactivated(() => {
  $wsServices.disconnect();
  $wsConfServices.disconnect();
  $wsServices.getStore().setLidarData([]);
})

function sceneInitialisation() {
  updateButtonStates();
  // Create scene
  scene = new THREE.Scene();
  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1300);
  camera.position.set(0, 0, cameraZ.value)
  camera.lookAt(scene.position)
  // Create renderer
  const canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize(window.innerWidth / 2, 2 * window.innerHeight / 3)

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

      let dst = $wsServices.getStore().getLidarData[i][3]; // distance in cm
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

      let dst = $wsServices.getStore().getLidarData[i][3]; // distance in cm
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
function toggleLidar() {
  showLoading();
  $wsConfServices.ws.onmessage = onMessage;
  tooltipLidar.hide()
  if (lidarRunning) {
    lidarRunning = false;
    $wsConfServices.stopLidar();
  }
  else {
    lidarRunning = true;
    $wsConfServices.startLidar();
    displayPoints();
  }
  // updateButtonStates();
}

function toggleTraffic() {
  showLoading();
  $wsConfServices.ws.onmessage = onMessage;
  tooltipTraffic.hide()
  if (trafficRunning) {
    trafficRunning = false;
    $wsConfServices.disableNoise();
  }
  else {
    trafficRunning = true;
    $wsConfServices.enableNoise();
  }

}

function toggleTas() {
  showLoading();
  $wsConfServices.ws.onmessage = onMessage;
  tooltipTas.hide()
  if (tasRunning) {
    tasRunning = false;
    $wsConfServices.disableTas();
  }
  else {
    tasRunning = true;
    $wsConfServices.enableTas();
  }
}

function toggleNegative() {
  showLoading();
  $wsConfServices.ws.onmessage = onMessage;
  tooltipNegative.hide()
  if (negativeRunning) {
    negativeRunning = false;
    $wsConfServices.disableNegative();
  }
  else {
    negativeRunning = true;
    $wsConfServices.enableNegative();
  }
}

function buttonClass() {
  return lidarRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}
function trafficButtonClass() {
  return trafficRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}

function negativeButtonClass() {
  return negativeRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}


function updateButtonStates() {

  const button = document.getElementById('lidarButton');
  if (button) {
    button.className = buttonClass();
  }
  const trafficButton = document.getElementById('trafficButton');
  if (trafficButton) {
    trafficButton.className = trafficButtonClass();
  }
  const tasButton = document.getElementById('tasButton');
  if (tasButton) {
    tasButton.className = tasButtonClass();
  }
  const negativeButton = document.getElementById('negativeTest');
  if (negativeButton) {
    negativeButton.className = negativeButtonClass();
  }

  tooltipReset.hide()
  document.getElementById("resetTas").disabled = tasRunning;

}

function tasButtonClass() {
  return tasRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}

function resetTas() {
  showLoading();
  tasRunning = true;
  $wsConfServices.resetTas();
}

function showLoading() {
      const loadingOverlay = document.getElementById('loadingOverlay');
      if (loadingOverlay) {
        console.log("hide")
        loadingOverlay.style.display = 'flex';
      }
    }
  function  hideLoading() {
      const loadingOverlay = document.getElementById('loadingOverlay');
      if (loadingOverlay) {
        
        loadingOverlay.style.display = 'none';
      }
    }
</script>

<style scoped>
.title {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: normal;
}
.button-rounded {
  width: 40px;
  height: 40px;
  padding: 4px 0;
  border-radius: 20px;
  font-size: 8px;
  text-align: center;
}

.bi-radar,.bi-activity, .bi-list-ol, .bi-x-circle, .bi-arrow-counterclockwise{
  font-size: 20px;
  color: #ffffff;
}

#lidar-container {
  min-width: 100%;
  width: 100%;
  padding: 5px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3); /* Semi-transparent black background */
  display: none;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure it's on top of other content */
}

.loading-wheel {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1a88a2;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
