<script setup>
import { defineProps } from 'vue';
// import WebSocketHandler2 from '@/components/WebSocketHandler2.vue';
// import PlotComponent from '@/components/PlotComponent.vue';
import PlotLidarComponent from '@/components/PlotLidarComponent.vue';

defineProps({
    title:{
        type: String,
        required: true
    },
    components:{
        // PlotComponent,
        // WebSocketHandler2,
        PlotLidarComponent
    }
})
</script>

<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <div class="grid-item">
                    <h1>{{ title }}</h1>
                    <PlotLidarComponent/>
                </div>
            </div>

/
        </div>

<!--        <div class="row">-->
<!--            <div class="col-6">-->
<!--                <div class="grid-item">-->
<!--                    <h3>Text</h3>-->
<!--                    &lt;!&ndash; Additional child component or content &ndash;&gt;-->
<!--                </div>-->
<!--            </div>-->

<!--            <div class="col-6">-->
<!--                <div class="grid-item">-->
<!--                    &lt;!&ndash; Additional child component or content &ndash;&gt;-->
<!--                    <PlotComponent />-->
<!--                </div>-->
<!--            </div>-->
<!--        </div>-->
    </div>
</template>

<style scoped>
.grid-item {
    background-color: #f0f0f0;
    padding: 10px;
    margin-bottom: 20px;
}
</style>


