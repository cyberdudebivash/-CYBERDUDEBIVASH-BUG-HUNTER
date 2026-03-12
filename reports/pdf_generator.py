"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Reporting Engine
Path: reports/pdf_generator.py
"""

from fpdf import FPDF
from datetime import datetime
import os

class BugHunterReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.set_text_color(220, 20, 60) # CyberDudeBivash Branding
        self.cell(0, 10, "CYBERDUDEBIVASH BUG HUNTER - AUDIT REPORT", 0, 1, "C")
        self.ln(10)

    def add_finding(self, finding):
        self.set_font("Arial", "B", 11)
        self.set_text_color(255, 0, 0)
        self.cell(0, 10, f"FINDING: {finding.get('type')}", 0, 1)
        self.set_text_color(0)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 7, f"Evidence: {finding.get('url') or finding.get('bucket')}")
        self.ln(5)

class ReportOrchestrator:
    def __init__(self, output_dir="outputs/reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir): os.makedirs(output_dir)

    def generate(self, domain, findings):
        pdf = BugHunterReport()
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Executive Summary for {domain}", 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 7, f"Identification of {len(findings)} high-risk assets requiring immediate remediation.")
        pdf.ln(10)

        for f in findings: pdf.add_finding(f)
        
        filename = f"CDB_Report_{domain}_{datetime.now().strftime('%Y%m%d')}.pdf"
        path = os.path.join(self.output_dir, filename)
        pdf.output(path)
        return path