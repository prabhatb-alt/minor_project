# Application entry point and CORS configuration

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import config and blueprints for routes
from core.config import config
from api.routes_admin import admin_bp
from api.routes_public import public_bp


# 1. Initialize Flask and define frontend files location
app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.config['SECRET_KEY'] = config.SECRET_KEY

# 2. Setup CORS: Enables cross origin reqs from frontend to backend
CORS(app)

# 3. Register Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)

# 4. Define frontend routes
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/admin/dashboard')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/student')
def serve_student():
    return send_from_directory(app.static_folder, 'student.html')

@app.route('/employer')
def serve_employer():
    return send_from_directory(app.static_folder, 'employer.html')

# 5. Server
if __name__ == "__main__":
    if not config.setup_check():
        print("ERROR: .env is missing (values). Kindly check")
    else:
        print("Backend is starting on http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)