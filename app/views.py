"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
from datetime import datetime
from .models import User, Post, Likes, Follow
from . import db
import os
from flask import session
from werkzeug.utils import secure_filename
import jwt 
from functools import wraps

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token.split(' ')[1], app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            print("Decoded token data:", data)  # Add this line for debugging
        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.form  # assuming form data is sent

    # Check if the POST request contains the file part
    print("Form Data:", data)  # Print form data for debugging
    if 'profile_photo' not in request.files:
        print("No file part")
        return jsonify({'error': 'No file part'})

    profile_photo = request.files['profile_photo']
    print("Profile Photo:", profile_photo)  # Print profile photo for debugging

    # If the user does not select a file, the browser may also submit an empty file without a filename
    if profile_photo.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'})

    if profile_photo and allowed_file(profile_photo.filename):
        try:
            # Save the profile photo to the uploads folder
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profilephotos'), exist_ok=True)
            filename = secure_filename(profile_photo.filename)
            profile_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profilephotos', filename)
            profile_photo.save(profile_photo_path)
            print("Profile Photo Path:", profile_photo_path)  # Print profile photo path for debugging

            # Save user data to the database and reference the profile photo path
            print("Saving user data to the database...")

            new_user = User(
                username=data['username'],
                password=data['password'],
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                location=data.get('location'),
                biography=data.get('biography'),
                profile_photo=profile_photo_path,  # Save the profile photo path to the database
                joined_on=datetime.utcnow()
            )
            print(new_user.__dict__)

            db.session.add(new_user)
            db.session.commit()

            print("User registered successfully")
            return jsonify({'message': 'User registered successfully'})
        except Exception as e:
            # Handle exceptions and return an error message
            print(f"Exception occurred: {e}")
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Invalid file type'})

# Import the redirect function
from flask import redirect

# Route for user login
@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        # Generate JWT token
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
        print("Token generated:", token)  # Add this line to print the generated token

        # Return token to the client
        return jsonify({'token': token, 'user_id': user.id})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Route for user logout
@app.route('/api/v1/auth/logout', methods=['POST'])
def logout_user():
    # Check if user is logged in
    if 'user_id' in session:
        # Clear session variable
        session.pop('user_id', None)
        return jsonify({'message': 'User logged out successfully'})
    else:
        return jsonify({'error': 'User is not logged in'})

# Route for adding posts to a user's feed
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
def add_post(user_id):
    data = request.form

    # Define the folder for user posts
    user_posts_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', str(user_id))

    # Check if the POST request contains the file part
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'})

    photo = request.files['photo']

    # If the user does not select a file, the browser may also submit an empty file without a filename
    if photo.filename == '':
        return jsonify({'error': 'No selected file'})

    if photo:
        try:
            # Save the photo to the user's posts folder
            os.makedirs(user_posts_folder, exist_ok=True)
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(user_posts_folder, filename)
            photo.save(photo_path)
        except Exception as e:
            return jsonify({'error': str(e)})

        # Save post data to the database
        new_post = Post(
            caption=data['caption'],
            photo=photo_path,
            user_id=user_id,
            created_on=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()

        return jsonify({'message': 'Post added successfully'})
    else:
        return jsonify({'error': 'Invalid file'})
# Route for retrieving a user's posts
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    user_posts = Post.query.filter_by(user_id=user_id).all()
    posts_data = [{'id': post.id, 'caption': post.caption, 'photo': post.photo, 'created_on': post.created_on} for post in user_posts]
    return jsonify({'posts': posts_data})

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

# Route for retrieving all posts for all users
@app.route('/api/v1/posts', methods=['GET'])
@token_required
def get_all_posts(current_user):
    all_posts = Post.query.all()
    posts_data = [{'id': post.id, 'caption': post.caption, 'photo': post.photo, 'user_id': post.user_id, 'created_on': post.created_on} for post in all_posts]
    return jsonify({'posts': posts_data})

# Route for setting or unsetting a like on a post
@app.route('/api/v1/posts/<int:post_id>/likes', methods=['POST'])
def toggle_like_post(post_id):
    data = request.json
    user_id = data['user_id']

    # Check if user has already liked the post
    existing_like = Likes.query.filter_by(post_id=post_id, user_id=user_id).first()

    if existing_like:
        # Unlike the post
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'message': 'Post unliked successfully'})
    else:
        # Like the post
        new_like = Likes(
            post_id=post_id,
            user_id=user_id
        )
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'message': 'Post liked successfully'})

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

@app.route('/api/v1/auth/check', methods=['GET'])
@token_required
def check_authentication(current_user):
    return jsonify({'message': 'User is authenticated'})