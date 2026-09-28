import pytest
from src.analytics.cross_deal import CrossDealAnalytics
from src.analytics.relationship import MultiSessionRelationshipIntelligence
from src.analytics.competitive import RealTimeCompetitiveIntelligence
from src.analytics.win_loss import PredictiveWinLossReasoning

def test_cross_deal_analytics():
    cda = CrossDealAnalytics()
    interactions = [
        {"interaction_id": "i1", "content": "Legacy ERP integration is very slow."},
        {"interaction_id": "i2", "content": "Need GDPR and EU data residency compliance."},
        {"interaction_id": "i3", "content": "Seat-based pricing is too expensive for 500 users."}
    ]
    pain_points = cda.mine_recurring_pain_points(interactions)
    assert pain_points["total_interactions_analyzed"] == 3
    assert len(pain_points["pain_point_frequencies"]) >= 3

    lost_deals = [{"opportunity_id": "opp_10", "arr": 75000.0, "loss_reason": "Lacked SAML SSO"}]
    gaps = cda.generate_product_gap_feedback(lost_deals)
    assert gaps[0]["identified_feature_gap"] == "Enterprise SSO / SAML 2.0"

def test_relationship_intelligence():
    msr = MultiSessionRelationshipIntelligence()
    stakeholders = [
        {"name": "Bob", "role": "Champion", "sentiment": "Positive"},
        {"name": "Carol", "role": "Economic Buyer", "sentiment": "Positive"}
    ]
    mapping = msr.map_stakeholder_influence(stakeholders)
    assert mapping["has_champion"] is True
    assert mapping["has_economic_buyer_coverage"] is True

    health = msr.compute_account_health_score([], stakeholders, days_since_last_contact=3)
    assert health["health_status"] == "Healthy"
    assert health["health_score"] >= 75.0

def test_competitive_intelligence():
    rtc = RealTimeCompetitiveIntelligence()
    text = "We are currently comparing your solution with Salesforce and Gong."
    mentions = rtc.extract_competitor_mentions(text)
    assert "salesforce" in mentions
    assert "gong" in mentions

    card = rtc.get_battlecard("salesforce")
    assert "Salesforce Sales Cloud" in card["competitor_name"]

def test_win_loss_reasoning():
    pwl = PredictiveWinLossReasoning()
    res = pwl.compute_deal_win_probability(
        deal_stage="Proposal",
        arr=100000.0,
        stakeholders=[{"role": "Champion", "sentiment": "Positive"}],
        days_in_stage=10,
        has_budget_approval=True
    )
    assert res["win_probability"] > 0.0
    assert len(res["prescriptive_next_best_actions"]) > 0
