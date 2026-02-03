# Supabase Setup (Huge upgrade over local JSON)

from supabase import create_client
from core.config import config

# Connection Initialization
supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def upload_todb(local_path, storage_name):
    """
    Sends your generated PDF to the 'certificates' folder in the cloud.
    It returns a link so students can actually view their achievement.
    """
    try:
        with open(local_path, "rb") as f:
            supabase.storage.from_(config.SUPABASE_BUCKET).upload(
                path=storage_name,
                file=f,
                file_options={"content-type": "application/pdf"}
            )    
        return supabase.storage.from_(config.SUPABASE_BUCKET).get_public_url(storage_name)
    
    except Exception as e:
        print("Upload failed. . . check if the bucket name is correct:", e)
        return None

def save_todb(name, email, course, tx_hash, url):
    """
    Saves a digital 'receipt' of the certificate.
    """
    data = {
        "student_name": name,
        "student_email": email,
        "course_name": course,
        "tx_hash": tx_hash,
        "pdf_url": url
    }
    try:
        return supabase.table("certificates").insert(data).execute()
    except Exception as e:
        print("Database save failed:", e)
        return None

def fetch_cert(email):
    """
    Fetches every single certificate linked to a specific student.
    """
    try:
        return supabase.table("certificates").select("*").eq("student_email", email).execute()
    except Exception as e:
        print("Fetch failed:", e)
        return None

def verify_cert(email, hash_val):
    """
    Checks if a specific transaction hash is valid for a student.
    This is the core of the Employer Portal.
    """
    try:
        return supabase.table("certificates").select("*").eq("student_email", email).eq("tx_hash", hash_val).execute()
    except Exception as e:
        print("Verification lookup failed:", e)
        return None