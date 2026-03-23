# SMTP logic: Building and sending HTML emails

import smtplib
import ssl
from email.message import EmailMessage
from core.config import config

def send_email(student_email, student_name, course_name, explorer_url, pdf_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Success! Your Certificate for {course_name}"
        msg["From"] = config.EMAIL_ADDRESS
        msg["To"] = student_email

        # Extrating the transaction hash directly from the explorer URL
        tx_hash = "Unknown"
        if "/txn/" in explorer_url:
            tx_hash = explorer_url.split("/txn/")[1].split("?")[0]

        # Text ver
        text_content = f"Hello {student_name},\n\nCongratulations! Your certificate for {course_name} has been issued on the blockchain.\n\nTransaction ID: {tx_hash}\nView on Explorer: {explorer_url}\n\nYour certificate is attached below."
        msg.set_content(text_content)

        # HTML ver
        html_content = f"""
        <html>
            <body style="font-family: sans-serif; color: #333;">
                <h2 style="color: #00E079;">Congratulations, {student_name}!</h2>
                <p>Your official certificate for <strong>{course_name}</strong> is now live on the Aptos Blockchain.</p>
                
                <div style="background-color: #f8f9fa; border-left: 4px solid #00E079; padding: 15px; margin: 20px 0;">
                    <p style="margin-top: 0; font-size: 12px; color: #666; text-transform: uppercase;">Blockchain Transaction ID (Save this)</p>
                    <p style="font-family: monospace; font-size: 14px; word-break: break-all; margin-bottom: 0;">
                        <strong>{tx_hash}</strong>
                    </p>
                </div>
                
                <p>
                    <a href="{explorer_url}" style="background: #00E079; color: black; font-weight: bold; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        View Blockchain Record
                    </a>
                </p>
                <p>Please find your digital certificate attached to this email.</p>
                <br>
                <p>Regards,<br><strong>Credlytic Network</strong></p>
            </body>
        </html>
        """
        msg.add_alternative(html_content, subtype="html")

        with open(pdf_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename=f"{student_name}_Certificate.pdf"
            )

        # Send via server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email successfully sent to {student_email}")
        return True

    except Exception as e:
        print("Failed to send email:", e)
        return False