# Minting Certificates as PDFs with QR codes

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from core.config import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "..", "..", "frontend", "assets", "fonts", "inter.ttf")
TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "..", "frontend", "assets", "images", "template.png")

def create_cert(student_name, course_name, tx_hash, output_pdf_path):
    """
    This function does three things:
    1. Generates a QR code for verification.
    2. Opens your certificate template.
    3. Draws the name, course, hash, and QR code onto the image.
    """
    try:
        # 1. CREATE THE QR CODE
        verify_link = f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet"
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(verify_link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # 2. OPEN THE TEMPLATE
        img = Image.open(TEMPLATE_PATH).convert("RGB")
        draw = ImageDraw.Draw(img)

        # 3. FONT SETP
        try:
            name_font = ImageFont.truetype(FONT_PATH, 60)
            sub_font = ImageFont.truetype(FONT_PATH, 25)
        except:
            name_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

        # 4. "DRAW" THE TEXT
        draw.text((726, 526), student_name, fill="white", font=name_font)
        draw.text((840, 674), course_name, fill="white", font=sub_font)
        hash_display = f"Blockchain ID: {tx_hash[:20]}..." 
        draw.text((699, 765), hash_display, fill="gray", font=sub_font)

        # 5. QR CODE
        img.paste(qr_img, (100, 700)) 

        # 6. PDF OUTPUT
        img.save(output_pdf_path, "PDF", resolution=100.0)
        return True

    except Exception as e:
        print("Certificate creation failed:", e)
        return False