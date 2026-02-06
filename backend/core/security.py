# Google OAuth verification & signature validation

from google.oauth2 import id_token
from google.auth.transport import requests
from core.config import config

def verify_google_token(token):
    """
    Checks if the Google login token is real using your Project Client ID.
    """
    try:
        # We use the ID from our centralized config
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            config.GOOGLE_CLIENT_ID
        )

        user_email = idinfo.get("email")
        return user_email

    except Exception as e:
        print("Google Token Verification Failed:", e)
        return None

def is_admin_authorized(email):
    """
    Checks if the logged-in email is in the white-list we set in .env.
    """
    # We check if the email exists in the list we created in config.py
    if email in config.ADMIN_WHITELIST:
        return True
    
    print(f"Unauthorized login attempt blocked for: {email}")
    return False