<template>
    <div class="container">
        <div class="chart-container">
            <div class="title-row">
                <h3 class="title">Real-Time Bandwidth Utilization</h3>
                <button class="btn btn-primary" @click.prevent="refreshPlot"><i class="bi bi-arrow-clockwise"></i></button>
            </div>
            <div class="svg-row">
                <div class="chart-content">
                    <svg ref="chart"></svg>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { ref, onMounted, onUnmounted, inject } from 'vue'; // Import necessary functions from Vue
import * as d3 from 'd3'; // Import D3.js library

export default {
    setup() {
        const wsService = inject('$wstservices'); // Inject WebSocket service

        const chart = ref(null); // Reference to the SVG element

        let xScale, yScale; // Scales for x and y axes
        let line1, line2; // Line generators for data visualization
        let data = [];

        // Function to initialize the chart
        const initChart = () => {
            const margin = { top: 50, right: 20, bottom: 50, left: 80 }; // Increased bottom margin to accommodate x-axis label
            const fullWidth = window.innerWidth * (1 / 3); // Width as 2/5 of window size
            const fullHeight = window.innerHeight * (2/ 3); // Height as 1/4 of window size

            const width = fullWidth - margin.left - margin.right;
            const height = fullHeight - margin.top ;

            const svg = d3.select(chart.value)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")"); 

            // Append title
            // svg.append("text")
            //     .attr("x", (width + margin.left + margin.right) / 2)
            //     .attr("y", -margin.top / 2) // Position above the plot area
            //     .attr("text-anchor", "middle")
            //     .style("font", "bold 22px arial")
            //     .text("Real-Time Bandwidth Utilization");

            // Define x and y scales
            xScale = d3.scaleLinear().range([0, width]);
            yScale = d3.scaleLinear().range([height, 0]);

            // Define the line generators
            line1 = d3.line()
                .x(d => xScale(d.time))
                .y(d => yScale(d.last_200));

            line2 = d3.line()
                .x(d => xScale(d.time))
                .y(d => yScale(d.last_all));

            // Append x and y axes
            svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScale))
                .append("text")
                .attr("x", width / 2)
                .attr("y", margin.bottom - 10) // Adjusted position below X axis
                .attr("fill", "#000")
                .attr("text-anchor", "middle")
                .text("Time, seconds") // X axis label
                .style("font", "18px arial");

            svg.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(yScale))
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", -margin.left + 5)
                .attr("x", -height / 2)
                .attr("dy", "0.71em")
                .attr("fill", "#000")
                .attr("text-anchor", "middle")
                .text("Mbit/second") // Y axis label
                .style("font", "18px arial");
            
            // Append gridlines for x-axis
            // svg.append("g")
            //     .attr("class", "grid")
            //     .attr("transform", "translate(0," + height + ")")
            //     .call(d3.axisBottom(xScale).tickSize(-height).tickFormat(""))
            //     .selectAll("line")
            //     .attr("stroke", "lightgrey");

            // Append gridlines for y-axis
            svg.append("g")
                .attr("class", "grid")
                .call(d3.axisLeft(yScale).tickSize(-width).tickFormat("")) // Adjust the number of ticks displayed
                .selectAll(".tick")
                .each(function (d, i) {
                    if (i === 0) {
                        d3.select(this).remove(); // Remove the first tick (which overlaps with the x-axis)
                    }
                })
                .selectAll("line")
                .attr("stroke", "lightgrey");


            // Append path elements for lines
            svg.append("path")
                .attr("class", "line1")
                .attr("fill", "none")
                .attr("stroke", "red")
                .attr("stroke-width", 1.5);

            svg.append("path")
                .attr("class", "line2")
                .attr("fill", "none")
                .attr("stroke", "blue")
                .attr("stroke-width", 1.5);

            // Append legend
            const legend = svg.append("g")
                .attr("class", "legend")
                .attr("transform", "translate(" + (width - margin.right - 10) + "," + (margin.top + 10) + ")");

            // Add background rectangle for legend caption
            legend.append("rect")
                .attr("x", -35)
                .attr("y", -20)
                .attr("width", 70)
                .attr("height", 50)
                .attr("fill", "white")
                .attr("stroke", "black");

            // Add text elements for legend
            legend.append("text")
                .attr("x", -30)
                .attr("y", 0)
                .attr("fill", "red")
                .text("LiDAR")
                .style("font", "20px arial");

            legend.append("text")
                .attr("x", -30)
                .attr("y", 20)
                .attr("fill", "blue")
                .text("ALL")
                .style("font", "20px arial");
        };


        // Function to update chart with new data
        const updateChart = () => {
            const svg = d3.select(chart.value).select("g");

            // Update x and y domains
            xScale.domain([0, d3.max(data, d => d.time)]); // Assuming d.time represents time in seconds
            yScale.domain([0, d3.max(data, d => Math.max(d.last_200, d.last_all))]);

            // Select and update x and y axes
            svg.select(".x-axis")
                .call(d3.axisBottom(xScale))
                .selectAll(".tick text")
                .style("font-size", "16px");

            svg.select(".y-axis")
                .call(d3.axisLeft(yScale))
                .selectAll(".tick text")
                .style("font-size", "16px");

            // Update line paths
            svg.select(".line1")
                .attr("d", line1(data));

            svg.select(".line2")
                .attr("d", line2(data));


        };

        const onMessage = event => {
            const newData = JSON.parse(event.data);
            if (newData.type === "bandwidth_update") {
                newData.time = data.length; // Generate time value based on index
                data.push(newData);
                updateChart();
            }
        };
        const refreshPlot = () => {
            // Disconnect WebSocket
            wsService.disconnect();

            // Clear data array
            data = [];

            // Reconnect WebSocket and initialize chart
            wsService.connect();
            wsService.ws.onmessage = onMessage;

            updateChart();
        };
        // Connect to WebSocket on component mount
        onMounted(() => {
            wsService.connect();
            wsService.ws.onmessage = onMessage;
            initChart();
        });

        // Disconnect from WebSocket on component unmount
        onUnmounted(() => {
            wsService.disconnect();
        });

        return { chart, refreshPlot };
    }
};
</script>

<style>
.container {
    display: flex;
    justify-content: center;
}

.chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.title-row {
    display: flex;
    align-items: center;
}

.title {
    margin-right: 10px;
}

</style>