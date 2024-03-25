<script setup>
import { defineProps } from 'vue';
import HeaderComponent from '@/components/HeaderComponent.vue';
import PlotComponent from '@/components/PlotComponent.vue';
import PlotLidarComponent from '@/components/PlotLidarComponent.vue';

defineProps({
    components:{
        HeaderComponent,
        PlotLidarComponent,
        PlotComponent
    }
})
</script>

<template>
    <div>
        <HeaderComponent title="Interactive Off-the-Shelf TSN Testbed"/>
        <div class="row">
            <div class="col-md-8">
                <div class="grid-item">
                  <div class="d-flex flex-column">
                    <PlotLidarComponent/>
                  </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="grid-item">
                    <PlotComponent/>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.grid-item {
    /* background-color: #f0f0f0; */
    padding: 10px;
    margin-bottom: 20px;
}
</style>


