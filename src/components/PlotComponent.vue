<template>
    <h3>Plot Component</h3>
</template>

<script setup>
import { onMounted, inject, onDeactivated } from "vue";
const $wsThServices = inject('$wstservices')
onMounted(() => {
  $wsThServices.connect()
//   sceneInitialisation()
//   displayPoints()
})

onDeactivated(() => {
  $wsThServices.disconnect();
})
</script>