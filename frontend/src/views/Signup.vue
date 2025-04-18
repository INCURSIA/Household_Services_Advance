<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow-lg p-4" style="max-width: 450px; width: 100%;">
      <h2 class="text-center mb-4 text-primary">Sign Up</h2>

      <form @submit.prevent="signup">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input v-model="full_name" type="text" class="form-control" placeholder="Enter your name" required />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            <input v-model="email" type="email" class="form-control" placeholder="Enter your email" required />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input v-model="password" type="password" class="form-control" placeholder="Create a password" required />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Role</label>
          <select v-model="role" class="form-select" required>
            <option value="Customer">Customer</option>
            <option value="Professional">Professional</option>
          </select>
        </div>

        <div v-if="role === 'Professional'">
          <div class="mb-3">
            <label class="form-label">Service</label>
            <select v-model="service_name" class="form-select" required>
              <option disabled value="">Select a Service</option>
              <option v-for="service in servicesList" :key="service.name" :value="service.name">
                {{ service.name }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-geo-alt"></i></span>
              <input v-model="address" type="text" class="form-control" placeholder="Enter your address" required />
            </div>
          </div>
        </div>

        <button type="submit" class="btn btn-primary w-100">Sign Up</button>
      </form>

      <p v-if="message" class="text-center mt-3 text-danger">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      full_name: "",
      email: "",
      password: "",
      role: "Customer",
      service_name: "",
      address: "",
      servicesList: [
        { name: "Plumbing" },
        { name: "Gardening" },
        { name: "Painting" },
        { name: "Electrical" },
        { name: "Cleaning" },
        { name: "Pest Control" },
        { name: "AC Servicing" }
      ],
      message: ""
    };
  },
  methods: {
    async signup() {
      try {
        const payload = {
          full_name: this.full_name,
          email: this.email,
          password: this.password,
          role: this.role,
        };

        if (this.role === "Professional") {
          payload.service_name = this.service_name;
          payload.address = this.address;
        }

        const response = await axios.post("http://127.0.0.1:5000/api/signup", payload);
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data?.error || "Signup failed!";
      }
    }
  }
};
</script>

<style scoped>

.card {
  border-radius: 12px;
  background: #fff;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
}

.input-group-text {
  background: #f1f1f1;
  border-right: 0;
}

.form-control {
  border-left: 0;
}

/* Button animation */
.btn-primary {
  transition: 0.3s;
}

.btn-primary:hover {
  background: #0056b3;
}
</style>
