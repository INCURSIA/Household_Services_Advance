<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">House Hold Services</router-link>
  
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Account
              </a>
              <ul class="dropdown-menu">
                <li><router-link class="dropdown-item" to="/login">Login</router-link></li>
                <li><router-link class="dropdown-item" to="/signup">Signup</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Features
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Contact Us</a></li>
                <li><a class="dropdown-item" href="#">About Us</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <button class="btn btn-danger btn-sm ms-2" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();

    const logout = () => {
      console.log("User logged out");

      
      localStorage.removeItem("authToken");

      // Redirect to login page
      router.push("/login");
    };

    return { logout };
  },
};
</script>

  
  <style scoped>
  .navbar-nav .nav-link {
    color: white !important;
  }
  
  .navbar-nav .nav-link:hover {
    color: #f8d210 !important;
  }
  </style>
  