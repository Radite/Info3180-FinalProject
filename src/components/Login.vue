<template>
  <div class="main-background">
    <div class="container mt-5">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username:</label>
          <input type="text" class="form-control" id="username" v-model="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input type="password" class="form-control" id="password" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8080/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        if (response.ok) {
            const data = await response.json();
            // Store token in local storage
            localStorage.setItem('token', data.token);
            // Redirect to homepage on successful login
            this.$router.push('/');
        
        } else {
          const errorData = await response.json();
          this.errorMessage = errorData.error;
        }
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = 'An error occurred during login. Please try again later.';
      }
    }
  }
};
</script>

<style scoped>
.main-background {
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  align-items: flex-start; /* Aligns the container to the top */
  justify-content: center;
  padding-top: 50px; /* Adds some space at the top */
}

.container {
  background-color: white;
  padding: 2rem;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style>