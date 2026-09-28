from typing import List, Dict, Any
from collections import Counter

class CrossDealAnalytics:
    """
    Analyzes unstructured notes and deals across account executives and industry verticals
    to mine recurring pain points and feed product feature gap loops.
    """
    def __init__(self, hindsight_client=None):
        self.hindsight_client = hindsight_client

    def mine_recurring_pain_points(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Clusters unstructured interaction notes to quantify statistical frequencies of customer challenges.
        """
        pain_point_categories = {
            "Legacy ERP / CRM Integration": ["integration", "legacy", "erp", "crm", "api"],
            "Data Residency & Security Compliance": ["gdpr", "eu", "data residency", "security", "soc2", "compliance"],
            "Seat-Based Pricing Reluctance": ["pricing", "seat-based", "expensive", "budget", "cost", "discount"],
            "Custom Workflow Automation Needs": ["workflow", "automation", "customization", "logic"]
        }

        category_counts = Counter()
        detailed_findings = []

        for interaction in interactions:
            content = interaction.get("content", "").lower()
            matched = False
            for category, keywords in pain_point_categories.items():
                if any(kw in content for kw in keywords):
                    category_counts[category] += 1
                    matched = True
            if matched:
                detailed_findings.append({
                    "interaction_id": interaction.get("interaction_id"),
                    "account_id": interaction.get("account_id"),
                    "summary": interaction.get("content")[:100] + "..."
                })

        return {
            "total_interactions_analyzed": len(interactions),
            "pain_point_frequencies": dict(category_counts),
            "top_recurring_pain_point": category_counts.most_common(1)[0][0] if category_counts else "None",
            "findings_sample": detailed_findings[:5]
        }

    def generate_product_gap_feedback(self, lost_deals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Automatically tags and scores product feature gaps directly correlated with lost opportunities.
        """
        feature_gaps = []
        for deal in lost_deals:
            reason = deal.get("loss_reason", "").lower()
            arr = deal.get("arr", 0.0)

            gap_type = "Unspecified"
            if "sso" in reason or "saml" in reason:
                gap_type = "Enterprise SSO / SAML 2.0"
            elif "hipaa" in reason or "soc2" in reason:
                gap_type = "Healthcare / HIPAA Compliance"
            elif "on-prem" in reason or "air-gapped" in reason:
                gap_type = "On-Premises / Air-Gapped Deployment"
            elif "custom report" in reason or "analytics" in reason:
                gap_type = "Advanced Custom Reporting Engine"

            feature_gaps.append({
                "deal_id": deal.get("opportunity_id"),
                "account_id": deal.get("account_id"),
                "revenue_lost": arr,
                "identified_feature_gap": gap_type,
                "loss_reason": deal.get("loss_reason")
            })

        return feature_gaps
