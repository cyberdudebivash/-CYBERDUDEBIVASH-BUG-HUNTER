"""
CYBERDUDEBIVASH BUG HUNTER - Bug Bounty Export Engine
Path: intel/export_findings_csv.py
Purpose: Exports critical findings to a CSV format optimized for HackerOne/Bugcrowd.
"""

import csv
import os
from datetime import datetime
from sqlmodel import Session, select
from database import engine, Vulnerability # Assumes production database.py

def export_to_bug_bounty_csv(output_dir="outputs/exports"):
    """
    Logic: Queries the DB for Critical hits and writes them to a standardized CSV.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CDB_Export_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    # Standard headers for Bugcrowd/HackerOne imports
    headers = ["Title", "Type", "Severity", "Target_URL", "Evidence", "Impact", "Date_Found"]

    print(f"\n[Export] Generating Bug Bounty Export: {filename}")

    try:
        with Session(engine) as session:
            # Select findings flagged as CRITICAL by the BOLA or Cloud engines
            statement = select(Vulnerability).where(Vulnerability.severity == "CRITICAL")
            findings = session.exec(statement).all()

            if not findings:
                print("[!] No critical findings available for export.")
                return None

            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for f in findings:
                    writer.writerow([
                        f"Critical {f.type} Discovered",
                        f.type,
                        f.severity,
                        f.url,
                        f.evidence or "See technical report",
                        "Unauthorized access to sensitive internal data/logic.",
                        datetime.utcnow().strftime("%Y-%m-%d")
                    ])

        print(f"[+] SUCCESS: Exported {len(findings)} findings to {filepath}")
        return filepath

    except Exception as e:
        print(f"[ERROR] Export failed: {e}")
        return None

if __name__ == "__main__":
    export_to_bug_bounty_csv()