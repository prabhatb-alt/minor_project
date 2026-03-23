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
    Fixed version with explicit 4-item bounding box for QR code pasting.
    """
    try:
        # 1. CREATE THE QR CODE
        verify_link = f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=devnet"
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(verify_link)
        qr.make(fit=True)
        # We convert to RGB immediately to ensure compatibility
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # 2. OPEN THE TEMPLATE
        img = Image.open(TEMPLATE_PATH).convert("RGB")
        draw = ImageDraw.Draw(img)

        # 3. FONT SETUP
        try:
            name_font = ImageFont.truetype(FONT_PATH, 60)
            sub_font = ImageFont.truetype(FONT_PATH, 25)
        except:
            name_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

        # 4. DRAW THE TEXT
        draw.text((726, 526), student_name, fill="white", font=name_font)
        draw.text((840, 674), course_name, fill="white", font=sub_font)
        hash_display = f"Blockchain ID: {tx_hash[:20]}..." 
        draw.text((699, 765), hash_display, fill="gray", font=sub_font)

        # 5. QR CODE - Using the explicit 4-item box (x1, y1, x2, y2)
        x, y = 100, 700
        width, height = qr_img.size
        img.paste(qr_img, (x, y, x + width, y + height)) 

        # 6. PDF OUTPUT
        img.save(output_pdf_path, "PDF", resolution=100.0)
        return True

    except Exception as e:
        print("Certificate creation failed:", e)
        return False