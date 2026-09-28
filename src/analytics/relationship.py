from typing import List, Dict, Any
from datetime import datetime

class MultiSessionRelationshipIntelligence:
    """
    Monitors long-term trajectory, stakeholder influence mapping, and account health scoring over multi-month sales motions.
    """
    def __init__(self, hindsight_client=None):
        self.hindsight_client = hindsight_client

    def map_stakeholder_influence(self, stakeholders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Maps decision makers, internal champions, economic buyers, technical evaluators, and blockers.
        """
        champions = [s for s in stakeholders if s.get("role") == "Champion"]
        economic_buyers = [s for s in stakeholders if s.get("role") == "Economic Buyer"]
        technical_evaluators = [s for s in stakeholders if s.get("role") == "Technical Evaluator"]
        blockers = [s for s in stakeholders if s.get("role") == "Blocker" or s.get("sentiment") == "Negative"]

        return {
            "total_stakeholders": len(stakeholders),
            "champions": champions,
            "economic_buyers": economic_buyers,
            "technical_evaluators": technical_evaluators,
            "blockers": blockers,
            "has_economic_buyer_coverage": len(economic_buyers) > 0,
            "has_champion": len(champions) > 0
        }

    def compute_account_health_score(
        self,
        interactions: List[Dict[str, Any]],
        stakeholders: List[Dict[str, Any]],
        days_since_last_contact: int
    ) -> Dict[str, Any]:
        """
        Computes composite relationship health index (0 - 100) using sentiment, engagement velocity, and stakeholder roles.
        """
        score = 100.0

        # Latency penalty
        if days_since_last_contact > 14:
            score -= 30.0
        elif days_since_last_contact > 7:
            score -= 15.0

        # Stakeholder coverage evaluation
        mapped = self.map_stakeholder_influence(stakeholders)
        if not mapped["has_economic_buyer_coverage"]:
            score -= 20.0
        if not mapped["has_champion"]:
            score -= 25.0
        if len(mapped["blockers"]) > 0:
            score -= (15.0 * len(mapped["blockers"]))

        # Sentiment penalty/bonus
        positive_count = sum(1 for s in stakeholders if s.get("sentiment") == "Positive")
        negative_count = sum(1 for s in stakeholders if s.get("sentiment") == "Negative")
        score += (positive_count * 5.0) - (negative_count * 10.0)

        final_score = max(0.0, min(100.0, score))
        health_status = "Healthy" if final_score >= 75 else ("At Risk" if final_score >= 50 else "Critical")

        return {
            "health_score": final_score,
            "health_status": health_status,
            "days_since_last_contact": days_since_last_contact,
            "stakeholder_summary": {
                "champions_count": len(mapped["champions"]),
                "blockers_count": len(mapped["blockers"])
            }
        }
