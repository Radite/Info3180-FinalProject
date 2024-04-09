<template>
  <div class="posts-container">
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <div class="user-profile">
            <img v-if="post.userProfile && post.userProfile.profile_photo" :src="getUserProfilePic(post.userProfile.profile_photo)" class="user-profile-pic" alt="User Profile Pic">
            <span class="username">{{ post.userProfile && post.userProfile.username }}</span>
          </div>
        </div>
        <div class="post-image-container">
          <img :src="getImageUrl(post.photo)" class="post-img" alt="Post">
        </div>
        <div class="post-content">
          <p class="post-caption">{{ post.caption }}</p>
          <div class="post-details">
            <p class="post-likes">{{ post.likes_count }} <i class="like-icon fas fa-heart" :class="{ 'liked': post.liked }" @click="toggleLike(post)"></i> likes</p>
            <p class="post-date">{{ formatDate(post.created_on) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      posts: [],
      error: '',
      USER_ID: null // Initialize USER_ID
    }
  },
  mounted() {
    // Get the user ID from the token
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.USER_ID = decodedToken.user_id; // set USER_ID to the user_id from the decoded token
      // Fetch posts after USER_ID is initialized
      this.fetchPosts();
    }
  },
  methods: {
    fetchPosts() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Authentication token is missing');
        this.error = 'Authentication token is missing';
        return;
      }

      // Fetch posts
      axios.get('http://localhost:8080/api/v1/posts', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          this.posts = response.data.posts;
          this.error = '';

          // Check if the current user has liked each post
          this.checkLikedPosts();
        })
        .catch(error => {
          console.error('Error fetching posts:', error);
          this.error = 'Failed to fetch posts. Please try again later.';
        });
    },
    checkLikedPosts() {
      // Initialize 'liked' property for each post after USER_ID is initialized
      this.posts.forEach(post => {
        // Check if the 'likes' array exists and is not null or undefined
        if (post.likes && post.likes.length) {
          post.liked = post.likes.some(like => like.user_id === this.USER_ID);
        } else {
          post.liked = false; // Initialize 'liked' property as false if 'likes' array is not defined or empty
        }
      });
    },
    getImageUrl(photoPath) {
      return `http://localhost:8080/uploads/${photoPath}`;
    },
    getUserProfilePic(profilePicPath) {
      return `http://localhost:8080/uploads/${profilePicPath}`;
    },
    formatDate(dateString) {
      const options = { day: '2-digit', month: 'long', year: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
    },
    toggleLike(post) {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Authentication token is missing');
        return;
      }

      const postId = post.id;

      // Ensure post.likes is initialized as an array
      post.likes = post.likes || [];

      // Check if the current user has already liked the post
      const likeIndex = post.likes.findIndex(like => like.user_id === this.USER_ID);

      if (likeIndex !== -1) {
        // Unlike the post
        axios.post(`http://localhost:8080/api/v1/posts/${postId}/likes`, { user_id: this.USER_ID }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
          .then(response => {
            console.log('Post unliked successfully');
            post.liked = false;
            post.likes.splice(likeIndex, 1);
            // Fetch updated post data
            this.fetchPostById(postId);
          })
          .catch(error => {
            console.error('Error unliking post:', error);
          });
      } else {
        // Like the post
        axios.post(`http://localhost:8080/api/v1/posts/${postId}/likes`, { user_id: this.USER_ID }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
          .then(response => {
            console.log('Post liked successfully');
            post.liked = true;
            post.likes.push({ user_id: this.USER_ID });
            // Fetch updated post data
            this.fetchPostById(postId);
          })
          .catch(error => {
            console.error('Error liking post:', error);
          });
      }
    },
    fetchPostById(postId) {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Authentication token is missing');
        return;
      }

      axios.get(`http://localhost:8080/api/v1/posts/${postId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          const updatedPost = response.data.post;
          // Update the posts array with the updated post data
          const index = this.posts.findIndex(post => post.id === updatedPost.id);
          if (index !== -1) {
            // If using Vue 3 with Composition API
            this.posts[index] = { ...this.posts[index], ...updatedPost };
          }
        })
        .catch(error => {
          console.error('Error fetching updated post:', error);
        });
    }
  }
}
</script>

<style>
.posts-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
  background-color: #fafafa;
}

.post-card {
  width: 500px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  margin-bottom: 60px;
  border-radius: 3px;
}

.post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid #efefef;
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-profile-pic {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  color: #262626;
}

.post-image-container {
  width: 100%;
  height: 0;
  padding-bottom: 100%;
  position: relative;
}

.post-img {
  position: absolute;
  object-fit: scale-down; 
  width: 100%;
  height: 100%;
}

.post-content {
  padding: 16px;
}

.post-caption {
  margin-bottom: 5px;
  color: #262626;
}

.post-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #8e8e8e;
  font-size: 14px;
}

.post-likes {
  font-weight: bold;
  color: #262626;
}

.post-date {
  color: #8e8e8e;
}

.like-icon {
  cursor: pointer;
}

.liked {
  color: red;
}
</style>
