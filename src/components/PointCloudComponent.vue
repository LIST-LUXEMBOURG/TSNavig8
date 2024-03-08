<template>
    <div ref="container"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  
  export default {
    mounted() {
      this.init();
    },
    methods: {
      init() {
        // Create scene
        const scene = new THREE.Scene();
  
        // Create camera
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 10;
  
        // Create renderer
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth/2, window.innerHeight/2);
        this.$refs.container.appendChild(renderer.domElement);
  
        // Create points
        const geometry = new THREE.BufferGeometry();

      
  
        // Generate random points
        const positions = [];
        for (let i = 0; i < 1000; i++) {
          positions.push(Math.random() * 10 - 5);
          positions.push(Math.random() * 10 - 5);
          positions.push(Math.random() * 10 - 5);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(positions, 3));

        // const material = new THREE.PointsMaterial({ color: 0xffffff });
        // Create a sprite material for changing the shape of the points
        const sprite = new THREE.TextureLoader().load( './disc.png' );
        // sprite.colorSpace = THREE.SRGBColorSpace;
        const material = new THREE.PointsMaterial({ 
        size: 0.1, // Adjust the size of the sprite
        map: sprite,
        vertexColors: true // Enable vertex colors
      });	
        const points = new THREE.Points(geometry, material);
        scene.add(points);
  
        // Render loop
        const animate = () => {
          requestAnimationFrame(animate);
          points.rotation.x += 0.01;
          points.rotation.y += 0.01;
          renderer.render(scene, camera);
        };
  
        animate();
      }
    }
  };
  </script>
  
  <style scoped>

  </style>
  