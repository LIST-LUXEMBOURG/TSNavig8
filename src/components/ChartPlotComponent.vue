<script setup>
/* eslint-disable */
import { Chart, registerables } from "chart.js";
import { color } from 'chart.js/helpers'
import 'chartjs-adapter-luxon'
import ChartStreaming from 'chartjs-plugin-streaming';
import { onMounted, ref, onUnmounted, inject } from "vue";

// Variables declarations
let canvas = ref(null)
let ctx = ref(null)
let myChart = ref(null)
let chartConfig = null
let chartWidth = ref(null)
let headerWidth = ref(null)
let lidarWidth = ref(null)
const wsService = inject('$wstservices');
let latestWebSocketData = ref(null);

function getChartConfig() {
  chartConfig = {
    type: 'line',
    data: {
      datasets: [{
        label: 'LiDAR',
        backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
        borderColor: chartColors.red,
        fill: false,
        lineTension: 0,
        // borderDash: [8, 4],
        data: []
      }, {
        label: 'All',
        backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
        borderColor: chartColors.blue,
        fill: false,
        cubicInterpolationMode: 'monotone',
        data: []
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'realtime',
          title: {
            display: true,
            text: 'Time',
            font: {
              size: 18
            }
          },
          ticks: {
            font: {
              size: 18
            }
          }
        },
        y: {
          title: {
            display: true,
            text: 'Mbit/second',
            font: {
              size: 18
            }
          },
          ticks: {
            font: {
              size: 18
            }
          }
        }
      },
      tooltips: {
        mode: 'nearest',
        intersect: false
      },
      hover: {
        mode: 'nearest',
        intersect: false
      },
      plugins: {
        legend: {
          labels: {
            font: {
              size: 18
            }
          }
        },
        streaming: {
          duration: 15000,
          refresh: 1000,
          delay: 2000,
          onRefresh: onRefresh
        },

      }
    }
  };
  return chartConfig
}

const chartColors = {
  red: 'rgb(255, 99, 132)',
  blue: 'rgb(54, 162, 235)',
};

function onMessage(event) {
  const newData = JSON.parse(event.data);
  if (newData.type === "bandwidth_update") {
    latestWebSocketData.value = newData;
  }
}


function updateChartWithWebSocketData(chart) {
  const newData = latestWebSocketData.value;
  if (newData) {
    const currentTime = Date.now();
    chart.config.data.datasets.forEach((dataset, index) => {
      const value = index === 0 ? newData.last_200 : newData.last_all;
      dataset.data.push({ x: currentTime, y: value });
    });
    // console.log("chart ", chart);
    chart.update();
  }
}

function onRefresh(chart) {
  updateChartWithWebSocketData(chart);

  headerWidth = document.getElementById("header-wrapper").offsetWidth
  // console.log("header width: " + headerWidth)
  if (headerWidth > 1400) {
    chartWidth = document.getElementById("wrapper").offsetWidth
    lidarWidth = document.getElementById("lidar-wrapper").offsetWidth
    // console.log("wrapper width: " + chartWidth)
    const newWidth = (headerWidth - lidarWidth) - 10
    document.getElementById("wrapper").setAttribute("style", "width: " + newWidth + "px")
    document.getElementById("chart-wrapper").setAttribute("style", "width: " + newWidth + "px")
  }
  else {
    document.getElementById("wrapper").setAttribute("style", "width: 100%")
    document.getElementById("chart-wrapper").setAttribute("style", "width: 100%")
  }
}

onMounted(() => {
  canvas = document.getElementById('myChart')
  ctx = canvas.getContext('2d');
  Chart.register(...registerables)
  Chart.register(ChartStreaming)
  myChart = new Chart(ctx, getChartConfig());
  // Connect to WebSocket
  wsService.connect();
  wsService.ws.onmessage = onMessage;

})

onUnmounted(() => {
  wsService.disconnect();
})
</script>

<template>
  <div class="d-flex flex-column plotchart-container" id="wrapper">
    <div class="d-flex flex-column mt-2">
      <div class="d-flex flex-row justify-content-center mb-4">
        <h3 class="title">Real-Time Bandwidth Utilization</h3>
        <!-- <button class="btn btn-primary ms-2" ><i class="bi bi-arrow-clockwise"></i></button> -->
      </div>
    </div>
    <div class="chart-wrapper" id="chart-wrapper">
      <canvas id="myChart"></canvas>
    </div>
  </div>
</template>

<style scoped>
.title {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.plotchart-container {
  width: 100%
}

.chart-wrapper {
  display: flex;
  flex-direction: row;
  position: relative;
  height: 650px !important;
  padding: 5px;
  margin-top: 31px;
}

#myChart {
  /* border: 1px solid red; */
  padding: 15px;
}
</style>
