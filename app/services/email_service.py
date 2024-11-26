from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
import smtplib  # For error handling

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        if not settings.smtp_server or not settings.smtp_port or not settings.smtp_username or not settings.smtp_password:
            print("SMTP settings not configured. Email service will not work.")
            self.smtp_client = None
        else:
            self.smtp_client = SMTPClient(
                server=settings.smtp_server,
                port=settings.smtp_port,
                username=settings.smtp_username,
                password=settings.smtp_password
            )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        if not self.smtp_client:
            print("SMTP client not initialized. Email cannot be sent.")
            return

        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type provided.")

        try:
            # Render the email template
            html_content = self.template_manager.render_template(email_type, **user_data)
            # Send the email
            self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])
            print(f"Email of type '{email_type}' sent successfully to {user_data['email']}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email of type '{email_type}' to {user_data['email']}: {e}")

    async def send_verification_email(self, user: User):
        if not self.smtp_client:
            print("SMTP client not initialized. Verification email cannot be sent.")
            return
        verification_url = f"{settings.server_base_url}/verify-email/{user.id}/{user.verification_token}"
        await self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')
