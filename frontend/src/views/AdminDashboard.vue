<template>
  <div class="d-flex">
    
    <div class="sidebar bg-dark text-white p-3">
      <h4 class="text-center">Admin Panel</h4>
      <ul class="nav flex-column">
        <li
          class="nav-item"
          v-for="(section, key) in sections"
          :key="key"
          @click="selectedSection = key"
        >
          <a
            class="nav-link"
            :class="{ active: selectedSection === key }"
            href="#"
          >
            {{ section }}
          </a>
        </li>
      </ul>
    </div>

    
    <div class="content p-4">
      <div v-if="selectedSection === 'professionals'">
        <h3>Professionals</h3>
        <input v-model="searchQuery" class="form-control mb-2" placeholder="Search Professional" />
        <button @click="searchProfessionals" class="btn btn-primary">Search</button>
        <table class="table mt-3">
          <thead><tr><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="pro in professionals" :key="pro.email">
              <td>{{ pro.full_name }}</td>
              <td>{{ pro.email }}</td>
              <td>{{ pro.status }}</td>
              <td>{{ pro.approved ? 'Approved' : 'Pending' }}</td>
              <td>
                <button v-if="!pro.approved" @click="approveProfessional(pro.email)" class="btn btn-success">Approve</button>
                <button v-if="!pro.approved" @click="rejectProfessional(pro.email)" class="btn btn-danger">Reject</button>
                <button v-if="pro.status !== 'blocked'" @click="blockProfessional(pro.email)" class="btn btn-warning">Block</button>
                <button v-if="pro.status === 'blocked'" @click="unblockProfessional(pro.email)" class="btn btn-secondary">Unblock</button>
 </td>

            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="selectedSection === 'customers'">
        <h3>Customers</h3>
        <table class="table">
          <thead><tr><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="cust in customers" :key="cust.email">
              <td>{{ cust.full_name }}</td>
              <td>{{ cust.email }}</td>
              <td>{{ cust.status }}</td>
              <td>
                <button v-if="cust.status !== 'blocked'" @click="blockUser(cust.email)" class="btn btn-danger">Block</button>
                <button v-else @click="unblockUser(cust.email)" class="btn btn-success">Unblock</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="selectedSection === 'services'">
        <h3>Services</h3>
        <div>
    <button @click="refreshCache">Refresh Cache</button>
  </div>
        <table class="table">
          <thead><tr><th>Name</th><th>Base Price</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.name }}</td>
              <td>₹{{ service.base_price }}</td>
              <td>
                <button @click="openEditForm(service)" class="btn btn-warning">Edit</button>
                <button @click="deleteService(service.id)" class="btn btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="showEditForm">
          <h4>Edit Service</h4>
          <input v-model="editServiceData.name" class="form-control mb-2" placeholder="Service Name" />
          <input v-model="editServiceData.base_price" type="number" class="form-control mb-2" placeholder="Base Price" />
          <input v-model="editServiceData.description" class="form-control mb-2" placeholder="Description" />
          <input v-model="editServiceData.pin_code" type="number" class="form-control mb-2" placeholder="Pin Code" />
          <button @click="updateService" class="btn btn-primary">Update</button>
          <button @click="showEditForm = false" class="btn btn-secondary">Cancel</button>
        </div>

        <h4>Create Service</h4>
        <input v-model="newService.name" class="form-control mb-2" placeholder="Service Name" />
        <input v-model="newService.base_price" type="number" class="form-control mb-2" placeholder="Base Price" />
        <input v-model="newService.description" class="form-control mb-2" placeholder="Description" />
        <input v-model="newService.pin_code" type="number" class="form-control mb-2" placeholder="Pin Code" />
        <button @click="createService" class="btn btn-success">Create</button>
      </div>

      <div v-if="selectedSection === 'summary'">
        <h3>Admin Summary</h3>
        <ul class="list-group">
          <li class="list-group-item"><strong>Pending:</strong> {{ summary.Pending }}</li>
          <li class="list-group-item"><strong>Assigned:</strong> {{ summary.Assigned }}</li>
          <li class="list-group-item"><strong>Closed:</strong> {{ summary.Closed }}</li>
        </ul>

        <SummaryChart v-if="summary.Pending !== undefined" :summary="summary" />
        <button class="btn btn-primary mt-3" @click="exportCSV">Export CSV</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../api";
import SummaryChart from "@/components/SummaryChart.vue";

export default {
  components: { SummaryChart },
  data() {
    return {
      selectedSection: "professionals", 
      professionals: [],
      customers: [],
      services: [],
      editServiceData: { id: null, name: "", base_price: "", description: "", pin_code: "" },
      showEditForm: false,
      summary: {},
      searchQuery: "",
      newService: { name: "", base_price: "", description: "", pin_code: "" },
      sections: {
        professionals: "Professionals",
        customers: "Customers",
        services: "Services",
        summary: "Summary",
      },
    };
  },
  methods: {
    async fetchDashboardData() {
      const response = await axios.get("/dashboard");
      this.professionals = response.data.professionals;
      this.customers = response.data.customers;
      const servicesResponse = await axios.get("/get_services");
      this.services = servicesResponse.data.services;
    },
    openEditForm(service) {
      this.editServiceData = { ...service }; 
      this.showEditForm = true; 
    },
    async searchProfessionals() {
      const response = await axios.get(`/search_professional?query=${this.searchQuery}`);
      console.log("API Response:", response.data);
      this.professionals = response.data;
    },
    async fetchSummary() {
      const response = await axios.get("/admin_summary");
      this.summary = response.data;
    },
    async exportCSV() {
      try {
        const response = await axios.post("/export");
        alert(response.data.message);
      } catch (error) {
        alert("Export failed!");
      }
    },
    async approveProfessional(email) {
      const pro = this.professionals.find(p => p.email === email);
      if (pro) pro.approved = true;
      await axios.post(`/approve_professional/${email}`);
    },
    async rejectProfessional(email) {
      this.professionals = this.professionals.filter(p => p.email !== email);
      await axios.post(`/reject_professional/${email}`);
    },
    async blockUser(email) {
      const cust = this.customers.find(c => c.email === email);
      if (cust) cust.status = "blocked";
      await axios.post(`/block_user/${email}`);
    },
    async unblockUser(email) {
      const cust = this.customers.find(c => c.email === email);
      if (cust) cust.status = "active";
      await axios.post(`/unblock_customer/${email}`);
    },

    async blockProfessional(email) {
      try {
        await axios.post(`/block_professional/${email}`);
        const pro = this.professionals.find(p => p.email === email);
        if (pro) pro.status = "blocked"; 
      } catch (error) {
        console.error("Error blocking professional:", error);
      }
    },

    async unblockProfessional(email) {
      try {
        await axios.post(`/unblock_professional/${email}`);
        const pro = this.professionals.find(p => p.email === email);
        if (pro) pro.status = "active"; 
      } catch (error) {
        console.error("Error unblocking professional:", error);
      }
    },
    async createService() {
      await axios.post("/create_service", this.newService);
      this.fetchDashboardData();
    },
    async deleteService(serviceId) {
      await axios.delete(`/delete_service/${serviceId}`);
      this.fetchDashboardData();
    },

    async refreshCache() {
      try {
        await axios.post("http://localhost:5000/clear_cache");
        alert("Cache cleared!");
      } catch (error) {
        console.error("Error clearing cache:", error);
      }
    },
    async updateService() {
      try {
        await axios.put(`/update_service/${this.editServiceData.id}`, this.editServiceData);
        this.fetchDashboardData(); 
        this.showEditForm = false; 
      } catch (error) {
        console.error("Error updating service:", error);
      }
    }

  },
  mounted() {
    this.fetchDashboardData();
    this.fetchSummary();
  },
};
</script>

<style scoped>
.d-flex {
  display: flex;
}
.sidebar {
  width: 250px;
  height: 100vh;
  position: fixed;
  top: 50px;
  left: 0;
  background-color: #212529;
  padding-top: 20px;
}
.content {
  margin-left: 270px; 
  width: calc(100% - 270px);
  padding: 20px;
  overflow-x: auto;
}
.nav-link {
  cursor: pointer;
  padding: 10px;
  border-radius: 5px;
}
.nav-link.active {
  background-color: #007bff;
  color: white !important;
}
</style>
