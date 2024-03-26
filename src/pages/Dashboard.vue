<script setup>
// import { defineProps } from 'vue';
import HeaderComponent from '@/components/HeaderComponent.vue';
// import PlotComponent from '@/components/PlotComponent.vue';
// import PlotLidarComponent from '@/components/PlotLidarComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import MainContent from "@/components/MainContent.vue";

// defineProps({
//     components: {
//         HeaderComponent,
//         PlotLidarComponent,
//         PlotComponent,
//         FooterComponent
//     }
// })
</script>

<template>
    <div class="container-fluid">
      <div class="d-flex flex-column">
        <HeaderComponent title="Interactive Off-the-Shelf In-Car TSN Testbed" />
        <MainContent />
<!--        <div class="main-content-container">-->
<!--        <div class="row">-->
<!--          <div class="col-md-7">-->
<!--            <div class="grid-item">-->
<!--              <div class="d-flex flex-column">-->
<!--                <PlotLidarComponent />-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--          <div class="col-md-5">-->
<!--            <div class="grid-item">-->
<!--&lt;!&ndash;              <PlotComponent />&ndash;&gt;-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--        </div>-->
        <FooterComponent />
      </div>
    </div>
  </template>



<style scoped>
.grid-item {
    //background-color: cadetblue;
  border: 2px solid cadetblue;
    padding: 10px;
    margin-bottom: 20px;
}
.main-content-container {
  box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
  -webkit-box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
  -moz-box-shadow: -3px -1px 38px -1px rgba(0,0,0,0.73);
}
</style>
