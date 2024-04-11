from flask import jsonify, request
from app import app, db
from ..models import User, Follow
import os

# Route for setting or unsetting a follow relationship between users
@app.route('/api/v1/users/<int:user_id>/follow', methods=['POST'])
def toggle_follow_user(user_id):
    data = request.json
    follower_id = data['follower_id']

    # Check if follower is already following the user
    existing_follow = Follow.query.filter_by(user_id=user_id, follower_id=follower_id).first()

    if existing_follow:
        # Unfollow the user
        db.session.delete(existing_follow)
        db.session.commit()
        return jsonify({'message': 'User unfollowed successfully'})
    else:
        # Follow the user
        new_follow = Follow(
            user_id=user_id,
            follower_id=follower_id
        )
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': 'User followed successfully'})


# Route for retrieving all users
@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    # Query all users from the database
    all_users = User.query.all()
    
    # Construct JSON response with user data
    users_data = []
    for user in all_users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'location': user.location,
            'biography': user.biography,
            'profile_photo': user.profile_photo,
            'joined_on': user.joined_on
        }
        users_data.append(user_data)
    
    # Return JSON response with all users
    return jsonify({'users': users_data})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        followers_count = get_followers_count(user_id)
        following_count = get_following_count(user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'location': user.location,
            'biography': user.biography,
            'profile_photo': user.profile_photo,
            'joined_on': user.joined_on,
            'followers_count': followers_count,
            'following_count': following_count
        }
        return jsonify({'user': user_data})
    else:
        return jsonify({'error': 'User not found'}), 404
