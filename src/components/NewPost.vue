<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      caption: '',
      photo: null,
      USER_ID: null // initialize USER_ID as null
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.USER_ID = decodedToken.user_id; // set USER_ID to the user_id from the decoded token
    }
  },
  methods: {
    async submitForm() {
      const formData = new FormData();
      formData.append('caption', this.caption);
      formData.append('photo', this.photo);

      try {
        const token = localStorage.getItem('token'); // Retrieve token from localStorage
        if (!this.USER_ID) {
          console.error('User ID is missing');
          return;
        }
        const response = await axios.post(`http://localhost:8080/api/v1/users/${this.USER_ID}/posts`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${token}`
          },
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
    onFileChange(event) {
      this.photo = event.target.files[0];
    }
  },
};

</script>

<template>
  <div class="container">
    <form @submit.prevent="submitForm">
      <label for="caption">Caption:</label>
      <input type="text" id="caption" v-model="caption">

      <label for="photo">Photo:</label>
      <input type="file" id="photo" @change="onFileChange">

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 500px;
  margin: 0 auto;
}

form {
  background-color: #fff;
  box-shadow: 0px 0px 8px #aaa;
  padding: 20px;
  margin-top: 20px;
}

form label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

form input[type="text"],
form input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
}

form button {
  padding: 10px 15px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  cursor: pointer;
}

form button:hover {
  background-color: #0056b3;
}
</style>
