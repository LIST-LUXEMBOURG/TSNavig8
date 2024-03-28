<script setup>
/* eslint-disable */
import {Chart, registerables} from "chart.js";
import { color } from 'chart.js/helpers'
import 'chartjs-adapter-luxon'
import ChartStreaming from 'chartjs-plugin-streaming';
import {onMounted, ref} from "vue";

// Variables declarations
let canvas = ref(null)
let ctx = ref(null)
let myChart = ref(null)
let chartConfig = null
let chartWidth = ref(null)


function getChartConfig() {
  chartConfig = {
    type: 'line',
    data: {
      datasets: [{
        label: 'Dataset 1 (linear interpolation)',
        backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
        borderColor: chartColors.red,
        fill: false,
        lineTension: 0,
        // borderDash: [8, 4],
        data: []
      }, {
        label: 'Dataset 2 (cubic interpolation)',
        backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
        borderColor: chartColors.blue,
        fill: false,
        cubicInterpolationMode: 'monotone',
        data: []
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Line chart (horizontal scroll) sample'
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'realtime'
        },
        y: {
          scaleLabel: {
            display: true,
            labelString: 'value'
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
        streaming: {
          duration: 15000,
          refresh: 1000,
          delay: 2000,
          onRefresh: onRefresh
        }
      }
    }
  };
  return chartConfig
}

const chartColors = {
  red: 'rgb(255, 99, 132)',
  blue: 'rgb(54, 162, 235)',
};

function randomScalingFactor() {
  return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
}

function onRefresh(chart) {
  chart.config.data.datasets.forEach(function(dataset) {
    dataset.data.push({
      x: Date.now(),
      y: randomScalingFactor()
    });
  });
  chartWidth = document.getElementById("wrapper").offsetWidth
  console.log("wrapper width: " + chartWidth)
  document.getElementById("chart-wrapper").setAttribute("style", "width: " + chartWidth + "px")
}

onMounted(() => {
  canvas = document.getElementById('myChart')
  ctx = canvas.getContext('2d');
  Chart.register(...registerables)
  Chart.register(ChartStreaming)
  myChart = new Chart(ctx, getChartConfig());
  chartWidth = document.getElementById("wrapper").offsetWidth

})
</script>

<template>
  <div class="d-flex flex-column plotchart-container">
    <div class="d-flex flex-column mt-2" id="wrapper">
      <div class="d-flex flex-row justify-content-center mb-4">
        <h3 class="title">Real-Time Bandwidth Utilization</h3>
        <button class="btn btn-primary ms-2" ><i class="bi bi-arrow-clockwise"></i></button>
      </div>
    </div>
    <div class="chart-wrapper" id="chart-wrapper" style="width: 600px">
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
  height: 500px !important;
  padding: 5px;
  margin-top: 31px;
}
#myChart {
  border: 1px solid red;
  padding: 15px;
}
</style>
