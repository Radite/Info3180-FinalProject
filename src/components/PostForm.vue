<template>
  <div class="container">
    <form @submit.prevent="submitForm">
      <label for="caption">Caption:</label>
      <input type="text" id="caption" v-model="caption">

      <label for="photo">Photo/Video:</label>
      <input type="file" id="photo" accept="image/*, video/*" @change="onFileChange">

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      caption: '',
      photo: null,
      USER_ID: null,
      error: ''
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.USER_ID = decodedToken.user_id;
    }
  },
  methods: {
    async submitForm() {
      if (!this.photo || !this.allowedFile(this.photo.name)) {
        this.error = 'Invalid file. Please upload a valid photo/video.';
        return;
      }

      const formData = new FormData();
      formData.append('caption', this.caption);
      formData.append('photo', this.photo);

      try {
        const token = localStorage.getItem('token');
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
        setTimeout(() => {
          console.log('Redirecting...');
          this.$router.push('/explore');
        }, 1000);
      } catch (error) {
        console.error(error);
      }
    },
    onFileChange(event) {
      this.photo = event.target.files[0];
    },
    allowedFile(filename) {
      const allowedExtensions = ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'];
      const extension = filename.split('.').pop().toLowerCase();
      return allowedExtensions.includes(extension);
    }
  },
};
</script>

<style scoped>
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

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
}

button {
  padding: 10px 15px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  margin-bottom: 20px;
}
</style>
