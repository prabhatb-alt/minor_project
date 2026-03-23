# Google OAuth verification & signature validation

from google.oauth2 import id_token
from google.auth.transport import requests
from core.config import config

def verify_google_token(token):
    """
    Checks if the Google login token is real using your Project Client ID.
    """
    try:
        # We added clock_skew_in_seconds=10 to fix the 'Token used too early' error
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            config.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10 
        )

        user_email = idinfo.get("email")
        return user_email

    except Exception as e:
        print("Google Token Verification Failed:", e)
        return None

def is_admin_authorized(email):
    """
    Checks if the logged-in email is in the whitelist we set in .env.
    """
    # 1. Ensure the email from Google is lowercase and clean
    clean_email = email.lower().strip()

    # 2. Convert the whitelist into a clean list (removing spaces and making lowercase)
    # This handles both strings and lists if you change config.py later
    whitelist = config.ADMIN_WHITELIST
    if isinstance(whitelist, str):
        whitelist = [e.strip().lower() for e in whitelist.split(',')]
    else:
        whitelist = [str(e).strip().lower() for e in whitelist]

    # 3. Final check
    if clean_email in whitelist:
        return True
    
    print(f"Unauthorized login attempt blocked for: {clean_email}")
    return False