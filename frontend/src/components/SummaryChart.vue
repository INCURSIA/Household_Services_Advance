<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);
  
  export default {
    mounted() {
      const ctx = this.$refs.chartCanvas.getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Pending", "Assigned", "Closed"],
          datasets: [
            {
              label: "Jobs Summary",
              data: [this.summary.Pending, this.summary.Assigned, this.summary.Closed],
              backgroundColor: ["#ff6384", "#36a2eb", "#4bc0c0"],
            },
          ],
        },
      });
    },
    props: {
      summary: Object, 
    },
  };
  </script>
  