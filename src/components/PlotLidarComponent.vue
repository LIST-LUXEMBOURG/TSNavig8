<template>
  <div class="container-fluid">
    <canvas id="lidar-container"></canvas>
    <div class="container">
      <div class="d-flex">
        <button class="btn byn-danger m-2" @click.prevent="stop">STOP</button>
        <button class="btn byn-primary m-2" @click.prevent="start">START</button>
        <button class="btn byn-primary m-2" @click.prevent="increaseCamera">Z CAMERA +</button>
        <button class="btn byn-primary m-2" @click.prevent="decreaseCamera">Z CAMERA -</button>

      </div>

    </div>
  </div>
</template>

<script setup>
import * as THREE from 'three';
import { onMounted, ref, inject, computed, onDeactivated } from "vue";

const $wsServices = inject('$wsservices')
let pointsData = computed(() => { return $wsServices.getStore().getLidarData })
console.log("Lidar: ",pointsData)
let cameraZ=ref(500)

let scene = null
let camera = null
let renderer = null
let material = null


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
  camera.position.z = cameraZ.value;

  // Create renderer
  const canvas = document.getElementById('lidar-container');
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas });
  renderer.setSize(1080, 800)

  const sprite = new THREE.TextureLoader().load('disc.png');
  material = new THREE.PointsMaterial({
    size: 0.1, // Adjust the size of the sprite
    map: sprite,
    vertexColors: true // Enable vertex colors
  });
  // console.log('Scene initialised')
  // animate()
 
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
      // let refl = pointsData.value[i][3]; // reflectivity (intensity)

      let clr = dst/255;
        colors[i * 3] = 1-clr;
        colors[i * 3 + 1] = clr;
        colors[i * 3 + 2] = clr;
    }
    // else{
    //   console.log('else')
    // }
  }
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  const pointsThree = new THREE.Points(geometry, material);
  scene.add(pointsThree);
  animate();
  // geometry.dispose()
  // positions.dispose()
  // colors.dispose()
  // pointsThree.dispose()
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
      // let refl = pointsData.value[i][3]; // reflectivity (intensity)

      // console.log('distance: ', pointsData.value[i][4])
      let clr = dst/255;
        colors[i * 3] = 1-clr;
        colors[i * 3 + 1] = clr;
        colors[i * 3 + 2] = clr;
    }
    // else{
    //   console.log('Here')
    // }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geometry.needsUpdate = true
  material.needsUpdate = true
  const pointsThree = new THREE.Points(geometry, material);
  scene.add(pointsThree);
  camera.position.z = cameraZ.value

  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

function stop(){
  $wsServices.disconnect();
}

function start(){
  $wsServices.connect();
  displayPoints();
}

function increaseCamera(){
  cameraZ.value = cameraZ.value+40
}

function decreaseCamera(){
  cameraZ.value = cameraZ.value-40
  if (cameraZ.value <=0) cameraZ.value = 0
}

</script>

<style scoped></style>
