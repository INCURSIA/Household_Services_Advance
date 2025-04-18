<template>
    <div>
      
      <section class="hero d-flex flex-column align-items-center justify-content-center text-center">
        <h1 class="display-3 fw-bold animate-fadein">Household Services</h1>
        <p class="fs-5 text-light">Find the best professionals for all your needs in one place.</p>
        <router-link to="/signup" class="btn btn-lg btn-glow mt-3">Get Started</router-link>
      </section>
  
      
      <section class="container my-5">
        <h2 class="text-center fw-bold mb-4 text-gradient">Our Services</h2>
        <div class="row g-4">
          <div v-for="(service, index) in services" :key="index" class="col-md-4">
            <div class="card service-card text-center p-4 animate-slidein">
              <div class="service-icon-container">
                <i :class="service.icon" class="service-icon"></i>
              </div>
              <h5 class="mt-3 fw-semibold text-light">{{ service.name }}</h5>
              <p class="text-light">{{ service.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      
      <footer class="footer text-center mt-5 p-4">
        &copy; 2025 ServicePro - All rights reserved.
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        services: [
          { name: "Plumbing", description: "Reliable plumbing services at your doorstep.", icon: "bi bi-tools" },
          { name: "Cleaning", description: "Professional home & office cleaning services.", icon: "bi bi-brush" },
          { name: "Electrical", description: "Expert electricians for all your needs.", icon: "bi bi-lightning-charge" },
          { name: "Gardening", description: "Get your garden maintained by pros.", icon: "bi bi-tree" },
          { name: "Painting", description: "High-quality painting services for homes & offices.", icon: "bi bi-palette" },
          { name: "Pest Control", description: "Say goodbye to pests with our services.", icon: "bi bi-bug" }
        ]
      };
    }
  };
  </script>
  
  <style scoped>
  
  .hero {
    height: 80vh;
    width: 100%;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
  }
  
  
  .btn-glow {
    background: linear-gradient(45deg, #ff7eb3, #ff758c);
    border: none;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 4px 15px rgba(255, 117, 140, 0.7);
  }
  
  .btn-glow:hover {
    background: linear-gradient(45deg, #ff758c, #ff7eb3);
    transform: scale(1.08);
  }
  
  
  .service-card {
    border-radius: 12px;
    background: #222;
    box-shadow: 0px 6px 15px rgba(255, 75, 90, 0.3);
    transition: all 0.3s ease-in-out;
    border: none;
  }
  
  .service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 20px rgba(255, 75, 90, 0.5);
  }
  
  
  .service-icon-container {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: auto;
    background: linear-gradient(135deg, #ff8a00, #da1b60);
    box-shadow: 0px 0px 15px rgba(218, 27, 96, 0.8);
  }
  
  .service-icon {
    font-size: 40px;
    color: white;
  }
  
  
  .text-gradient {
    background: linear-gradient(45deg, #ff758c, #ff7eb3);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  
  .footer {
    background: #111;
    color: #ddd;
  }
  
  
  .animate-fadein {
    animation: fadeIn 1.2s ease-in-out;
  }
  
  .animate-slidein {
    animation: slideIn 1s ease-in-out;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideIn {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  </style>
  