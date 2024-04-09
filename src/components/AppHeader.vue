<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">VueJS with Flask</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>          
          </ul>
          <button @click="logout" class="btn btn-light">Logout</button> <!-- Logout button -->
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from "vue-router";
import axios from "axios";
const router = useRouter();
// Function to logout the user
const logout = async () => {
  try {
    const token = localStorage.getItem("token"); // Get the token from local storage
    if (!token) {
      console.error("Authentication token is missing");
      return;
    }
    // Call the logout API endpoint
    const response = await axios.post(
      "http://localhost:8080/api/v1/auth/logout",
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the request headers
        },
      }
    );
    // Clear local storage and redirect to the home page
    localStorage.removeItem("token");
    router.push("/");
  } catch (error) {
    console.error("Logout error:", error);
    // Handle logout error
  }
};
</script>

<style>
/* Add any component specific styles here */
</style>