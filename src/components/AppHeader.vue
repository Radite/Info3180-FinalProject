<template>
  <head>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
  </head>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <div class="container-fluid">
        <h1 class="instagram-font smaller-logo"><i class="fas fa-camera smaller-icon"></i> <span class="underline"></span> <span class="photogram-text">Photogram</span></h1>
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
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/explore" class="nav-link">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="`/users/${userId}`" class="nav-link">My Profile</RouterLink> <!-- My Profile link -->
            </li>
            <li class ="nav-item">
              <a v-if="!isAuthenticated" href="/login" class="nav-link">Login</a>
              <a v-else @click="logout" class="nav-link">Logout</a> <!-- Logout link -->
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from "vue-router";
import axios from "axios";
const router = useRouter();
import { jwtDecode } from "jwt-decode";
import debounce from 'lodash/debounce';

let userId = null;
let isAuthenticated = false;
let logoutTimer;

// Decode the token and set userId
const decodeToken = () => {
  const token = localStorage.getItem("token");
  if (token) {
    const decodedToken = jwtDecode(token);
    userId = decodedToken.user_id;
    isAuthenticated = true;
  } else {
    isAuthenticated = false;
  }
};
decodeToken();
// console.log(userId)

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
    isAuthenticated = false;
    router.push("/");
  } catch (error) {
    console.error("Logout error:", error);
    // Handle logout error
  }
};

//Timer function to auto-logout user after period of inactivity
const logoutTiming = () => {
  const logoutTime = 30 * 60 * 1000;

  clearTimeout(logoutTimer);
  console.log('timer running');
  logoutTimer = setTimeout(() => {
    logout();
  }, logoutTime)
}

//debounce throttles the amount of times the auto-logout funtion is called.
const runLogoutTimer = debounce(() => {
  logoutTiming();
}, 10000)

document.addEventListener("mousemove", runLogoutTimer);
document.addEventListener("keypress", runLogoutTimer);



</script>

<style>
/* Smaller camera icon and logo text */
.smaller-icon {
  font-size: 20px; /* Adjust the font size as needed */
}

.smaller-logo {
  font-size: 24px; /* Adjust the font size as needed */
}

/* White photogram text */
.photogram-text {
  color: white;
  font-family: 'Lucida Handwriting', cursive; /* Set font family */
  font-size: 18px; /* Set font size */
  font-weight: bold; /* Set font weight */
  position: relative; /* Set relative positioning */
}

/* Align list items to the right */
.navbar-nav {
  margin-left: auto;
}

nav {
  background-color: #4a90e2;
}

/* Make list items inline and adjust margin */
.nav-item {
  display: inline-block;
  margin-right: 10px; /* Adjust the margin as needed */
}

/* Set cursor pointer for navigation links */
.nav-link {
  cursor: pointer;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
