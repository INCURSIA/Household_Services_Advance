<template>
    <div style="width: 400px; height: 400px;">
      <canvas ref="pieChartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, PieController, ArcElement, Tooltip, Legend } from 'chart.js';
  
  Chart.register(PieController, ArcElement, Tooltip, Legend);
  
  export default {
    props: {
      chartData: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        chartInstance: null
      };
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        if (this.chartInstance) {
          this.chartInstance.destroy(); 
        }
  
        const ctx = this.$refs.pieChartCanvas;
  
        this.chartInstance = new Chart(ctx, {
          type: 'pie',
          data: this.chartData, 
          options: {
  responsive: true,
  maintainAspectRatio: false, 
  plugins: {
    legend: {
      display: true,
      position: 'bottom', 
      labels: {
        padding: 20, 
        boxWidth: 20, 
        font: {
          size: 14 
        }
      }
    }
  }
}

        });
      }
    },
    watch: {
      chartData: {
        deep: true,
        handler() {
          this.renderChart();
        }
      }
    },
    beforeUnmount() {
      if (this.chartInstance) {
        this.chartInstance.destroy(); 
      }
    }
  };
  </script>
  