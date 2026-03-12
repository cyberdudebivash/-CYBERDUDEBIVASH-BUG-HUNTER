"""
CYBERDUDEBIVASH BUG HUNTER - Asset Delta Analyzer
Path: intel/asset_delta_analyzer.py
Purpose: Tracks attack surface drift and identifies newly exposed assets.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Set
from sqlmodel import Session, select, create_engine
from database import Asset, Scan # Assumes these are defined in your database.py

# Elite Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CDB-BH-DELTA] - %(message)s')
logger = logging.getLogger(__name__)

class AssetDeltaAnalyzer:
    def __init__(self, db_url: str = "sqlite:///assets.db"):
        self.engine = create_engine(db_url)

    def get_scan_history(self, domain: str, limit: int = 2) -> List[Scan]:
        """Retrieves the last two scan objects for a specific domain."""
        with Session(self.engine) as session:
            statement = select(Scan).where(Scan.domain == domain).order_by(Scan.timestamp.desc()).limit(limit)
            return session.exec(statement).all()

    def get_assets_for_scan(self, scan_id: str) -> Dict[str, Asset]:
        """Maps hostnames to Asset objects for a specific scan ID."""
        with Session(self.engine) as session:
            statement = select(Asset).where(Asset.scan_id == scan_id)
            assets = session.exec(statement).all()
            return {asset.hostname: asset for asset in assets}

    def analyze_drift(self, domain: str) -> Dict:
        """
        Logic: Compares the latest scan against the previous baseline.
        Returns: Added, Removed, and Modified assets.
        """
        history = self.get_scan_history(domain)
        
        if len(history) < 2:
            logger.info(f"Insufficient history for {domain} delta analysis.")
            return {"status": "baseline_established", "added": [], "removed": [], "modified": []}

        current_scan = history[0]
        previous_scan = history[1]

        current_map = self.get_assets_for_scan(current_scan.id)
        previous_map = self.get_assets_for_scan(previous_scan.id)

        current_hosts = set(current_map.keys())
        previous_hosts = set(previous_map.keys())

        # 1. Added Assets (The most critical for Bug Hunters)
        added_hosts = current_hosts - previous_hosts
        added_details = [current_map[h] for h in added_hosts]

        # 2. Removed Assets
        removed_hosts = previous_hosts - current_hosts
        removed_details = [previous_map[h] for h in removed_hosts]

        # 3. Modified Assets (Tech Stack Changes)
        modified_details = []
        common_hosts = current_hosts & previous_hosts
        for h in common_hosts:
            if current_map[h].technologies != previous_map[h].technologies:
                modified_details.append({
                    "hostname": h,
                    "old_tech": previous_map[h].technologies,
                    "new_tech": current_map[h].technologies
                })

        logger.info(f"Delta Analysis for {domain}: +{len(added_details)} | -{len(removed_details)} | Δ{len(modified_details)}")
        
        return {
            "domain": domain,
            "timestamp": datetime.utcnow().isoformat(),
            "added": added_details,
            "removed": removed_details,
            "modified": modified_details
        }

    def generate_delta_alert(self, delta_report: Dict):
        """Logic for triggering a real-time notification if new assets are found."""
        if delta_report["added"]:
            # This would typically publish to the Redis 'recon_alerts' channel
            logger.warning(f"CRITICAL: {len(delta_report['added'])} NEW ASSETS detected for {delta_report['domain']}!")

if __name__ == "__main__":
    # Internal Performance Test
    analyzer = AssetDeltaAnalyzer()
    report = analyzer.analyze_drift("example.com")
    print(json.dumps(report, indent=2, default=str))