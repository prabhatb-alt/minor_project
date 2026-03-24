# Mialing using Bypassing Render SMTP error using Google Scripts

import urllib.request
import json
import base64

def send_email(student_email, student_name, course_name, explorer_url, pdf_path):
    try:
        tx_hash = "Unknown"
        if "/txn/" in explorer_url:
            tx_hash = explorer_url.split("/txn/")[1].split("?")[0]

        with open(pdf_path, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

        html_content = f"""
        <html>
            <body style="font-family: sans-serif; color: #333;">
                <h2 style="color: #00e676;">Congratulations, {student_name}!</h2>
                <p>Your official certificate for <strong>{course_name}</strong> is now live on the Aptos Blockchain.</p>
                
                <div style="background-color: #f8f9fa; border-left: 4px solid #00e676; padding: 15px; margin: 20px 0;">
                    <p style="margin-top: 0; font-size: 12px; color: #666; text-transform: uppercase;">Blockchain Transaction ID</p>
                    <p style="font-family: monospace; font-size: 14px; word-break: break-all; margin-bottom: 0;">
                        <strong>{tx_hash}</strong>
                    </p>
                </div>
                
                <p>
                    <a href="{explorer_url}" style="background: #00e676; color: black; font-weight: bold; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Blockchain Record
                    </a>
                </p>
                <p>Please find your cryptographically secured digital certificate attached to this email.</p>
                <br>
                <p>Regards,<br><strong>Credlytic Network</strong></p>
            </body>
        </html>
        """

        payload = {
            "to": student_email,
            "subject": f"Success! Your Certificate for {course_name}",
            "htmlBody": html_content,
            "pdfB64": pdf_b64,
            "filename": f"{student_name}_Certificate.pdf"
        }

        GAS_URL = "https://script.google.com/macros/s/AKfycbx-nk9l-A_Kk9zKMQCBLCQP1X_916caumCQufeg56pdMSww18s7guK9s1DE4dnfFQ/exec" 
        
        req = urllib.request.Request(
            GAS_URL, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            if result.get("ok"):
                print(f"Email successfully smuggled to {student_email} via HTTPS Proxy!")
                return True
            else:
                print("Google Proxy Error:", result)
                return False

    except Exception as e:
        print("Failed to route email via HTTPS:", e)
        return False