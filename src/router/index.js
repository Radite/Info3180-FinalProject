import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Register from '../components/Register.vue'
import Login from '../components/Login.vue'
import Explore from '../components/Explore.vue'
import UserProfile from '../components/UserProfile.vue'
import NewPost from '../components/NewPost.vue'
import NotFoundView from '../views/NotFoundView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/explore',
      name: 'explore',
      component: Explore,
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:userId',
      name: 'user-profile',
      component: UserProfile,
      meta: { requiresAuth: true }
    },
    {
      path: '/posts/new',
      name: 'new-post',
      component: NewPost,
      meta: { requiresAuth: true }
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView
    }
  ]
})
// Navigation guard to check if the route requires authentication
router.beforeEach((to, from, next) => {
  // Check if the route requires authentication and if the user is authenticated
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('token'); // Check if token exists 

  if (requiresAuth && !isAuthenticated) {
    // If the route requires authentication and the user is not authenticated, redirect to login
    next({ name: 'login' });
  } else {
    // Otherwise, proceed with navigation
    next();
  }
});

export default router
