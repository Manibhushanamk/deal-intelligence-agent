from typing import List, Dict, Any

class PredictiveWinLossReasoning:
    """
    Evaluates deal stage dwell time, buyer engagement level, executive sponsorship presence, and budget alignment
    to compute win probabilities and causal risk attributions.
    """
    def compute_deal_win_probability(
        self,
        deal_stage: str,
        arr: float,
        stakeholders: List[Dict[str, Any]],
        days_in_stage: int,
        has_budget_approval: bool
    ) -> Dict[str, Any]:
        """
        Calculates probabilistic win outcome and primary risk vectors.
        """
        # Base win probability by stage
        stage_base_probability = {
            "Qualification": 0.20,
            "Discovery": 0.35,
            "Proposal": 0.55,
            "Negotiation": 0.75,
            "Closed Won": 1.00,
            "Closed Lost": 0.00
        }
        base_prob = stage_base_probability.get(deal_stage, 0.40)
        risk_vectors = []
        positive_factors = []

        # Stagnation penalty
        if days_in_stage > 30:
            base_prob -= 0.15
            risk_vectors.append(f"Deal stalled in {deal_stage} for {days_in_stage} days (> 30 day threshold).")
        else:
            positive_factors.append(f"Healthy velocity: {days_in_stage} days in current stage.")

        # Budget verification
        if not has_budget_approval:
            base_prob -= 0.20
            risk_vectors.append("Budget approval not explicitly confirmed by Economic Buyer.")
        else:
            positive_factors.append("Explicit budget approval confirmed.")

        # Stakeholder coverage evaluation
        has_buyer = any(s.get("role") == "Economic Buyer" for s in stakeholders)
        has_champion = any(s.get("role") == "Champion" for s in stakeholders)
        has_blocker = any(s.get("role") == "Blocker" or s.get("sentiment") == "Negative" for s in stakeholders)

        if not has_buyer:
            base_prob -= 0.15
            risk_vectors.append("Absence of Economic Buyer participation in evaluation.")
        if not has_champion:
            base_prob -= 0.15
            risk_vectors.append("No designated internal Champion identified.")
        if has_blocker:
            base_prob -= 0.10
            risk_vectors.append("Negative sentiment blocker present among stakeholders.")

        final_prob = max(0.05, min(0.95, base_prob))

        # Prescriptive Next-Best-Action (NBA)
        next_best_actions = []
        if "Budget" in str(risk_vectors):
            next_best_actions.append("Schedule ROI & Business Case review with CFO / Economic Buyer.")
        if "Economic Buyer" in str(risk_vectors):
            next_best_actions.append("Request Executive Briefing call to engage Economic Buyer.")
        if "Champion" in str(risk_vectors):
            next_best_actions.append("Identify technical lead to nurture into internal Champion.")
        if not next_best_actions:
            next_best_actions.append("Draft customized proposal and schedule closing review meeting.")

        return {
            "win_probability": round(final_prob, 2),
            "deal_stage": deal_stage,
            "causal_risk_vectors": risk_vectors,
            "positive_factors": positive_factors,
            "prescriptive_next_best_actions": next_best_actions
        }
