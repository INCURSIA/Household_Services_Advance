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
        if (chartInstance) {
          chartInstance.destroy(); 
        }
  
        const ctx = chartCanvas.value.getContext("2d");
  
        
        const gradientBlue = ctx.createLinearGradient(0, 0, 0, 400);
        gradientBlue.addColorStop(0, "#4facfe");
        gradientBlue.addColorStop(1, "#00f2fe");
  
        const gradientOrange = ctx.createLinearGradient(0, 0, 0, 400);
        gradientOrange.addColorStop(0, "#ff9966");
        gradientOrange.addColorStop(1, "#ff5e62");
  
        const gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
        gradientGreen.addColorStop(0, "#38ef7d");
        gradientGreen.addColorStop(1, "#11998e");
  
        chartInstance = new Chart(chartCanvas.value, {
          type: "bar",
          data: {
            labels: ["Requested", "Assigned", "Closed"],
            datasets: [
              {
                label: "Service Requests",
                data: [
                  props.chartData.requested,
                  props.chartData.assigned,
                  props.chartData.closed,
                ],
                backgroundColor: [gradientBlue, gradientOrange, gradientGreen],
                borderRadius: 10, 
                borderWidth: 1,
                hoverBackgroundColor: ["#3b8ff3", "#e86542", "#2ab673"],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                labels: {
                  color: "#444",
                  font: {
                    size: 14,
                    weight: "bold",
                  },
                },
              },
              tooltip: {
                backgroundColor: "#fff",
                titleColor: "#333",
                bodyColor: "#444",
                borderColor: "#ccc",
                borderWidth: 1,
                bodyFont: { size: 14 },
                titleFont: { weight: "bold" },
                padding: 10,
                boxPadding: 5,
                cornerRadius: 8,
              },
            },
            scales: {
              x: {
                ticks: {
                  color: "#555",
                  font: {
                    size: 14,
                  },
                },
                grid: {
                  display: false,
                },
              },
              y: {
                ticks: {
                  color: "#555",
                  font: {
                    size: 14,
                  },
                },
                grid: {
                  color: "rgba(200, 200, 200, 0.2)",
                  borderDash: [5, 5],
                },
              },
            },
            animation: {
              duration: 1500,
              easing: "easeOutBounce",
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
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  