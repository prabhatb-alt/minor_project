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

# ==========================================
# 4. FRONTEND HTML ROUTES (The updated schema)
# ==========================================

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/admin/dashboard')
def serve_dashboard():
    # Now correctly points to adm_dash.html
    return send_from_directory(app.static_folder, 'adm_dash.html')

@app.route('/student')
def serve_student():
    return send_from_directory(app.static_folder, 'student.html')

@app.route('/student/dashboard')
def serve_student_dashboard():
    # New route for the student dashboard
    return send_from_directory(app.static_folder, 'stud_dash.html')

@app.route('/verification')
def serve_verification():
    # Replaced the old /employer route with your new verification route
    return send_from_directory(app.static_folder, 'verification.html')

@app.route('/about')
def about_page():
    """Serves the project and team information page."""
    return send_from_directory(app.static_folder, 'about.html')

# ==========================================

# 5. Server
if __name__ == "__main__":
    if not config.setup_check():
        print("ERROR: .env is missing (values). Kindly check")
    else:
        print("Flask Backend Started")
        port = int(os.environ.get("PORT", 5000))
        is_dev = os.environ.get("FLASK_ENV") == "development"
        
        app.run(host="0.0.0.0", port=port, debug=is_dev)