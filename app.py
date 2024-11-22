from flask import Flask, request, jsonify  # Import necessary modules for Flask
from flask_sqlalchemy import SQLAlchemy  # For database interaction
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity  # For JWT authentication
from flask_cors import CORS  # To handle cross-origin resource sharing
from datetime import timedelta  # For setting token expiration time
from werkzeug.security import generate_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Configure the database and JWT settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Secret key for JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Token expiration time

CORS(app)  # Enable CORS for all routes

# Initialize database and JWT manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(80), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(120), nullable=False)  # User password
    name = db.Column(db.String(80), nullable=False)  # User name

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key referencing the user
    caption = db.Column(db.String(255), nullable=False)  # Caption for the post
    image = db.Column(db.String(255), nullable=False)  # URL of the image

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the comment
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key referencing the user
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key referencing the post
    text = db.Column(db.String(255), nullable=False)  # Text of the comment

# Create database tables
with app.app_context():
    db.create_all()  # Create all tables if they don't exist

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists!"}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create new user
    new_user = User(email=email, password=password, name=name)
    db.session.add(new_user)
    db.session.commit()

    # Generate access token (for authentication)
    access_token = create_access_token(identity=email)

    return jsonify({
        "msg": "User registered successfully",
        "access_token": access_token
    }), 201  # 201 Created status

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Parse the JSON payload
    # Validate required fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"msg": "Missing fields"}), 400
    
    # Check if the user exists and credentials are correct
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401
    
    # Create a JWT token with the user ID as identity
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token, "user_id": user.id}), 200  # Respond with token and user ID

# Route to create a post
@app.route('/posts', methods=['POST'])
@jwt_required()  # Require authentication
def create_post():
    data = request.get_json()  # Parse the JSON payload
    user_id = get_jwt_identity()  # Get the user ID from the token

    # Validate required fields
    if not data or 'caption' not in data or 'image' not in data:
        return jsonify({"msg": "Caption and image are required"}), 400
    
    # Validate field types
    if not isinstance(data['caption'], str) or not isinstance(data['image'], str):
        return jsonify({"msg": "Caption and image must be strings"}), 400
    
    # Create a new post and save to the database
    new_post = Post(user_id=int(user_id), caption=data['caption'], image=data['image'])
    db.session.add(new_post)
    db.session.commit()
    
    # Respond with the created post
    return jsonify({"msg": "Post created successfully", "post": {
        "id": new_post.id,
        "user_id": new_post.user_id,
        "caption": new_post.caption,
        "image": new_post.image
    }}), 201

# Route to add a comment to a post
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()  # Require authentication
def add_comment(post_id):
    data = request.get_json()  # Parse the JSON payload
    user_id = get_jwt_identity()  # Get the user ID from the token

    # Validate required fields
    if not data or 'text' not in data:
        return jsonify({"msg": "Text is required"}), 400
    
    # Validate field type
    if not isinstance(data['text'], str):
        return jsonify({"msg": "Text must be a string"}), 400
    
    # Check if the post exists
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    # Create a new comment and save to the database
    new_comment = Comment(user_id=user_id, post_id=post_id, text=data['text'])
    db.session.add(new_comment)
    db.session.commit()
    
    # Respond with the created comment
    return jsonify({"msg": "Comment added successfully", "comment": {
        "id": new_comment.id,
        "post_id": new_comment.post_id,
        "user_id": new_comment.user_id,
        "text": new_comment.text
    }}), 201

# Route to retrieve all posts with comments
@app.route('/posts', methods=['GET'])
@jwt_required()  # Require authentication
def get_posts():
    posts = Post.query.all()  # Retrieve all posts
    response = []
    # Format each post with its comments
    for post in posts:
        comments = Comment.query.filter_by(post_id=post.id).all()
        response.append({
            "id": post.id,
            "user_id": post.user_id,
            "caption": post.caption,
            "image": post.image,
            "comments": [
                {"id": comment.id, "user_id": comment.user_id, "text": comment.text}
                for comment in comments
            ]
        })
    return jsonify(response), 200  # Respond with the list of posts

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
