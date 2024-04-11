<template>
  <div class="posts-container">
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
          <router-link v-if="post.userProfile" :to="`/users/${post.userProfile.id}`" class="user-profile">
            <img v-if="post.userProfile && post.userProfile.profile_photo" :src="getUserProfilePic(post.userProfile.profile_photo)" class="user-profile-pic" alt="User Profile Pic">
            <span class="username">{{ post.userProfile && post.userProfile.username }}</span>
          </router-link>
        </div>
        <div class="post-image-container">
          <!-- Display video if the post is a video -->
          <video v-if="isVideo(post.photo)" :src="getVideoUrl(post.photo)" controls class="post-video"></video>
          <!-- Display image if the post is not a video -->
          <img v-else :src="getImageUrl(post.photo)" class="post-img" alt="Post">
        </div>
        <div class="post-content">
          <p class="post-caption">{{ post.caption }}</p>
          <div class="post-details">
            <p class="post-likes">{{ post.likes_count }} 
              <i :class="['like-icon', post.liked ? 'fas fa-heart liked' : 'far fa-heart']" @click="toggleLike(post)"></i> likes</p>
            <p class="post-date">{{ formatDate(post.created_on) }}</p>
          </div>
        </div>
      </div>
    </div>
    <router-link to="/posts/new" class="new-post-button">New Post</router-link>
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
      USER_ID: null, // Initialize USER_ID
      users: [] // Array to store users data
    };
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
      // Check if the post is a video
  isVideo(photoPath) {
    return photoPath.toLowerCase().endsWith('.mp4') || photoPath.toLowerCase().endsWith('.mov') || photoPath.toLowerCase().endsWith('.avi');
  },
  // Get the URL of the video
  getVideoUrl(photoPath) {
    return `http://localhost:8080/uploads/${photoPath}`;
  },

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
    .then(async response => {
      this.posts = response.data.posts;
      this.error = '';

      // Fetch all likes
      const likesResponse = await axios.get(`http://localhost:8080/api/v1/likes`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const likes = likesResponse.data.likes;

      // Distribute likes to posts
      this.posts.forEach(post => {
        post.likes = likes.filter(like => like.post_id === post.id);
        post.liked = post.likes.some(like => like.user_id === this.USER_ID);
      });

      // Fetch users data
      this.fetchUsers();
    })
    .catch(error => {
      console.error('Error fetching posts:', error);
      this.error = 'Failed to fetch posts. Please try again later.';
    });
},
fetchLikesForPost(post) {
  return new Promise((resolve, reject) => {
    const token = localStorage.getItem('token');
    if (!token) {
      reject('Authentication token is missing');
      return;
    }

    // Fetch likes for the post
    axios.get(`http://localhost:8080/api/v1/posts/${post.id}/likes`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        // Check if the logged-in user has liked the post
        const userLiked = response.data.likes.some(like => like.user_id === this.USER_ID);
        post.liked = userLiked;
        resolve();
      })
      .catch(error => {
        console.error(`Error fetching likes for post ${post.id}:`, error);
        reject(`Failed to fetch likes for post ${post.id}. Please try again later.`);
      });
  });
},

    fetchUsers() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Authentication token is missing');
        this.error = 'Authentication token is missing';
        return;
      }

      // Fetch users
      axios.get('http://localhost:8080/api/v1/users', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          this.users = response.data.users;
          this.error = '';

          // Assign user profiles to posts
          this.assignUserProfilesToPosts();
        })
        .catch(error => {
          console.error('Error fetching users:', error);
          this.error = 'Failed to fetch users. Please try again later.';
        });
    },
    assignUserProfilesToPosts() {
      // Loop through each post and find matching user data to assign to post's userProfile property
      this.posts.forEach(post => {
        const user = this.users.find(user => user.id === post.user_id);
        if (user) {
          post.userProfile = {
            id: user.id,
            profile_photo: user.profile_photo,
            username: user.username
          };
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
  },
}
</script>

<style scoped>
.posts-container {
  display: flex;
  flex-direction: column; /* Stack posts vertically */
  align-items: center; /* Center horizontally */
  padding: 20px;
  position: relative; 
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
  text-decoration: none; /* Remove underline */
}

.user-profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  color: #262626;
}

.post-image-container {
  width: 100%;
  height: 300px;
  position: relative;
}

.post-img, .post-video {
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
.new-post-button {
  background-color: #4a90e2; /* Light blue color */
  border: none;
  color: #ffffff;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  position: absolute; 
  top: 20px;
  right: 20px;
}

</style>