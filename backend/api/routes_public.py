# Public student lookup and employer verification

from flask import Blueprint, request, jsonify
from services.database import fetch_cert, verify_cert

# Blueprint for public routes without admin access
public_bp = Blueprint('public', __name__)

@public_bp.route('/api/student/certificates', methods=['GET'])
def get_student_certs():
    """
    Fetches all certificates linked to a student's email(student.html)
    """
    email = request.args.get("email")
    if not email:
        return jsonify({"ok": False, "error": "Email is required"}), 400

    # Find records on supabase database
    result = fetch_cert(email)
    
    if result:
        # result.data contains the list of certificate rows
        return jsonify({"ok": True, "certificates": result.data})
    return jsonify({"ok": False, "error": "No certificates found"}), 404

@public_bp.route('/api/employer/verify', methods=['POST'])
def employer_verify():
    """
    Checks if a specific student email and transaction hash match our records(employer.html)
    """
    data = request.json
    email = data.get("email")
    tx_hash = data.get("tx_hash")
    if not email or not tx_hash:
        return jsonify({"ok": False, "error": "Email and Tx Hash are required"}), 400

    # Database verifies the record and tx_hash
    result = verify_cert(email, tx_hash)
    
    # If the database returns even one row the certificate is authentic
    if result and len(result.data) > 0:
        return jsonify({"ok": True, "certificate": result.data[0]})
    return jsonify({"ok": False, "error": "Verification failed: No matching record"}), 404