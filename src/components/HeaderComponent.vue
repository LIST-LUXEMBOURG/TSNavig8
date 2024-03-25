<template>
    <div>
        <header class="d-flex justify-content-between align-items-center">
            <h2>{{ title }}</h2>
            <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                aria-controls="offcanvasRight"> <i class="bi bi-gear-wide"></i></button>

            <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel"
                style="width: 27vw; background-color: rgba(255, 255, 255, 0.5); backdrop-filter: blur(4px);">
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

<script>
import TasComponent from './TasComponent.vue';
import NoiseComponent from './NoiseComponent.vue';

export default {
    props: {
        title: {
            type: String,
            required: true
        }
    },
    components: {
        TasComponent,
        NoiseComponent,
    }
};
</script>

<style scoped>
header {
    background-color: #707070;
    color: white;
    padding: 10px;
    text-align: left;
}
</style>
