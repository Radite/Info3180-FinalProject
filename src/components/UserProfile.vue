<template>
  <div>
    <!-- Profile information -->
    <div v-if="user" class="profile-info">
      <!-- Profile picture -->
      <div class="profile-picture">
        <img :src="getUserProfilePic(user.profile_photo)" alt="Profile Picture">
      </div>
      <!-- User details -->
      <div class="user-details">
        <div class="username">{{ user.firstname }} {{ user.lastname }}</div>
        <div class="user-meta">
          <div>{{ user.location }}</div>
          <div class="joined-on">Member since {{ formatJoinedDate(user.joined_on) }}</div>
        </div>
        <div class="biography">{{ user.biography }}</div>
      </div>

      <!-- User stats -->
      <div class="user-stats">
        <div>
          <div>{{ posts.length }}</div>
          <div>Posts</div>
        </div>
        <div>
          <div>{{ user.followers_count }}</div>
          <div>Followers</div>
        </div>
        <div>
          <div>{{ user.following_count }}</div>
          <div>Following</div>
        </div>
      </div>

      <!-- Follow button -->
      <button v-if="!isCurrentUser" @click="toggleFollow" class="follow-button">{{ followButtonText }}</button>
    </div>
    <div v-else>Loading...</div>

    <!-- Posts -->
    <h2>Posts</h2>
    <div v-if="posts" class="post-grid">
      <div v-for="post in posts" :key="post.id" class="post-item">
        <div class="post-image-container">
          <!-- Display video if the post is a video -->
          <video v-if="isVideo(post.photo)" :src="getImageUrl(post.photo)" controls class="post-image"></video>
          <!-- Display image if the post is not a video -->
          <img v-else :src="getImageUrl(post.photo)" alt="Post Image" class="post-image">
        </div>
      </div>
    </div>
    <div v-else>No posts found.</div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

export default {
  data() {
    return {
      user: null,
      posts: [],
      followerCount: 0,
      followingCount: 0,
      isFollowing: false,
      isCurrentUser: false,
      USER_ID: null, // Initialize USER_ID
      followButtonText: '' // Initialize followButtonText
    };
  },
  mounted() {
  // Get the token from localStorage and decode it to extract the user ID
  const token = localStorage.getItem('token');
  if (token) {
    const decodedToken = jwtDecode(token);
    this.USER_ID = decodedToken.user_id; // Set USER_ID to the user_id from the decoded token
  }

  const userId = this.$route.params.userId;
  this.fetchUserData(userId);
  this.fetchUserPosts(userId);
  this.checkIfFollowing(userId).then(() => {
    this.setFollowButtonText(); // Update followButtonText after checking follow status
  });
  this.checkIfCurrentUser(userId);
},
  methods: {
    async toggleFollow() {
  try {
    const userId = this.$route.params.userId;
    const response = await axios.post(`http://localhost:8080/api/v1/users/${userId}/follow`, {
      follower_id: this.USER_ID // Use USER_ID instead of loggedInUserId
    });
    if (response.data.message === 'User followed successfully') {
      this.isFollowing = true;
      this.user.followers_count++; // Increment followers count
    } else if (response.data.message === 'User unfollowed successfully') {
      this.isFollowing = false;
      this.user.followers_count--; // Decrement followers count
    }
    this.setFollowButtonText(); // Update followButtonText after toggle
  } catch (error) {
    console.error('Error toggling follow status:', error);
  }
},

    async fetchUserData(userId) {
      try {
        const response = await axios.get(`http://localhost:8080/api/v1/users/${userId}`);
        this.user = response.data.user;
        this.isCurrentUser = response.data.user.id === this.loggedInUserId;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async fetchUserPosts(userId) {
      try {
        const response = await axios.get(`http://localhost:8080/api/v1/users/${userId}/posts`);
        this.posts = response.data.posts;
      } catch (error) {
        console.error('Error fetching user posts:', error);
      }
    },
    async checkIfFollowing(userId) {
        try {
            const response = await axios.get(`http://localhost:8080/api/v1/users/${userId}/follow_status/${this.USER_ID}`);
            this.isFollowing = response.data.is_following;
            this.setFollowButtonText(); // Update followButtonText after checking follow status
        } catch (error) {
            console.error('Error checking follow status:', error);
        }
    },
    checkIfCurrentUser(userId) {
      this.isCurrentUser = userId === this.loggedInUserId;
    },
    setFollowButtonText() {
      // Set followButtonText based on isFollowing
      this.followButtonText = this.isFollowing ? 'Unfollow' : 'Follow';
    },
    getImageUrl(photoPath) {
      return `http://localhost:8080/uploads/${photoPath}`;
    },
    getUserProfilePic(profilePicPath) {
      return `http://localhost:8080/uploads/${profilePicPath}`;
    },
    // Check if the post is a video
    isVideo(photoPath) {
      return photoPath.toLowerCase().endsWith('.mp4') || photoPath.toLowerCase().endsWith('.mov') || photoPath.toLowerCase().endsWith('.avi');
    },
    formatJoinedDate(joinedDate) {
      const date = new Date(joinedDate);
      const options = { month: 'long', year: 'numeric' };
      return date.toLocaleDateString('en-US', options);
    }
  }
};
</script>

<style scoped>
.post-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Display 3 items in a row */
  grid-gap: 10px;
  justify-items: center;
  padding: 0 20px; /* Adjust as needed */
}

.post-item {
  width: 100%; /* Ensure each item takes the full width */
}

.post-image-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  overflow: hidden;
}

.post-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  display: flex;
  align-items: center;
  justify-content: center; /* Center items vertically */
  border: 2px solid black; /* Add black border */
  padding: 20px; /* Add padding for better spacing */
  max-width: 90%;
  margin: 0 auto; /* Center horizontally */  
}
.profile-picture {
  margin-right: 20px;
}

.profile-picture img {
  width: 200px;
  height: 200px;
}


.user-info {
  display: flex;
}

.user-details {
  flex-grow: 1;
}

.user-stats {
  display: flex;
  align-items: center;
  margin-bottom: 100px;

}

.user-stats > div {
  margin-right: 20px;
}

.user-stats > div:last-child {
  margin-right: 0;
}

.user-stats > div > div {
  font-weight: bold;
  text-align: center;
}

.user-stats > div > div:first-child {
  font-size: 1.2em;
}

.user-stats > div > div:last-child {
  font-size: 0.8em;
}




.username {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 20px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-meta {
  margin-bottom: 10px;
}

.joined-on {
  font-size: 0.8em;
}

.biography {
  margin-top: 10px;
}

.user-stats {
  display: flex;
  margin-top: 10px;
}

.user-stats > div {
  margin-right: 20px;
}

.user-stats > div:last-child {
  margin-right: 0;
}

.user-stats > div > div {
  font-weight: bold;
  text-align: center;
}

.user-stats > div > div:first-child {
  font-size: 1.2em;
}

.user-stats > div > div:last-child {
  font-size: 0.8em;
}

.follow-button {
  margin-top: 10px;
  align-self: flex-end;
  background-color: #4a90e2; /* Set background color */
  color: white; /* Set text color */
  border: none; /* Remove border */
  padding: 10px 20px; /* Add padding */
  cursor: pointer; /* Add pointer cursor */
  width: 200px; /* Set width of button */
  border-radius: 5px; /* Add border radius */
}
</style>
