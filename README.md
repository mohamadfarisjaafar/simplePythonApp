# simplePythonApp
Simple Python API with Simple Front End

This application is a RESTful API built with Python and Flask. It supports user registration, authentication, creating posts, adding comments to posts, and retrieving posts with their associated comments. The API is designed to demonstrate basic CRUD functionality with user authentication via JSON Web Tokens (JWT).

Features

User Management:
Register a new user.
Authenticate a user and issue a JWT token.
Post Management:
Create a new post with an image and caption.
Retrieve all posts with their associated comments.
Comment Management:
Add a comment to a specific post.

Technology Stack

Backend: Python, Flask, Flask-RESTful
Database: SQLite
Authentication: Flask-JWT-Extended (JWT tokens)
Cross-Origin Resource Sharing (CORS): Flask-CORS

Setup Instructions

Prerequisites
Python 3.7 or higher installed on your system.
A terminal or command prompt for running commands.

Steps to Run API
1. Clone the repo to local
2. Set Up a Virtual Environment

Create and activate a Python virtual environment:

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

3. Install Dependencies
Install the required Python packages:

pip install flask flask-restful flask-jwt-extended flask-sqlalchemy

Start the Flask development server:
python app.py

The server will run on http://127.0.0.1:5000 by default.


Steps to Run Website
1. Navigate to frontend folder in terminal/cmd
2. Run web server using python
    Python3 -m http.server
3.  Open localhost:8000 in browser


Working app with video link : https://drive.google.com/drive/folders/18P4ns7oQ6HxL3SvYHq7Igg2SnN-xjncK?usp=sharing


