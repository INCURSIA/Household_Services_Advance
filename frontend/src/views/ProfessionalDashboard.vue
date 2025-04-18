<template>
  <div class="dashboard-container">
    
    <div class="sidebar bg-dark text-white p-4">
      <div class="sidebar-header mb-4">
        <h3 class="text-center">
          <i class="fas fa-tachometer-alt me-2"></i>
          Pro Dashboard
        </h3>
        <div class="small text-muted text-center">Service Management System</div>
      </div>
      
      <ul class="nav flex-column sidebar-menu">
        <li class="nav-item mb-2" v-for="section in sections" :key="section.id">
          <a 
            href="#" 
            class="nav-link d-flex align-items-center" 
            :class="{ 'active': currentSection === section.id }"
            @click="currentSection = section.id"
          >
            
            <i class="fas me-3" :class="{
              'fa-chart-pie': section.id === 'summary',
              'fa-clock': section.id === 'pending',
              'fa-tasks': section.id === 'active',
              'fa-check-circle': section.id === 'completed',
              'fa-user-edit': section.id === 'profile'
            }"></i>
            {{ section.name }}
            <span v-if="section.id === 'pending' && pendingRequests.length" class="badge bg-danger ms-auto">{{ pendingRequests.length }}</span>
            <span v-if="section.id === 'active' && activeRequests.length" class="badge bg-primary ms-auto">{{ activeRequests.length }}</span>
          </a>
        </li>
      </ul>
      
      <div class="sidebar-footer mt-auto pt-3 border-top border-secondary">
        <div class="text-center">
          <span class="text-muted small">© 2025 Professional Services</span>
        </div>
      </div>
    </div>

    
    <div class="content p-4">
      <div class="content-header d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">
          <i class="fas me-2" :class="{
            'fa-chart-pie': currentSection === 'summary',
            'fa-clock': currentSection === 'pending',
            'fa-tasks': currentSection === 'active',
            'fa-check-circle': currentSection === 'completed',
            'fa-user-edit': currentSection === 'profile'
          }"></i>
          {{ sections.find(s => s.id === currentSection)?.name }}
        </h2>
      </div>

      <div class="content-body">
        
        <div v-if="currentSection === 'pending'" class="card shadow-sm">
          <div class="card-header bg-light">
            <h5 class="mb-0">Pending Requests</h5>
          </div>
          <div class="card-body p-0">
            <div class="list-group list-group-flush" v-if="pendingRequests.length">
              <div v-for="request in pendingRequests" :key="request.id" class="list-group-item list-group-item-action">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Service ID: {{ request.service_id }}</h6>
                    <p class="mb-1 text-muted">
                      <i class="fas fa-user me-1"></i> {{ request.user_email }}
                    </p>
                  </div>
                  <div class="btn-group">
                    <button class="btn btn-success btn-sm" @click="acceptRequest(request.id)">
                      <i class="fas fa-check me-1"></i> Accept
                    </button>
                    <button class="btn btn-danger btn-sm" @click="rejectRequest(request.id)">
                      <i class="fas fa-times me-1"></i> Reject
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-5">
              <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
              <h5>No pending requests</h5>
            </div>
          </div>
        </div>

        
        <div v-if="currentSection === 'active'" class="card shadow-sm">
          <div class="card-header bg-light">
            <h5 class="mb-0">Active Service Requests</h5>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive" v-if="activeRequests.length">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Service ID</th>
                    <th>Customer</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in activeRequests" :key="request.id">
                    <td><span class="badge bg-primary me-2">ID</span>{{ request.service_id }}</td>
                    <td>{{ request.user_email }}</td>
                    <td>
                      <button class="btn btn-warning btn-sm" @click="closeRequest(request.id)">
                        <i class="fas fa-check-circle me-1"></i> Close Request
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-5">
              <i class="fas fa-hourglass-half text-muted fa-3x mb-3"></i>
              <h5>No active requests</h5>
            </div>
          </div>
        </div>

       
        <div v-if="currentSection === 'completed'" class="card shadow-sm">
  <div class="card-header bg-light">
    <h5 class="mb-0">Completed Requests</h5>
  </div>
  <div class="card-body p-0">
    <div class="table-responsive" v-if="completedRequests.length">
      <table class="table table-striped table-hover mb-0">
        <thead class="table-light">
          <tr>
            <th>Service ID</th>
            <th>Customer</th>
            <th>Status</th>
            <th>Rating</th>
            <th>Remark</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in completedRequests" :key="request.id">
            <td>{{ request.service_id }}</td>
            <td>{{ request.user_email }}</td>
            <td>
              <span :class="'badge ' + (request.status === 'Closed' ? 'bg-success' : 'bg-secondary')">
                {{ request.status }}
              </span>
            </td>
            <td>
              <span v-if="request.rating">{{ request.rating }} ⭐</span>
              <span v-else class="text-muted">No rating</span>
            </td>
            <td>
              <span v-if="request.remarks">{{ request.remarks }}</span>
              <span v-else class="text-muted">No remark</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center py-5">
      <i class="fas fa-clipboard-check text-muted fa-3x mb-3"></i>
      <h5>No completed requests</h5>
    </div>
  </div>
</div>


        
        <div v-if="currentSection === 'profile'" class="row">
          <div class="col-md-4">
            <div class="card shadow-sm mb-4">
              <div class="card-body text-center">
                <div class="avatar-placeholder mb-3">
                  <i class="fas fa-user fa-3x text-muted"></i>
                </div>
                <h5 class="mb-0">{{ profile.full_name || 'Your Name' }}</h5>
                <p class="text-muted">{{ profile.service_name || 'Your Service' }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-8">
            <div class="card shadow-sm">
              <div class="card-header bg-light">
                <h5 class="mb-0">Profile Information</h5>
              </div>
              <div class="card-body">
                <div class="mb-3">
                  <label class="form-label">Full Name</label>
                  <input v-model="profile.full_name" class="form-control" placeholder="Full Name" />
                </div>
                <div class="mb-3">
                  <label class="form-label">Email Address</label>
                  <input v-model="profile.email" class="form-control" placeholder="Email" />
                </div>
                <div class="mb-3">
                  <label class="form-label">Service Name</label>
                  <input v-model="profile.service_name" class="form-control" placeholder="Service Name" />
                </div>
                <button class="btn btn-primary" @click="updateProfile">
                  <i class="fas fa-save me-1"></i> Update Profile
                </button>
              </div>
            </div>
          </div>
        </div>

        
        <div v-if="currentSection === 'summary'" class="row">
          <div class="col-md-4 mb-4">
            <div class="card border-0 bg-primary text-white shadow-sm">
              <div class="card-body d-flex align-items-center">
                <div class="stat-icon-lg bg-white text-primary rounded-circle me-3">
                  <i class="fas fa-clock"></i>
                </div>
                <div>
                  <h3 class="mb-0">{{ pendingRequests.length }}</h3>
                  <div>Pending Requests</div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card border-0 bg-success text-white shadow-sm">
              <div class="card-body d-flex align-items-center">
                <div class="stat-icon-lg bg-white text-success rounded-circle me-3">
                  <i class="fas fa-tools"></i>
                </div>
                <div>
                  <h3 class="mb-0">{{ activeRequests.length }}</h3>
                  <div>Active Requests</div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card border-0 bg-info text-white shadow-sm">
              <div class="card-body d-flex align-items-center">
                <div class="stat-icon-lg bg-white text-info rounded-circle me-3">
                  <i class="fas fa-check-circle"></i>
                </div>
                <div>
                  <h3 class="mb-0">{{ completedRequests.length }}</h3>
                  <div>Completed Requests</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-12">
            <div class="card shadow-sm">
              <div class="card-header bg-light">
                <h5 class="mb-0">Service Overview</h5>
              </div>
              <div class="card-body">
                <div class="alert alert-info" v-if="pendingRequests.length > 0">
                  <i class="fas fa-info-circle me-2"></i> You have <strong>{{ pendingRequests.length }}</strong> pending requests that need your attention.
                </div>
                
                <div class="text-center mt-4" v-if="pendingRequests.length === 0 && activeRequests.length === 0 && completedRequests.length === 0">
                  <i class="fas fa-clipboard text-muted fa-4x mb-3"></i>
                  <h4>No Service Requests Yet</h4>
                  <p class="text-muted">Your service request history will appear here.</p>
                </div>
                <div class="d-flex flex-wrap justify-content-around">
  <div style="width: 45%;">
    <PieChart :chartData="ratingData" />
  </div>
  <div style="width: 45%;">
    <BarChart :chartData="barChartData" />
  </div>
</div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PieChart from '@/components/PieChart.vue';
import BarChart from '@/components/probar.vue';

export default {
  components:{PieChart, BarChart},
  data() {
    return {
      currentSection: "summary", 
      sections: [
        { id: "summary", name: "Summary" },
        { id: "pending", name: "Pending Requests" },
        { id: "active", name: "Active Requests" },
        { id: "completed", name: "Completed Requests" },
        { id: "profile", name: "Update Profile" }
      ],
      pendingRequests: [],
      activeRequests: [],
      completedRequests: [],
      ratingData: {
      labels: ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"],
      datasets: [
        {
          data: [0, 0, 0, 0, 0], 
          backgroundColor: ["#4CAF50", "#8BC34A", "#FFEB3B", "#FF9800", "#F44336"]
        }
      ]
    },
      profile: {
        full_name: "",
        email: "",
        service_name: ""
      }
    };
  },
  computed: {
  barChartData() {
    return {
      requested: this.pendingRequests.length,
      assigned: this.activeRequests.length,
      closed: this.completedRequests.length
    };
  }
},
  async created() {
    await this.fetchDashboardData();
    await this.fetchProfile();
    await this.fetchRatings(); 
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await fetch("http://localhost:5000/professional_dashboard", {
          method: "GET",
          credentials: "include"
        });

        if (!response.ok) throw new Error("Unauthorized or session expired");

        const data = await response.json();
        this.pendingRequests = data.pending_requests;
        this.activeRequests = data.active_requests;
        this.completedRequests = data.completed_requests;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },
    async fetchRatings() {
    try {
      const response = await fetch("http://localhost:5000/professional_ratings", {
        method: "GET",
        credentials: "include"
      });

      if (!response.ok) throw new Error("Failed to fetch ratings");

      const data = await response.json();

      // EXACTLY MATCH THE ORDER FROM BACKEND
      this.ratingData.datasets[0].data = [
        data["5"] || 0,  // 5 Stars first
        data["4"] || 0,  // 4 Stars second
        data["3"] || 0,  // 3 Stars third
        data["2"] || 0,  // 2 Stars fourth
        data["1"] || 0   // 1 Star last
      ];

      console.log("Ratings data updated:", this.ratingData);
    } catch (error) {
      console.error("Error fetching ratings:", error);
    }
  },

    async acceptRequest(requestId) {
      try {
        const response = await fetch(`http://localhost:5000/accept_request/${requestId}`, {
          method: "POST",
          credentials: "include"
        });

        const data = await response.json();
        alert(data.message);
        await this.fetchDashboardData();
      } catch (error) {
        console.error("Error accepting request:", error);
      }
    },

    async rejectRequest(requestId) {
      try {
        const response = await fetch(`http://localhost:5000/reject_request/${requestId}`, {
          method: "POST",
          credentials: "include"
        });

        const data = await response.json();
        alert(data.message);
        await this.fetchDashboardData();
      } catch (error) {
        console.error("Error rejecting request:", error);
      }
    },

    async closeRequest(requestId) {
      try {
        const response = await fetch(`http://localhost:5000/close_request/${requestId}`, {
          method: "POST",
          credentials: "include"
        });

        const data = await response.json();
        alert(data.message);
        await this.fetchDashboardData();
      } catch (error) {
        console.error("Error closing request:", error);
      }
    },

    async fetchProfile() {
      try {
        const response = await fetch("http://localhost:5000/my_profile", {
          method: "GET",
          credentials: "include"
        });

        const data = await response.json();
        this.profile = data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },

    async updateProfile() {
      try {
        const response = await fetch("http://localhost:5000/my_profile", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify(this.profile)
        });

        const data = await response.json();
        alert(data.message);
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    }
  }
};
</script>

<style>
/* Custom Dashboard Styles */
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.sidebar {
  width: 260px;
  min-height: 100vh;
  position: sticky;
  top: 0;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.sidebar-header {
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu .nav-link {
  color: rgba(255, 255, 255, 0.75);
  border-radius: 0.25rem;
  padding: 0.75rem 1rem;
  transition: all 0.2s;
}

.sidebar-menu .nav-link:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-menu .nav-link.active {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
}

.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.card {
  border: none;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.stat-icon-lg {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .dashboard-container {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    min-height: auto;
  }
  .content {
    padding: 1rem;
  }
}
</style>