<template>
    <div>
        <h3>Configure the Time-Aware Shaper</h3>
        <table cellpadding="" cellspacing="50px" style="width: 55%;">
            <tr>
                <td><b>Number of Slots</b> </td>
                <td><input type="number" v-model="slotCount" min="1" step="1"></td>
            </tr>
        </table>
        <table cellpadding="" cellspacing="50px" style="width: 55%;"> 
            <thead>
                <tr>
                    <th>Slot duration (ns)</th>
                    <th>Slot number</th>
                    <th>Q7</th>
                    <th>Q6</th>
                    <th>Q5</th>
                    <th>Q4</th>
                    <th>Q3</th>
                    <th>Q2</th>
                    <th>Q1</th>
                    <th>Q0</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(index, rowIndex) in slotData" :key="index">
                    <td>
                        <input type="number" v-model="slotData[rowIndex].duration" min="1000" step="1" style="text-align: center;">
                    </td>
                    <td>Slot {{ rowIndex }}</td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q7">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q6">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q5">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q4">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q3">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q2">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q1">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q0">
                    </td>
                </tr>
            </tbody>
        </table>
        <button @click="generateJSON">Send Data</button>
    </div>
</template>

<script setup>
import { ref, inject, watch } from 'vue';

const $wsServices = inject('$wsservices');
const slotCount = ref(1);
const slotData = ref([{ duration: 0, q7: false, q6: false, q5: false, q4: false, q3: false, q2: false, q1: false, q0: false }]);


function generateJSON() {
    let controlList = [];
    // Calculate the number of zeros in the numerator
    let numZeros = 0;
    let numeratorCopy = slotData.value.reduce((acc, cur) => acc + cur.duration, 0);
    while (numeratorCopy % 10 === 0 && numeratorCopy !== 0) {
        numZeros++;
        numeratorCopy /= 10;
        // console.log("num zeros = ", numZeros)
    }

    // Adjust the denominator accordingly
    let denominator = Math.pow(10, 9-numZeros);

    for (let rowIndex = 0; rowIndex < slotData.value.length; rowIndex++) {
        let gateStatesValue = 0;
        for (let i = 0; i < 8; i++) {
            if (slotData.value[rowIndex][`q${i}`]) {
                gateStatesValue |= 1 << i;
            }
        }

        controlList.push({
            index: rowIndex,
            operation_name: "set-gate-states",
            gate_states_value: gateStatesValue,
            time_interval_value: slotData.value[rowIndex].duration
        });
    }

    const json = {
        "qbv_gate_parameters": {
            "gate_enabled": true,
            "admin": {
                "gate_states": 255,
                "control_list_length": slotData.value.length,
                "control_list": controlList,
                "cycle_time": {
                    "numerator": slotData.value.reduce((acc, cur) => acc + cur.duration, 0) / Math.pow(10, numZeros),
                    "denominator": denominator
                },
                "cycle_time_extension": 1000,
                "base_time": {
                    "seconds": 0,
                    "nanoseconds": 0
                }
            },
            "config_change": true
        }
    };
    console.log(JSON.stringify(json, 2, null))

    // Assuming $wsServices is an instance of WebSocket service
    $wsServices.sendTas(json);
}

watch(slotCount, (newValue) => {
    slotData.value = Array.from({ length: newValue }, () => ({ duration: 0, q7: false, q6: false, q5: false, q4: false, q3: false, q2: false, q1: false, q0: false }));
});
</script>

