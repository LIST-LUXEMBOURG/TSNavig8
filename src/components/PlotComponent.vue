<template>
    <div ref="plotContainer">
        <h3>This is the Plot component.</h3>
    </div>
  </template>
  
  <script>
  import * as d3 from 'd3';
  
  export default {
    mounted() {
      this.createPlot();
    },
    methods: {
      createPlot() {
        const width = 600;
        const height = 400;
        const originX = width / 2;
        const originY = height / 2;
        const data = [
          { x: 1, y: -305 },
          { x: 82, y: 19 },
          { x: 33, y: 187 },
          { x: 4, y: 12 },
          { x: 500, y: 6 },
          { x: 65, y: 10 }
        ];
  
        const svg = d3.select(this.$refs.plotContainer)
          .append("svg")
          .attr("width", width)
          .attr("height", height);
  
        svg.append('line')
          .attr('x1', 0)
          .attr('y1', originY)
          .attr('x2', width)
          .attr('y2', originY)
          .attr('stroke', 'black')
          .attr('stroke-width', 1);
  
        svg.append('line')
          .attr('x1', originX)
          .attr('y1', 0)
          .attr('x2', originX)
          .attr('y2', height)
          .attr('stroke', 'black')
          .attr('stroke-width', 1);
        svg.selectAll('circle')
          .data(data)
          .enter()
          .append("circle")
          .attr('cx', d => originX + d.x)
          .attr('cy', d => originY - d.y)
          .attr('r', 5) // Increase circle size for better visibility
          .attr('fill', 'steelblue');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add scoped styles if needed */
  </style>
  