<template>
    <header>
        <h2>{{ title }}</h2>
    </header>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        }
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