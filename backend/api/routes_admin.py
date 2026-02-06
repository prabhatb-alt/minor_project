# Admin auth, wallet binding, and issuance logic

from flask import Blueprint, request, jsonify
from core.security import verify_google_token, is_admin_authorized
from services.blockchain import mint_onchain
from services.certificate import create_cert
from services.database import upload_todb, save_todb
from services.mailer import send_email
import os

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/api/admin/login_check', methods=['POST'])
def login_check():
    """
    Checks if the admin is allowed to enter the dashboard.
    """
    data = request.json
    token = data.get("credential") # google login button sends this
    
    # 1. Ask Google if this token is real
    email = verify_google_token(token)
    if not email:
        return jsonify({"ok": False, "error": "Invalid Google Token"}), 401
    
    # 2. Check if this email is on .env
    if not is_admin_authorized(email):
        return jsonify({"ok": False, "error": "Unauthorized Admin Email"}), 403
    
    # 3. All good then proceed to dash
    return jsonify({"ok": True, "email": email})

@admin_bp.route('/api/admin/issue', methods=['POST'])
def issue_cert():
    """
    Mint -> Create PDF -> Upload to Cloud -> Save to DB -> Email Student
    """
    data = request.json
    student_name = data.get("student_name")
    student_email = data.get("student_email")
    course_name = data.get("course_name")

    # --- 1. Mint on Chain ---
    tx_hash = mint_onchain(student_name, course_name, student_email)
    if not tx_hash:
        return jsonify({"ok": False, "error": "Blockchain Minting Failed"}), 500

    # --- 2. Create PDF ---
    temp_filename = f"cert_{tx_hash[:10]}.pdf"
    temp_path = os.path.join("temp", temp_filename)
    os.makedirs("temp", exist_ok=True)

    success = create_cert(student_name, course_name, tx_hash, temp_path)
    if not success:
        return jsonify({"ok": False, "error": "PDF Generation Failed"}), 500

    # --- 3. Upload to supabase ---
    cloud_url = upload_todb(temp_path, temp_filename)
    if not cloud_url:
        return jsonify({"ok": False, "error": "Cloud Storage Upload Failed"}), 500

    # --- 4. metadata Store on supabase ---
    save_todb(student_name, student_email, course_name, tx_hash, cloud_url)

    # --- 5. Send the mail ---
    explorer_url = f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet"
    send_email(student_email, student_name, course_name, explorer_url, temp_path)

    # --- cleaning the system ---
    # Delete the local temp file to keep your server clean
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return jsonify({"ok": True, "tx_hash": tx_hash, "url": cloud_url})