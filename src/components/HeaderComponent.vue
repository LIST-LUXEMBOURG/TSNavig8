<template>
    <div>
        <header class="d-flex justify-content-between align-items-center">
            <div>
            <h3>{{ props.title }}</h3>
            <p>Authors: Darinela Andronovici, Damien Nicolas, Ion Turcanu, and Cristoph Sommer</p>
        </div>
            <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                aria-controls="offcanvasRight"> <i class="bi bi-gear-wide"></i></button>

            <div class="offcanvas offcanvas-end canvas-container" tabindex="-1" id="offcanvasRight"
                 aria-labelledby="offcanvasRightLabel">
                <div class="offcanvas-header">
                    <h3 id="offcanvasRightLabel">Configuration Menu</h3>
                    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <NoiseComponent />
                    <TasComponent />
                </div>
            </div>
        </header>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';
import TasComponent from '@/components/TasComponent.vue';
import NoiseComponent from '@/components/NoiseComponent.vue';
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
header {
  background-color: #707070;
  color: white;
  padding: 10px;
  text-align: left;
}

.canvas-container {
  width: 27vw;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
}
</style>
