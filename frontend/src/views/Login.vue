<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow-lg" style="max-width: 400px; width: 100%">
      <h3 class="text-center mb-3">Login</h3>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" placeholder="Enter email" />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" placeholder="Enter password" />
      </div>
      <div class="mb-3">
        <label class="form-label">Role</label>
        <select v-model="role" class="form-select">
          <option value="Customer">Customer</option>
          <option value="Professional">Professional</option>
          <option value="Admin">Admin</option>
        </select>
      </div>
      <button @click="login" class="btn btn-primary w-100">Login</button>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      email: "",
      password: "",
      role: "Customer", 
      errorMessage: "",
    };
  },
  methods: {
    async login() {
  try {
    const response = await api.post("/api/login", {
      email: this.email,
      password: this.password,
      role: this.role,
    });

    console.log("Login successful:", response.data);

    
    const routes = {
      Customer: "/customer/dashboard",
      Professional: "/professional/dashboard",
      Admin: "/admin/dashboard",
    };
    
    this.$router.push(routes[response.data.role] || "/");
  } catch (error) {
    console.error("Login failed:", error);

    if (error.response) {
      if (error.response.status === 403) {
        this.errorMessage = "Your account is blocked. Contact admin.";
      } else if (error.response.status === 401) {
        this.errorMessage = "Invalid email or password.";
      } else {
        this.errorMessage = "An unexpected error occurred. Try again later.";
      }
    } else {
      this.errorMessage = "Network error. Please check your connection.";
    }
  }
}
}};
</script>