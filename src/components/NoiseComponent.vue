<template>
    <div style="margin-top: 2%;">
        <h3>Configure the Traffic Generator</h3>
        <table cellpadding="" cellspacing="50px" style="width: 100%;"> 
            <thead>
                <tr >
                    <th >Frame Size (Bytes)</th>
                    <th>Priority Code Point</th>
                    <th>Transmission rate (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr >
                    <td >
                        <input type="number" min="60" max="1518" v-model="frameSize" style="width: 150px;">
                    </td>
                    <td >
                        <input type="number" min="0" max="7" v-model="priorityCodePoint" style="width: 150px;">
                    </td>
                    <td >
                        <input type="number" min="1" max="100" v-model="transmissionRate" style="width: 150px;">
                    </td>
                    
                </tr>
            </tbody>
        </table>
        <button @click="configure" style="margin-top: 2%;">Configure</button>
    </div>
</template>

<script setup>
    import { ref, inject } from 'vue';

    const frameSize = ref(0);
    const priorityCodePoint = ref(0);
    const transmissionRate = ref(0);
    const $wsServices = inject('$wsservices');

    function configure() {
        // Retrieve the values inserted by the user
        const size = parseInt(frameSize.value);
        const priority = parseInt(priorityCodePoint.value);
        const rate = parseInt(transmissionRate.value);

        // Validate the values
        if (size < 60 || size > 1518) {
            alert("Frame Size must be between 60 and 1518 bytes");
            return;
        }
        if (priority < 0 || priority > 7) {
            alert("Priority Code Point must be between 0 and 7");
            return;
        }
        if (rate < 1 || rate > 100) {
            alert("Transmission Rate must be between 1 and 100%");
            return;
        }
        $wsServices.configureNoise("--frame_size " + size + " -p " + priority + " -pr " + rate)
    }
</script>
