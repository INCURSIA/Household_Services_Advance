<template>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from "vue";
  import Chart from "chart.js/auto";
  
  export default {
    props: {
      chartData: Object, 
    },
    setup(props) {
      const chartCanvas = ref(null);
      let chartInstance = null;
  
      const renderChart = () => {
        if (!props.chartData) return;
        if (chartInstance) chartInstance.destroy();
        
        const ctx = chartCanvas.value.getContext("2d");
  
        chartInstance = new Chart(ctx, {
          type: "bar",
          data: {
            labels: ["Requested", "Assigned", "Closed"],
            datasets: [
              {
                label: "Service Requests",
                data: [props.chartData.requested, props.chartData.assigned, props.chartData.closed],
                backgroundColor: ["#4facfe", "#ff9966", "#38ef7d"],
                borderRadius: 8,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false,
              },
            },
            scales: {
              x: {
                ticks: { color: "#555" },
                grid: { display: false },
              },
              y: {
                ticks: { color: "#555" },
                grid: { color: "rgba(200, 200, 200, 0.2)" },
              },
            },
          },
        });
      };
  
      onMounted(() => {
        renderChart();
      });
  
      watch(() => props.chartData, renderChart, { deep: true });
  
      return { chartCanvas };
    },
  };
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    max-width: 600px;
    height: 350px;
    margin: auto;
    padding: 15px;
    border-radius: 10px;
    background: white;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  