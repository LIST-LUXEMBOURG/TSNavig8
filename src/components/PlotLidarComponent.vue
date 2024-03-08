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

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        
        // Create a sprite material for changing the shape of the points
        const sprite = new THREE.TextureLoader().load( 'disc.png' );
        // sprite.colorSpace = THREE.SRGBColorSpace;
        const material = new THREE.PointsMaterial({ 
            size: 0.1, // Adjust the size of the sprite
            map: sprite,
            vertexColors: true // Enable vertex colors
         });		

        const points = new THREE.Points(geometry, material);
        scene.add(points);


        // Start rendering loop
        const animate = () => {
          requestAnimationFrame(animate);
          renderer.render(scene, camera);       
        }
        animate();
      },
    }
  };
  </script>
  
  <style scoped>
  </style>
  