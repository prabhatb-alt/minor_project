# HTTPS Proxy Mailer: Bypassing Cloud SMTP Blocks via Google Apps Script

import urllib.request
import json
import base64

def send_email(student_email, student_name, course_name, explorer_url, pdf_path):
    try:
        # 1. Extract the hash from the URL
        tx_hash = "Unknown"
        if "/txn/" in explorer_url:
            tx_hash = explorer_url.split("/txn/")[1].split("?")[0]

        # 2. Read and encode the PDF for the HTTPS tunnel
        with open(pdf_path, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

        # 3. Build the HTML content
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
                <p><a href="{explorer_url}" style="background: #00e676; color: black; font-weight: bold; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Blockchain Record</a></p>
                <p>Please find your cryptographically secured digital certificate attached below.</p>
                <br><p>Regards,<br><strong>Credlytic Network</strong></p>
            </body>
        </html>
        """

        # 4. Prepare the payload
        payload = {
            "to": student_email,
            "subject": f"Success! Your Certificate for {course_name}",
            "htmlBody": html_content,
            "pdfB64": pdf_b64,
            "filename": f"{student_name}_Certificate.pdf"
        }

        # 5. THE PROXY TUNNEL
        GAS_URL = "https://script.google.com/macros/s/AKfycbx-nk9l-A_Kk9zKMQCBLCQP1X_916caumCQufeg56pdMSww18s7guK9s1DE4dnfFQ/exec" 
        
        # We add a 'User-Agent' to make the server request look like a real browser
        # This is the secret fix for the '403 Forbidden' error
        req = urllib.request.Request(
            GAS_URL, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        
        # 6. Fire the request
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            if result.get("ok"):
                print(f"Email successfully smuggled to {student_email} via HTTPS Proxy!")
                return True
            else:
                print("Google Proxy returned an internal error:", result)
                return False

    except Exception as e:
        print("Failed to route email via HTTPS tunnel:", e)
        return False