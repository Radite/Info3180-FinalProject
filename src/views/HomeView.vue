import { routerLink } from 'vue-router';

<template>
  <head>
    <!-- Other head elements -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
  </head>

  <div class="container">
    <!-- Left card with image -->
    <div class="card">
      <div class="image-section">
        <img src="/assets/main-image.jpg" alt="Main Image" />
      </div>
    </div>
    
    <!-- Right card with title, message, and buttons -->
    <div class="card">
      <div class="content">
        <h1 class="instagram-font"><i class="fas fa-camera"></i> <span class="underline"></span> <span class="photogram-text">Photogram</span></h1>
        <p>{{ photogramMessage }}</p>
        <div class="button-container">
        <router-link to="/register" class="register-button">Register</router-link>
        <router-link to="/login" class="login-button">Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const photogramMessage = ref("Share your favorite moments with friends, family, and the world.");
</script>

<style scoped>
/* Styles for the container */
.container {
  margin-top: 80px; /* Add margin to the top */
  display: flex; /* Display items as flex */
  width: 1000px; /* Set the width of the container */
}

/* Styles for the cards */
.card {
  flex: 1; /* Make the cards flex items */
  height: 350px; /* Set the height of the card */
  overflow: hidden; /* Prevent overflow of content */
  display: flex; /* Make the image section fill the height of the card */
}

/* Styles for the image section */
.image-section {
  width: 100%; /* Set the width to 100% */
  height: 100%; /* Make the image section take up full height of the card */
}

/* Styles for the image */
.image-section img {
  width: 100%; /* Make the image take up full width */
  height: 100%; /* Make the image take up full height */
  object-fit: cover; /* Cover the entire space of its parent */
}

/* Styles for the first card */
.card:first-child {
  border-right: 12px solid #f0f0f0; /* Add right border with color */
}

/* Styles for the content */
.content {
  padding: 20px; /* Add padding for spacing */
  text-align: center; /* Center-align text */
  margin-top: 20px; /* Add margin to the top */
}

/* Styles for the button container */
.button-container {
  display: flex; /* Display buttons as flex */
  justify-content: center; /* Center-align buttons */
  margin-top: 80px; /* Add margin to the top */
}

/* Styles for the register button */
.register-button {
  background-color: #7ed321; /* Set background color */
  color: white; /* Set text color */
  border: none; /* Remove border */
  padding: 10px 20px; /* Add padding */
  margin-right: 10px; /* Add margin to the right */
  cursor: pointer; /* Add pointer cursor */
  width: 200px; /* Set width of button */
  border-radius: 5px; /* Add border radius */
}

/* Styles for the login button */
.login-button {
  background-color: #4a90e2; /* Set background color */
  color: white; /* Set text color */
  border: none; /* Remove border */
  padding: 10px 20px; /* Add padding */
  cursor: pointer; /* Add pointer cursor */
  width: 200px; /* Set width of button */
  border-radius: 5px; /* Add border radius */
}

/* Font face styles */
@font-face {
  font-family: 'Billabong'; /* Set font family */
  src: url('path-to-your-font/Billabong.ttf'); /* Define font source */
}

/* Styles for the Instagram font */
.instagram-font {
  font-family: 'Billabong', cursive; /* Set font family */
  font-size: 28px; /* Set font size */
  font-weight: bold; /* Set font weight */
  position: relative; /* Set relative positioning */
}

/* Styles for the underline */
.underline {
  position: absolute; /* Position absolutely */
  bottom: 0; /* Align to the bottom */
  left: 0; /* Align to the left */
  width: 100%; /* Set width to 100% */
  height: 1px; /* Set height */
  background-color: #ccc; /* Set background color */
}

/* Styles for the photogram text */
.photogram-text {
  position: relative; /* Set relative positioning */
  z-index: 1; /* Set z-index */
}

/* Styles for the register and login buttons */
.register-button,
.login-button {
  text-decoration: none; /* Remove underline */
}
</style>
