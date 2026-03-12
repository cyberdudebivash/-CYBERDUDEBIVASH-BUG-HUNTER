"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Reporting Engine
Path: reports/pdf_generator.py
Version: 3.0.0 (Production Hardened)
Purpose: Generates high-authority, risk-scored PDF security reports.
"""

from fpdf import FPDF
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    """
    CyberDudeBivash Proprietary Risk Scoring Algorithm.
    Calculates impact based on vulnerability type and asset criticality.
    """
    @staticmethod
    def calculate_score(findings: list) -> int:
        if not findings:
            return 0
        
        total_score = 0
        for f in findings:
            # Weighted scoring based on vulnerability impact
            f_type = f.get("type", "").upper()
            if "BOLA" in f_type:
                total_score += 40
            elif "CLOUD_LEAK" in f_type or "S3" in f_type:
                total_score += 35
            elif "TAKEOVER" in f_type:
                total_score += 30
            
            # Severity multiplier
            if f.get("severity") == "CRITICAL":
                total_score += 10
                
        # Cap the score at 100 for enterprise normalization
        return min(total_score, 100)

class BugHunterReport(FPDF):
    def header(self):
        # Professional Branded Header
        self.set_font("Arial", "B", 15)
        self.set_text_color(220, 20, 60) # CyberDudeBivash Crimson
        self.cell(0, 10, "CYBERDUDEBIVASH BUG HUNTER - SECURITY AUDIT REPORT", 0, 1, "C")
        self.set_font("Arial", "I", 10)
        self.set_text_color(100)
        self.cell(0, 10, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential - CyberDudeBivash Pvt. Ltd.", 0, 0, "C")

    def add_risk_gauge(self, score: int):
        """Visual representation of the CyberDudeBivash Risk Score."""
        self.set_font("Arial", "B", 12)
        self.set_text_color(0)
        self.cell(0, 10, f"CyberDudeBivash Risk Score: {score}/100", 0, 1)
        
        # Color-coded risk indicator (Red for High, Orange for Medium)
        color = (220, 20, 60) if score >= 70 else (255, 140, 0)
        self.set_fill_color(*color)
        
        # Draw the score bar (normalized to 180mm max width)
        self.rect(10, self.get_y(), (score * 1.8), 5, 'F')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0)
        self.cell(0, 10, f" {title}", 0, 1, "L", 1)
        self.ln(4)

    def add_finding(self, finding):
        self.set_font("Arial", "B", 11)
        self.set_text_color(220, 20, 60)
        self.cell(0, 10, f"FINDING: {finding.get('type', 'Security Vulnerability')}", 0, 1)
        
        self.set_text_color(0)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 7, f"Target: {finding.get('domain', 'N/A')}")
        self.multi_cell(0, 7, f"Evidence: {finding.get('url') or finding.get('bucket', 'N/A')}")
        self.multi_cell(0, 7, f"Impact: {finding.get('impact', 'High-risk unauthorized access detected.')}")
        self.ln(5)

class ReportOrchestrator:
    def __init__(self, output_dir="outputs/reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, scan_data: dict) -> str:
        domain = scan_data.get("domain", "unknown")
        findings = scan_data.get("critical_findings", [])
        
        # 1. Calculate Risk Score via the Intelligence Engine
        risk_score = RiskEngine.calculate_score(findings)
        
        pdf = BugHunterReport()
        pdf.add_page()

        # 2. Executive Summary & Risk Gauge
        pdf.chapter_title("1. EXECUTIVE RISK ASSESSMENT")
        pdf.add_risk_gauge(risk_score)
        
        summary = (
            f"Automated audit results for {domain} identified {len(findings)} critical "
            f"vulnerabilities. The calculated CyberDudeBivash Risk Score is {risk_score}/100."
        )
        pdf.multi_cell(0, 7, summary)
        pdf.ln(5)

        # 3. Technical Findings
        pdf.chapter_title("2. TECHNICAL VULNERABILITY DETAILS")
        if not findings:
            pdf.cell(0, 10, "No critical vulnerabilities were identified during this cycle.", 0, 1)
        else:
            for finding in findings:
                pdf.add_finding(finding)

        # 4. Strategic Remediation
        pdf.chapter_title("3. REMEDIATION STRATEGY")
        remediation = (
            "1. Enforce strict BOLA validation on all API endpoints handling user-specific data.\n"
            "2. Audit all cloud storage buckets to ensure private access policies are active.\n"
            "3. Enable real-time certificate transparency monitoring for asset discovery."
        )
        pdf.multi_cell(0, 7, remediation)

        # Finalize and Save
        filename = f"CDB_Audit_{domain}_{datetime.now().strftime('%Y%m%d')}.pdf"
        file_path = os.path.join(self.output_dir, filename)
        pdf.output(file_path)
        
        logger.info(f"Enterprise Report Generated: {file_path}")
        return file_path