<template>
    <div style="margin-top: 2%;">
        <h5>Traffic Generator Configuration</h5>
        <table cellpadding="" cellspacing="40px" style="width: 100%;">
            <thead>
                <tr>
                    <th>Frame Size (Bytes)</th>
                    <th>Priority Code Point</th>
                    <th>Transmission rate (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <input type="number" min="60" max="1518" v-model="frameSize" value="60" style="width: 120px;" class="form-control">
                    </td>
                    <td>
                        <input type="number" min="0" max="7" v-model="priorityCodePoint" style="width: 120px;" class="form-control">
                    </td>
                    <td>
                        <input type="number" min="1" max="100" v-model="transmissionRate" style="width: 120px;" class="form-control">
                    </td>

                </tr>
            </tbody>
        </table>
        <div id="succMessage" style="display: none; color: green;">Configuration Successful</div>
        <button class="btn btn-success m-2" @click.prevent="configure" style="margin-top: 2%;" id="liveToastBtn">Apply</button>
      <div class="toast-container position-fixed top-0 end-0 p-3">
        <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="5000">
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
import {ref, inject, onMounted} from 'vue';
import { Toast } from 'bootstrap';

const frameSize = ref(60);
const priorityCodePoint = ref(0);
const transmissionRate = ref(1);
const $wsServices = inject('$wscservices');
let configurationTitle = ref('')
let configurationMsg = ref('')
//const toastTrigger = document.getElementById('liveToastBtn')
let toastLiveExample = null
let toastBootstrap = null
let error = ref(false);

function replaceWithBr() {
  let t1 = configurationMsg.value.replace(/\n/g, '<br />');
  let t2 = t1.replace(/\bs/g, '<strong>');
  return t2.replace(/\be/g, '</strong>');
}


function configure() {
    // Retrieve the values inserted by the user
    // const size = parseInt(frameSize);
    // const priority = parseInt(priorityCodePoint.value);
    // const rate = parseInt(transmissionRate.value);

    // Validate the values
  if (frameSize.value < 60 || frameSize.value > 1518) {
    //alert("Frame Size must be between 60 and 1518 bytes");
    error.value = true
    console.log("frameSize: " + frameSize.value)
    configurationMsg.value = "\bsFrame Size\be must be between 60 and 1518 bytes\n"
//    toastBootstrap.show()
//    return;
  }
  if (priorityCodePoint.value < 0 || priorityCodePoint.value > 7) {
    error.value = true
//        alert("Priority Code Point must be between 0 and 7");
    console.log("priorityCodePoint: " + priorityCodePoint.value)
    configurationMsg.value = configurationMsg.value + "\bsPriority Code\be Point must be between 0 and 7\n"
//    toastBootstrap.show()
//    return;
  }
  if (transmissionRate.value < 1 || transmissionRate.value > 100) {
//        alert("Transmission Rate must be between 1 and 100%");
    error.value = true
    console.log("transmissionRate: " + transmissionRate.value)
    configurationMsg.value = configurationMsg.value + "\bsTransmission Rate\be must be between 1 and 100%!\n"
    // toastBootstrap.show()
    // return;
  }

  if (error.value === true) {
    configurationTitle.value = "Incorrect Configuration"
    toastBootstrap.show()
  }  else {
    configurationTitle.value = "Configuration"
    configurationMsg.value = "\bsConfiguration Successfully Applied!\be"
    toastBootstrap.show()


    $wsServices.configureNoise("--frame_size " + frameSize.value + " -p " + priorityCodePoint.value + " -pr " + transmissionRate.value)
    // Clear input fields
    // frameSize.value = 60;
    // priorityCodePoint.value = 0;
    // transmissionRate.value = 1;
  }
}

onMounted(() => {
  toastLiveExample = document.getElementById('liveToast')
  toastBootstrap = Toast.getOrCreateInstance(toastLiveExample)
  toastLiveExample.addEventListener('hidden.bs.toast', () => {
    configurationMsg.value = ''
    error.value = false
  })
})
</script>
