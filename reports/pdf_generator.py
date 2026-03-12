"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Reporting Engine
Path: reports/pdf_generator.py
Purpose: Generates high-authority, branded PDF security reports.
"""

from fpdf import FPDF
from datetime import datetime
import json
import os

class BugHunterReport(FPDF):
    def header(self):
        # Branded Header
        self.set_font("Arial", "B", 15)
        self.set_text_color(255, 0, 0) # CyberDudeBivash Red
        self.cell(0, 10, "CYBERDUDEBIVASH BUG HUNTER - SECURITY AUDIT", 0, 1, "C")
        self.set_font("Arial", "I", 10)
        self.set_text_color(100)
        self.cell(0, 10, f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential - CyberDudeBivash Pvt. Ltd.", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, f" {title}", 0, 1, "L", 1)
        self.ln(4)

    def add_finding(self, finding):
        self.set_font("Arial", "B", 11)
        # Severity-based coloring
        severity = finding.get("severity", "CRITICAL")
        if severity == "CRITICAL":
            self.set_text_color(255, 0, 0)
        else:
            self.set_text_color(255, 140, 0)
            
        self.cell(0, 10, f"FINDING: {finding.get('type', 'Vulnerability')}", 0, 1)
        self.set_text_color(0)
        self.set_font("Arial", "", 10)
        
        # Details
        self.multi_cell(0, 7, f"Target: {finding.get('domain')}")
        self.multi_cell(0, 7, f"Evidence: {finding.get('url') or finding.get('bucket')}")
        self.multi_cell(0, 7, f"Impact: {finding.get('impact', 'High-risk unauthorized access.')}")
        self.ln(5)

class ReportOrchestrator:
    def __init__(self, output_dir="outputs/reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, scan_data: dict):
        """
        Processes pipeline data and outputs a professional PDF.
        """
        domain = scan_data.get("domain", "unknown")
        findings = scan_data.get("critical_findings", [])
        
        pdf = BugHunterReport()
        pdf.add_page()

        # 1. Executive Summary
        pdf.chapter_title("1. EXECUTIVE SUMMARY")
        pdf.set_font("Arial", "", 10)
        summary_text = (
            f"This security audit was performed by the CyberDudeBivash Bug Hunter platform for the domain {domain}. "
            f"The scan identified {len(findings)} critical vulnerabilities requiring immediate remediation."
        )
        pdf.multi_cell(0, 7, summary_text)
        pdf.ln(10)

        # 2. Technical Findings
        pdf.chapter_title("2. TECHNICAL FINDINGS")
        if not findings:
            pdf.cell(0, 10, "No critical vulnerabilities were identified during this scan.", 0, 1)
        else:
            for finding in findings:
                pdf.add_finding(finding)

        # 3. Remediation & Hardening
        pdf.ln(10)
        pdf.chapter_title("3. STRATEGIC REMEDIATION")
        pdf.set_font("Arial", "", 10)
        remediation = (
            "1. Implement strict Broken Object Level Authorization (BOLA) checks at the API gateway.\n"
            "2. Ensure all S3/Azure buckets are set to private and follow the Principle of Least Privilege.\n"
            "3. Monitor Certificate Transparency logs for unauthorized subdomain creation."
        )
        pdf.multi_cell(0, 7, remediation)

        # Save File
        report_name = f"CDB_Report_{domain}_{datetime.now().strftime('%Y%m%d')}.pdf"
        file_path = os.path.join(self.output_dir, report_name)
        pdf.output(file_path)
        print(f"[Reporting] Enterprise PDF generated: {file_path}")
        return file_path

if __name__ == "__main__":
    # Unit Test Logic
    sample_data = {
        "domain": "target-corp.com",
        "critical_findings": [
            {"type": "BOLA", "url": "https://api.target-corp.com/v1/user/1005", "severity": "CRITICAL"},
            {"type": "CLOUD_LEAK", "bucket": "target-corp-backup-2026", "severity": "CRITICAL"}
        ]
    }
    generator = ReportOrchestrator()
    generator.generate(sample_data)