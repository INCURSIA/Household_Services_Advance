import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/home.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import ProfessionalDashboard from "../views/ProfessionalDashboard.vue";
import CustomerDashboard from "../views/CustomerDashboard.vue";


const routes = [
  { path: "/", component: Home },
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", component: Signup },
  { path: "/admin/dashboard", name: "AdminDashboard", component: AdminDashboard },
  { path: "/professional/dashboard", name: "ProfessionalDashboard", component: ProfessionalDashboard },
  { path: "/customer/dashboard", name: "CustomerDashboard", component: CustomerDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
