<script setup>
import PlotLidarComponent from "@/components/PlotLidarComponent.vue";
import PlotComponent from "@/components/PlotComponent.vue";

</script>

<template>
  <div class="main-content-container">
    <PlotLidarComponent />
    <PlotComponent />
  </div>
</template>

<style scoped>
.main-content-container {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
  -webkit-box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
  -moz-box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
}

@media screen and (max-width: 1540px) {
  .main-content-container {
    display: flex;
    flex-direction: column;
    box-shadow: -3px -1px 38px -1px rgba(0, 0, 0, 0.73);
    -webkit-box-shadow: -3px -1px 38px -1px rgba(0, 0, 0, 0.73);
    -moz-box-shadow: -3px -1px 38px -1px rgba(0, 0, 0, 0.73);
  }
}
</style>
