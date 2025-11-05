import { createRouter, createWebHistory } from 'vue-router'
import Home from '../Views/HomeView.vue';
import Login from '../Views/LoginView.vue';
import Signup from '../Views/SignUp.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/login', name: 'login', component: Login },
    { path: '/signup', name: 'signup', component: Signup },

  ],
})

export default router
