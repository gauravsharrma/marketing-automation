import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings

def send_otp_email(to_email: str, otp: str) -> bool:
    """Send OTP via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = "Your OTP for Marketing Automation Platform"

        body = f"""
        <html>
            <body>
                <h2>Your One-Time Password</h2>
                <p>Hello!</p>
                <p>Your OTP for the Marketing Automation Platform is: <strong>{otp}</strong></p>
                <p>This OTP will expire in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
                <p>If you didn't request this OTP, please ignore this email.</p>
                <br>
                <p>Best regards,</p>
                <p>Marketing Automation Team</p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False 