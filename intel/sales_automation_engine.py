"""
CYBERDUDEBIVASH - Sales Automation & Report Delivery
Path: intel/sales_automation_engine.py
Version: 1.0.0 (Production Outreach)
"""

import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import settings

class SalesAutomation:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 465  # For SSL
        self.sender_email = os.getenv("SALES_EMAIL")
        self.password = os.getenv("SALES_EMAIL_PASSWORD")

    def create_email(self, target_domain, report_path, risk_score):
        """Drafts a high-authority outreach email based on the CyberDudeBivash brand."""
        subject = f"CRITICAL SECURITY ADVISORY: Potential Exposure Detected for {target_domain}"
        
        # High-Impact Body Logic
        body = f"""
        Dear Security Team,

        Our autonomous intelligence swarm, operating under the CyberDudeBivash Sentinel APEX framework, has identified critical security vulnerabilities associated with your infrastructure.

        Audit Summary for {target_domain}:
        - CyberDudeBivash Risk Score: {risk_score}/100
        - Finding Type: BOLA / Cloud Storage Exposure
        - Remediation Status: Immediate Action Required

        Attached is a complimentary Executive Security Audit detailing the evidence and recommended strategic hardening steps.

        For a deep-dive into these findings or to integrate our Sentinel-SDK for real-time protection, please reply to this advisory.

        Best regards,
        
        CyberDudeBivash Automated Intelligence Swarm
        CyberDudeBivash Pvt. Ltd.
        Official Authority: Bivash Kumar, Founder & CEO
        """

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = f"security@{target_domain}"  # Target security alias
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Attach the Branded PDF Report
        with open(report_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(report_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
            message.attach(part)
            
        return message

    def send_advisory(self, target_domain, report_path, risk_score):
        """Executes the delivery through the secure SMTP gateway."""
        message = self.create_email(target_domain, report_path, risk_score)
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, message["To"], message.as_string())
            print(f"[SALES] Advisory successfully delivered to {target_domain}")
        except Exception as e:
            print(f"[SALES-ERROR] Delivery failed for {target_domain}: {e}")

# This can be integrated into the MassOnboarder to trigger immediately after report generation