<template>
    <div style="margin-top: 10%;" >
        <h5>Time-Aware Shaper Configuration</h5>
        <table cellpadding="" cellspacing="30px" style="width: 100%;">
            <tr>
                <td><b>Number of Slots</b> </td>
                <td><input type="number" v-model="slotCount" min="1" step="1" style="width: 120px;"  class="form-control"></td>
            </tr>
        </table>
        <table cellpadding="" cellspacing="40px" style="width: 100%; margin-top: 2%;">
            <thead>
                <tr>
                    <th>Slot duration (ns)</th>
                    <th>Slot number</th>
                    <th style="text-align: center;">Q7</th>
                    <th style="text-align: center;">Q6</th>
                    <th style="text-align: center;">Q5</th>
                    <th style="text-align: center;">Q4</th>
                    <th style="text-align: center;">Q3</th>
                    <th style="text-align: center;">Q2</th>
                    <th style="text-align: center;">Q1</th>
                    <th style="text-align: center;">Q0</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(index, rowIndex) in slotData" :key="index">
                    <td>
                        <!-- minimum cycle time = 12 500 ns -->
                        <input type="number" v-model="slotData[rowIndex].duration" min="1000" step="1"
                            style="text-align: center; width: 120px;" class="form-control">
                    </td>
                    <td>Slot {{ rowIndex }}</td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q7" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q6" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q5" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q4" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q3" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q2" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q1" class="form-check-input">
                    </td>
                    <td style="text-align: center;">
                        <input type="checkbox" v-model="slotData[rowIndex].q0" class="form-check-input">
                    </td>
                </tr>
            </tbody>
        </table>
<!--        <div id="successMessage" style="display: none; color: green;">Configuration Successful</div>-->
        <button class="btn btn-success m-2" @click.prevent="generateJSON" style="margin-top: 2%;">Apply</button>
        <div class="toast-container position-fixed top-0 end-0 p-3">
        <div id="liveToast2" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="5000">
          <div :class="error ? 'toast-header bg-danger' : 'toast-header bg-success' ">
            <strong class="me-auto">{{  configurationTitle }}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>
          <div class="toast-body">
            <p v-html="replaceWithBr()"></p>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import {ref, inject, watch, onMounted} from 'vue';
import {Toast} from "bootstrap";

const $wsServices = inject('$wsservices');
const slotCount = ref(1);
const slotData = ref([{ duration: 0, q7: false, q6: false, q5: false, q4: false, q3: false, q2: false, q1: false, q0: false }]);
let configurationTitle = ref('')
let configurationMsg = ref('')
let toastLiveExample2 = null
let toastBootstrap = null
let error = ref(false);

function replaceWithBr() {
  let t1 = configurationMsg.value.replace(/\n/g, '<br />');
  let t2 = t1.replace(/\bs/g, '<strong>');
  return t2.replace(/\be/g, '</strong>');
}

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
    let denominator = Math.pow(10, 9 - numZeros);
    if (slotCount.value < 1) {
        // alert("Number of slots must be greater than 0.");
        error.value = true
        configurationMsg.value = "\bsNumber of slots\be must be greater than 0!\n"
    }
    for (let rowIndex = 0; rowIndex < slotData.value.length; rowIndex++) {
        let gateStatesValue = 0;
        for (let i = 0; i < 8; i++) {
            if (slotData.value[rowIndex][`q${i}`]) {
                gateStatesValue |= 1 << i;
            }
        }
        if (slotData.value[rowIndex].duration < 1000) {
            // alert("Slot duration must be greater than 1000 ns.");
          error.value = true
            configurationMsg.value = configurationMsg.value + "\bsSlot duration\be must be greater than 1000 ns!\n"
            // return;
        }

        controlList.push({
            index: rowIndex,
            operation_name: "set-gate-states",
            gate_states_value: gateStatesValue,
            time_interval_value: slotData.value[rowIndex].duration
        });

    }

  if (error.value === true) {
    configurationTitle.value = "Incorrect Configuration"
    toastBootstrap.show()
  }
  else {
    console.log("error = false")
    configurationTitle.value = "Configuration"
    configurationMsg.value = "\bsConfiguration Successfully Applied!\be"
    toastBootstrap.show()
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
    // console.log(JSON.stringify(json, 2, null))
    // Display success message
    // const successMessage = document.getElementById('successMessage');
    // successMessage.style.display = 'block';
    // slotCount.value = 1;
    // slotData.value = [{
    //   duration: 0,
    //   q7: false,
    //   q6: false,
    //   q5: false,
    //   q4: false,
    //   q3: false,
    //   q2: false,
    //   q1: false,
    //   q0: false
    // }];

    // Assuming $wsServices is an instance of WebSocket service
    $wsServices.sendTas(json);
  }
    // Hide success message after 5 seconds
    // setTimeout(() => {
    //     successMessage.style.display = 'none';
    // }, 5000); // 5000 milliseconds = 5 seconds
}

onMounted(() => {
  toastLiveExample2 = document.getElementById('liveToast2')
  toastBootstrap = Toast.getOrCreateInstance(toastLiveExample2)
  toastLiveExample2.addEventListener('hidden.bs.toast', () => {
    configurationMsg.value = ''
    error.value = false
  })
})

watch(slotCount, (newValue) => {
    slotData.value = Array.from({ length: newValue }, () => ({ duration: 0, q7: false, q6: false, q5: false, q4: false, q3: false, q2: false, q1: false, q0: false }));
});
</script>
