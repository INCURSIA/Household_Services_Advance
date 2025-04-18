<template>
  <div class="container mt-4">
    <h2 class="mb-3">Customer Dashboard</h2>
    
    <div class="mb-3 d-flex">
      <input v-model="query" class="form-control me-2" placeholder="Search services..." />
      <input v-model="pin_code" class="form-control me-2" placeholder="Enter pin code..." />
      <button @click="fetchServices" class="btn btn-primary">Search</button>
    </div>

    <div v-if="statusData" class="row mb-4">
      <div class="col-md-4">
        <div class="card text-white bg-info">
          <div class="card-body text-center">
            <h5>Requested</h5>
            <h3>{{ statusData.requested }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-warning">
          <div class="card-body text-center">
            <h5>Assigned</h5>
            <h3>{{ statusData.assigned }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success">
          <div class="card-body text-center">
            <h5>Closed</h5>
            <h3>{{ statusData.closed }}</h3>
          </div>
        </div>
      </div>
    </div>

    <h3>Available Services</h3>
    <div class="row">
      <div v-for="service in services" :key="service.id" class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <button @click="toggleProfessionalList(service.id)" class="btn btn-primary">
              Request Service
            </button>

            
            <div v-if="selectedServiceId === service.id && professionals.length > 0" class="mt-3">
              <h6>Select a Professional</h6>
              <ul class="list-group">
                <li v-for="pro in professionals" :key="pro.email" class="list-group-item d-flex justify-content-between align-items-center">
                  {{ pro.full_name }}
                  <button @click="requestService(service.id, pro.email)" class="btn btn-success btn-sm">Select</button>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </div>

    <h3 class="mt-4">My Requests</h3>
<ul class="list-group">
  <li v-for="request in requests" :key="request.id" class="list-group-item">
    <span>
  <strong>Email:</strong> {{ request.professional_email }} <br>
  <strong>Status:</strong> {{ request.status }} <br>
  <strong>Created On:</strong> {{ new Date(request.date_created).toLocaleString() }}
</span>

    
    <button v-if="request.status !== 'Closed'" @click="closeRequest(request.id)" class="btn btn-danger btn-sm">
      Close
    </button>

    
    <div v-if="request.status === 'Closed' && !request.rating_given" class="mt-2">
      <input v-model="request.rating" type="number" min="1" max="5" class="form-control" placeholder="Rate 1-5" />
      <input v-model="request.remark" type="text" class="form-control mt-2" placeholder="Add a remark..." />
      <button @click="submitRating(request.id, request.rating, request.remark)" class="btn btn-primary btn-sm mt-2">
        Submit Rating
      </button>
    </div>

    
    <div v-if="request.status === 'Closed' && request.rating_given" class="mt-2">
      <strong>Rating:</strong> ⭐{{ request.rating }}/5
      <br>
      <strong>Remark:</strong> {{ request.remarks || "No remarks added." }}
    </div>
  </li>
</ul>

<div class="chart-container">
      <h3>Service Request Summary</h3>
      <BarChart :chartData="statusData" />
    </div>

  </div>
</template>

<script>
import axios from "axios";
import BarChart from "@/components/BarChart.vue";

export default {
  components: { BarChart },
data() {
  return {
    query: "",
    pin_code: "",
    services: [],
    requests: [],
    statusData: { requested: 0, assigned: 0, closed: 0 },
    professionals: [], 
    selectedServiceId: null, 
  };
},
async created() {
  await this.fetchDashboardData();
},
methods: {
  async fetchDashboardData() {
    try {
      const response = await axios.get("http://localhost:5000/customer/dashboard", {
        withCredentials: true,
      });
      this.services = response.data.services || [];
      this.requests = response.data.requests || [];
      this.statusData = response.data.status_data || { requested: 0, assigned: 0, closed: 0 };
    } catch (error) {
      console.error("Error fetching dashboard data:", error.response?.data || error.message);
    }
  },
  async fetchServices() {
    try {
      const response = await axios.get(
        `http://localhost:5000/customer/dashboard?query=${this.query}&pin_code=${this.pin_code}`,
        { withCredentials: true }
      );
      this.services = response.data.services || [];
    } catch (error) {
      console.error("Error fetching services:", error);
    }
  },

  
  async fetchProfessionals(serviceId) {
    try {
      console.log("Fetching professionals for service ID:", serviceId);
      const response = await axios.get(`http://localhost:5000/request_service_view/${serviceId}`, {
        withCredentials: true,
      });

      this.professionals = response.data.professionals;
      this.selectedServiceId = serviceId; 
      console.log("Fetched professionals:", this.professionals);
    } catch (error) {
      console.error("Error fetching professionals:", error);
    }
  },

  
  toggleProfessionalList(serviceId) {
    if (this.selectedServiceId === serviceId) {
      this.selectedServiceId = null;  
      this.professionals = [];
    } else {
      this.fetchProfessionals(serviceId);
    }
  },

  
  async requestService(serviceId, professionalEmail) {
    try {
      const response = await axios.post(`http://localhost:5000/request_service_view/${serviceId}`, {
        professional_email: professionalEmail
      }, { withCredentials: true });

      alert(response.data.message);
      this.fetchDashboardData(); 
    } catch (error) {
      console.error("Error requesting service:", error);
    }
  },
  async submitRating(requestId, rating, remark) {
  if (!rating || rating < 1 || rating > 5) {
    alert("Please provide a valid rating between 1 and 5.");
    return;
  }

  try {
    const response = await axios.post(`http://localhost:5000/add_remark/${requestId}`, {
      rating: rating,
      remark: remark,
    }, { withCredentials: true });

    alert(response.data.message);
    this.fetchDashboardData(); 
  } catch (error) {
    console.error("Error submitting rating:", error);
    alert("Failed to submit rating.");
  }
},

  async closeRequest(requestId) {
    try {
      const response = await fetch(`http://localhost:5000/close_request/${requestId}`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to close request");
      }

      alert(data.message);
      this.fetchDashboardData();
    } catch (error) {
      console.error("Error closing request:", error);
      alert("Error: " + error.message);
    }
  },
},
};
</script>

<style scoped>
.card {
  border-radius: 12px;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.btn-danger {
  width: auto;
  min-width: 80px;
  text-align: center;
}

.btn-success {
  width: auto;
  min-width: 80px;
  padding: 5px 10px;
}

</style>
