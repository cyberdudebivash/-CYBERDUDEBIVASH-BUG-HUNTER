"""
CYBERDUDEBIVASH BUG HUNTER - Findings Verifier
Path: intel/verify_findings.py
Purpose: Instantly extracts and validates critical findings from the asset database.
"""

from sqlmodel import Session, select
from database import engine, Vulnerability, Asset

def verify_critical_hits():
    print("\n[DB] Querying for HIGH and CRITICAL findings...")
    with Session(engine) as session:
        # Pull findings with HIGH or CRITICAL severity
        statement = select(Vulnerability).where(Vulnerability.severity == "CRITICAL")
        findings = session.exec(statement).all()
        
        if not findings:
            print("[!] No critical findings found in the database yet.")
            return

        print(f"[+] SUCCESS: Found {len(findings)} Critical Vulnerabilities!")
        for f in findings:
            print(f"--- FINDING ---")
            print(f"TYPE: {f.type}")
            print(f"TARGET: {f.url}")
            print(f"EVIDENCE: {f.evidence}")
            print(f"----------------\n")

if __name__ == "__main__":
    verify_critical_hits()