<template>
  <div class="d-flex flex-column mt-2">
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
      <button :class="trafficButtonClass" @click="toggleTraffic" id="trafficButton">
        <i class="bi bi-infinity"></i>
      </button>
      <button :class="tasButtonClass" @click="toggleTas" id="tasButton">{{ tasButtonText }}</button>
      <button class="btn btn-success m-2" id="negativeTest" @click.prevent="negativeTest">NEGATIVE TEST</button>
      <button class="btn btn-success m-2" id="resetTas" @click.prevent="resetTas">DEFAULT TAS</button>
    </div>
<!--    <div class="row">-->
<!--      <div class="col-md-2">-->
<!--        <div class="d-flex flex-column">-->
<!--          <button :class="buttonClass" @click="toggleLidar" id="lidarButton">-->
<!--            <i class="bi bi-radar"></i>-->
<!--          </button>-->
<!--          <button :class="trafficButtonClass" @click="toggleTraffic" id="trafficButton">{{ trafficButtonText }}</button>-->

<!--        </div>-->
<!--      </div>-->

<!--      <div class="col-md-8">-->
<!--        <h3>Lidar Vizualization</h3>-->
    <div class="d-flex flex-row flex-grow-1">
      <canvas id="lidar-container"></canvas>
    </div>
<!--      </div>-->
<!--    </div>-->
  </div>
</template>


<script setup>
import { Tooltip } from 'bootstrap';
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
let lidarRunning = true;
let tasRunning = false
let trafficRunning = false

let tooltipLidarEl = null
let tooltipLidar = null

onMounted(() => {
  tooltipLidarEl = document.getElementById('lidarButton')
  tooltipLidar = Tooltip.getOrCreateInstance(tooltipLidarEl)
  tooltipLidarEl.addEventListener('shown.bs.tooltip', () => {
    console.log("show")
  })
  tooltipLidar.hide()
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
function toggleLidar() {
  tooltipLidar.hide()
  if (lidarRunning) {
    lidarRunning = false;
    $wsServices.disconnect();
  }
  else {
    lidarRunning = true;
    $wsServices.connect();
    displayPoints();
  }
  updateButtonStates();
}

function toggleTraffic() {
  if (trafficRunning) {
    trafficRunning = false;
    $wsServices.disableNoise();
  }
  else {
    trafficRunning = true;
    $wsServices.enableNoise();
  }
  updateButtonStates();

}

function toggleTas() {
  if (tasRunning) {
    tasRunning = false;
    $wsServices.disableTas();
  }
  else {
    tasRunning = true;
  $wsServices.enableTas();
  }
  updateButtonStates();
}

// function buttonText() {
//   return lidarRunning ? 'STOP LIDAR' : 'START LIDAR';
// }
function buttonClass() {
  return lidarRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}
function trafficButtonClass() {
  return trafficRunning ? 'btn btn-danger m-2 button-rounded' : 'btn btn-success m-2 button-rounded';
}

function updateButtonStates() {

  const button = document.getElementById('lidarButton');
  if (button) {
//    button.innerText = buttonText();
    button.className = buttonClass();
  }
  const trafficButton = document.getElementById('trafficButton');
  if (trafficButton) {
    // trafficButton.innerText = trafficButtonText();
    trafficButton.className = trafficButtonClass();
  }
  const tasButton = document.getElementById('tasButton');
  if (tasButton) {
    tasButton.innerText = tasButtonText();
    tasButton.className = tasButtonClass();
  }

  // updateButtonState("enableTas", tasRunning);
  updateButtonState("negativeTest", tasRunning);
  updateButtonState("resetTas", tasRunning);
  // updateButtonState("disableTas", !tasRunning);
}


// function trafficButtonText() {
//   return trafficRunning ? 'STOP TRAFFIC' : 'GENERATE TRAFFIC';
// }


function tasButtonText() {
  return tasRunning ? 'DISABLE TAS' : 'ENABLE TAS';
}
function tasButtonClass() {
  return tasRunning ? 'btn btn-danger m-2' : 'btn btn-success m-2';
}

function updateButtonState(buttonId, running) {
  document.getElementById(buttonId).disabled = running;
}
// function enableTas() {
//   tasRunning = true;
//   $wsServices.enableTas();
//   updateButtonStates();
// }

// function disableTas() {
//   tasRunning = false;
//   $wsServices.disableTas();
//   updateButtonStates();
// }



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

.bi-radar {
  font-size: 20px;
  color: #ffffff;
}
.bi-infinity {
  font-size: 20px;
  color: #ffffff;
}
#lidar-container {
  min-width: 100%;
  width: 100%;
  padding: 5px;
}
</style>
