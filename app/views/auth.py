from flask import jsonify, request
from app import app, db
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from functools import wraps
from flask import session
from werkzeug.security import generate_password_hash
from validate_email import validate_email
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .utils import allowed_file
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from validate_email import validate_email
import re  # Import regular expression module for email validation

@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.form

    # Check if the POST request contains the file part
    print("Form Data:", data)
    profile_photo = request.files.get('profile_photo')

    if profile_photo and allowed_file(profile_photo.filename):
        try:
            # Save the profile photo to the uploads folder
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profilephotos'), exist_ok=True)
            filename = secure_filename(profile_photo.filename)
            profile_photo_path = os.path.join('profilephotos', filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_photo_path))
            print("Profile Photo Path:", profile_photo_path)

        except Exception as e:
            # Handle exceptions and return an error message
            print(f"Exception occurred: {e}")
            return jsonify({'error': str(e)})
    else:
        print("No file uploaded, using default photo path")
        profile_photo_path = os.path.join('profilephotos', 'default.jpg')

    try:
        # Hash the password before saving it to the database
        password = data['password']
        if len(password) < 8:
            return jsonify({'error': 'Password should be at least 8 characters long'}), 400
        if password.isalpha() or password.isdigit():
            return jsonify({'error': 'Password should contain both letters and numbers'}), 400

        # Check email format using regular expression
        email = data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(data['password'])

        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        # Save user data to the database and reference the profile photo path
        print("Saving user data to the database...")
        new_user = User(
            username=data['username'],
            password=hashed_password,  # Use hashed password
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            location=data.get('location', ''),
            biography=data.get('biography', ''),
            profile_photo=profile_photo_path,
            joined_on=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()

        print("User registered successfully")
        return jsonify({'message': 'User registered successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        # Handle other exceptions and return an error message
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500

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


# Route for user login
@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter(User.username.ilike(username)).first()
    if user and check_password_hash(user.password, password):
        # Generate JWT token
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
        print("Token generated:", token) 

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


@app.route('/api/v1/auth/check', methods=['GET'])
@token_required
def check_authentication(current_user):
    return jsonify({'message': 'User is authenticated'})
