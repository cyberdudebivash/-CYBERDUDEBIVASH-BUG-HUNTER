"""
CYBERDUDEBIVASH - ROI & Financial Impact Calculator
Path: analytics/roi_calculator.py
Purpose: Automates financial risk quantification for Executive Audits.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ROICalculator:
    def __init__(self):
        # Industry standard values for breach impact (2025-2026 estimates)
        self.avg_record_cost = 165  # Cost per leaked PII record
        self.bola_impact_constant = 250000  # Base cost for unauthorized API access
        self.cloud_leak_base = 500000  # Base cost for sensitive infra exposure

    def calculate_risk_exposure(self, findings: List[Dict]) -> Dict:
        """
        Calculates Annualized Loss Exposure (ALE) and Potential Savings.
        Formula: ALE = Single Loss Expectancy (SLE) * Annual Rate of Occurrence (ARO)
        """
        total_sle = 0
        mitigation_value = 0

        for f in findings:
            f_type = f.get("type", "").upper()
            
            # SLE calculation based on finding type
            if "BOLA" in f_type:
                sle = self.bola_impact_constant
            elif "CLOUD" in f_type or "S3" in f_type:
                sle = self.cloud_leak_base
            else:
                sle = 50000  # Default for low-tier findings
            
            # Severity Multiplier
            if f.get("severity") == "CRITICAL":
                sle *= 2.5
            
            total_sle += sle
            
        # ROI Logic: Assume CyberDudeBivash mitigates 95% of identified paths
        mitigation_value = total_sle * 0.95

        return {
            "potential_loss_exposure": total_sle,
            "prevented_loss_value": mitigation_value,
            "roi_percentage": (mitigation_value / 50000) * 100 # Against avg subscription cost
        }

    def get_formatted_metrics(self, findings: List[Dict]) -> str:
        """Returns a string summary for PDF report injection."""
        data = self.calculate_risk_exposure(findings)
        return (
            f"Financial Intelligence:\n"
            f"- Estimated Potential Loss Exposure: ${data['potential_loss_exposure']:,.2f}\n"
            f"- Prevented Loss (CDB Mitigation): ${data['prevented_loss_value']:,.2f}\n"
            f"- Projected ROSI: {data['roi_percentage']:.1f}%"
        )