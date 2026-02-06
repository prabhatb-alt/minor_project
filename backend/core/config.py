# Centralized environment variable management

import os
from dotenv import load_dotenv

load_dotenv()

class ProjectConfig:
    def __init__(self):
        # Flask Settings
        self.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "samplesecretvalueifitdoesnotexist")
        
        # Supabase Settings (Our cloud database)
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.SUPABASE_BUCKET = "certificates"

        # Aptos Blockchain Settings
        self.APTOS_NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.devnet.aptoslabs.com/v1")
        self.UNIVERSITY_PRIVATE_KEY = os.getenv("UNIVERSITY_PRIVATE_KEY")
        self.COLLECTION_NAME = "Credlytic - Hack"

        # SMTP Settings (For sending those emails)
        self.EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

        # Admin & Security Settings (The new stuff!)
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        
        # We take the string from .env and turn it into a list ['email1', 'email2']
        # This makes it way easier for Python to check if someone is allowed in.
        raw_admins = os.getenv("ADMIN_WHITELIST", "")
        self.ADMIN_WHITELIST = raw_admins.split(",")

    def setup_check(self):
        """A quick sanity check to make sure you didn't miss anything in your .env"""
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            return False
        if not self.UNIVERSITY_PRIVATE_KEY:
            return False
        if not self.EMAIL_ADDRESS or not self.EMAIL_PASSWORD:
            return False
        if not self.GOOGLE_CLIENT_ID:
            return False
        return True

# One single config instance to be used across the project
config = ProjectConfig()