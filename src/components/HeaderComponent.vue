<template>
    <div id="header-wrapper">
        <header class="d-flex justify-content-between align-items-center">
            <div>
            <h3 class="title">{{ props.title }}</h3>
            <p class="sub-title">Authors: Darinela Andronovici, Damien Nicolas, Ion Turcanu, and Christoph Sommer</p>
        </div>
            <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                aria-controls="offcanvasRight"> <i class="bi bi-list"></i></button>

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
  /* background-color: #d3c4b2; */
  color: black;
  padding: 5px;
  /* text-align: left; */
  margin-bottom: 10px;
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: normal;
  box-shadow: -3px 6px 22px -3px rgba(0,0,0,0.75);
  -webkit-box-shadow: -3px 6px 22px -3px rgba(0,0,0,0.75);
  -moz-box-shadow: -3px 6px 22px -3px rgba(0,0,0,0.75);
}

.title {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: normal;
}
.sub-title {
  font-family: "Roboto", sans-serif;
  font-weight: 100;
  font-style: normal;
}

.canvas-container {
  width: 27vw;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
}
</style>
