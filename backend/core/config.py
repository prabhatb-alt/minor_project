# Centralized environment variable management

import os
from dotenv import load_dotenv

load_dotenv()

class ProjectConfig:
    def __init__(self):
        # Flask
        self.SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "samplesecretvalueifitdoesnotexist")
        
        # Supabase
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.SUPABASE_BUCKET = "certificates"

        # Aptos Blockchain
        self.APTOS_NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.devnet.aptoslabs.com/v1")
        self.UNIVERSITY_PRIVATE_KEY = os.getenv("UNIVERSITY_PRIVATE_KEY")
        self.COLLECTION_NAME = "Credlytic - Hack"

        # SMTP
        self.EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    def setup_check(self):
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            return False
        if not self.UNIVERSITY_PRIVATE_KEY:
            return False
        if not self.EMAIL_ADDRESS or not self.EMAIL_PASSWORD:
            return False
        return True

# One single config instance to be used across the project
config = ProjectConfig()