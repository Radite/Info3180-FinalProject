from flask import jsonify, request
from app import app, db
from ..models import Post, Likes
import os
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    if photo and allowed_file(photo.filename):
        try:
            # Save the photo to the user's posts folder
            os.makedirs(user_posts_folder, exist_ok=True)
            filename = secure_filename(photo.filename)
            photo_path = os.path.join('posts', str(user_id), filename)  # Relative path from the uploads folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_path))
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

# Route for retrieving all posts for all users
@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    all_posts = Post.query.all()
    posts_data = []

    for post in all_posts:
        # Count likes for each post
        likes_count = Likes.query.filter_by(post_id=post.id).count()

        # Construct data for each post including likes count
        post_data = {
            'id': post.id,
            'caption': post.caption,
            'photo': post.photo,
            'user_id': post.user_id,
            'created_on': post.created_on,
            'likes_count': likes_count  # Include the likes count
        }

        posts_data.append(post_data)

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

# Route to fetch updated post data by ID
@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'caption': post.caption,
        'likes_count': len(post.likes)
    }
    return jsonify({'post': post_data}), 200

# Route for retrieving likes on a specific post
@app.route('/api/v1/posts/<int:post_id>/likes', methods=['GET'])
def get_likes_for_post(post_id):
    likes = Likes.query.filter_by(post_id=post_id).all()
    likes_data = [{'id': like.id, 'post_id': like.post_id, 'user_id': like.user_id} for like in likes]
    return jsonify({'likes': likes_data})

@app.route('/api/v1/likes', methods=['GET'])
def get_all_likes():
    likes = Likes.query.all()
    likes_data = [{'id': like.id, 'post_id': like.post_id, 'user_id': like.user_id} for like in likes]
    return jsonify({'likes': likes_data})
# Route for deleting a post
@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        # Query the database to find the post by its ID
        post = Post.query.get_or_404(post_id)

        # Delete associated likes for the post
        likes = Likes.query.filter_by(post_id=post.id).all()
        for like in likes:
            db.session.delete(like)

        # Commit the changes to the database
        db.session.commit()

        # Delete the post image file from the file system
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.photo))

        # Finally, delete the post from the database
        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        # If an error occurs during deletion, return an error response
        return jsonify({'error': str(e)}), 500