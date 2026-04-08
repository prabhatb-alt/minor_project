# Public student lookup and employer verification

import asyncio
from flask import Blueprint, request, jsonify
from services.database import fetch_cert, supabase
from aptos_sdk.async_client import RestClient
from core.config import config

# Blueprint for public routes without admin access
public_bp = Blueprint('public', __name__)

async def check_aptos_ledger(tx_hash):
    """Queries the Aptos blockchain directly to verify the transaction"""
    client = RestClient(config.APTOS_NODE_URL)
    try:
        tx_data = await client.transaction_by_hash(tx_hash)
        # Check if the transaction actually succeeded on-chain
        return tx_data.get("success", False)
    except Exception:
        # If the hash doesn't exist, it throws an error
        return False
    finally:
        await client.close()

@public_bp.route('/api/student/certificates', methods=['GET'])
def get_student_certs():
    email = request.args.get("email")
    if not email:
        return jsonify({"ok": False, "error": "Email is required"}), 400

    result = fetch_cert(email)
    if not result or not result.data:
        return jsonify({"ok": False, "error": "No certificates found"}), 404
    
    async def verify_all(certs):
        tasks = [check_aptos_ledger(cert['tx_hash']) for cert in certs]
        return await asyncio.gather(*tasks)

    validation_results = asyncio.run(verify_all(result.data))
    
    verified_certs = []
    for cert, is_on_chain in zip(result.data, validation_results):
        if is_on_chain:
            verified_certs.append(cert)
        else:
            print(f"Warning: Tampered or invalid record found in DB for {email}")
    if not verified_certs:
        return jsonify({"ok": False, "error": "Records found in DB, but failed blockchain verification."}), 404

    return jsonify({"ok": True, "certificates": verified_certs}), 200

@public_bp.route('/api/employer/verify', methods=['POST'])
def employer_verify():
    """
    Checks if a specific transaction hash exists, validates it on Aptos, 
    and checks email if provided.
    """
    data = request.json
    email = data.get("email", "").strip()
    tx_hash = data.get("tx_hash", "").strip()
    
    if not tx_hash:
        return jsonify({"ok": False, "error": "Transaction Hash is required"}), 400

    try:
        # 1. Search Supabase by the Hash (The Index)
        record = supabase.table('certificates').select('*').eq('tx_hash', tx_hash).execute()

        if not record.data:
            return jsonify({"ok": False, "error": "Record not found in the secure database"}), 404

        cert = record.data[0]

        # 2. Search Aptos (The Ultimate Source of Truth)
        # We run the async blockchain check inside our sync Flask route
        is_on_chain = asyncio.run(check_aptos_ledger(tx_hash))
        
        if not is_on_chain:
            return jsonify({"ok": False, "error": "Hash exists in DB but failed validation on the Aptos Blockchain."}), 401

        # 3. The Email Identity Logic
        if email:
            if cert['student_email'].lower() != email.lower():
                return jsonify({"ok": False, "error": "Email mismatch"}), 401
            cert['email_fully_verified'] = True
        else:
            cert['email_fully_verified'] = False

        return jsonify({"ok": True, "certificate": cert}), 200

    except Exception as e:
        print("Verification error:", e)
        return jsonify({"ok": False, "error": "Internal server error during verification"}), 500
    
@public_bp.route('/api/system-pulse', methods=['GET'])
def system_pulse():
    """
    Invisible keep-alive route. 
    Wakes up Render, and forces a microscopic Supabase query to reset the 7-day inactivity timer.
    """
    try:
        # We ask Supabase for a single, tiny piece of data just to keep the connection warm.
        # Replace 'certificates' with whatever your actual table name is!
        supabase.table('certificates').select('id').limit(1).execute()
        
        print("System Pulse: Render and Supabase are awake.")
        return jsonify({"status": "Systems Nominal", "database": "Online"}), 200
        
    except Exception as e:
        print("System Pulse Error:", e)
        return jsonify({"status": "Database Error", "details": str(e)}), 500