<template>
  <div class="registration-form">
    <h2>Register</h2>
    <form @submit.prevent="registerUser" class="form">
      <div class="form-group">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="formData.username" required>
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="formData.password" required>
        </div>
      </div>
      <div class="form-group">
        <div class="input-group">
          <label for="firstname">First Name</label>
          <input type="text" id="firstname" v-model="formData.firstname" required>
        </div>
        <div class="input-group">
          <label for="lastname">Last Name</label>
          <input type="text" id="lastname" v-model="formData.lastname" required>
        </div>
      </div>
      <div class="form-group">
        <div class="input-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="formData.email" required>
        </div>
        <div class="input-group">
          <label for="location">Location</label>
          <input type="text" id="location" v-model="formData.location">
        </div>
      </div>
      <div class="input-group textarea">
        <label for="biography">Biography</label>
        <textarea id="biography" v-model="formData.biography"></textarea>
      </div>
      <div class="form-group">
        <label for="profile-photo">Profile Photo</label>
        <input type="file" id="profile-photo" @change="onFileChange">
      </div>
      <button type="submit">Register</button>
    </form>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
        firstname: '',
        lastname: '',
        email: '',
        location: '',
        biography: '',
        profile_photo: null
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    registerUser() {
      const formData = new FormData();
      formData.append('username', this.formData.username);
      formData.append('password', this.formData.password);
      formData.append('firstname', this.formData.firstname);
      formData.append('lastname', this.formData.lastname);
      formData.append('email', this.formData.email);
      formData.append('location', this.formData.location);
      formData.append('biography', this.formData.biography);
      formData.append('profile_photo', this.formData.profile_photo);

      axios.post('http://localhost:8080/api/v1/register', formData)
        .then(response => {
          this.formData = {
            username: '',
            password: '',
            firstname: '',
            lastname: '',
            email: '',
            location: '',
            biography: '',
            profile_photo: null
          };
          this.successMessage = response.data.message;
          this.errorMessage = '';
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        })
        .catch(error => {
          if (error.response) {
            this.errorMessage = error.response.data.error;
          } else {
            console.error('Error registering user:', error);
            this.errorMessage = 'An unexpected error occurred';
          }
        });
    },
    onFileChange(event) {
      this.formData.profile_photo = event.target.files[0];
    }
  }
};
</script>

<style scoped>
.registration-form {
  max-width: 600px;
  margin: 0 auto;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  color: #6c757d;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  justify-content: space-between;
}

input[type="text"],
input[type="password"],
input[type="email"],
textarea {
  width: calc(50% - 10px);
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  font-size: 0.875rem;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  font-size: 1rem;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}
</style>
