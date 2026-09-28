import pytest
from src.memory.hindsight_client import HindsightClient
from src.memory.schema import Stakeholder, Opportunity, InteractionPayload

def test_hindsight_retain_and_recall():
    client = HindsightClient()

    # Ingest facts
    client.retain(
        namespace="account_101",
        key="stk_001",
        data={
            "interaction_id": "int_001",
            "content": "Requested SOC2 compliance report and SAML SSO integration setup."
        }
    )

    # Recall facts
    results = client.recall(namespace="account_101", query="SOC2 SSO compliance")
    assert len(results) == 1
    assert "SOC2" in results[0]["content"]

def test_hindsight_fact_extraction():
    client = HindsightClient()
    facts = client.extract_facts(
        text="Client budget is $100k, evaluating Salesforce vs our solution, requires SSO.",
        source_interaction_id="int_002"
    )
    categories = [f.category for f in facts]
    assert "budget" in categories
    assert "technical" in categories
    assert "competitor" in categories

def test_hindsight_reflect():
    client = HindsightClient()
    client.retain(
        memory_bank_id="bank_test_202",
        key="int_01",
        data={
            "interaction_id": "int_01",
            "content": "Customer mentioned $150k budget ceiling and compared pricing with Salesforce."
        }
    )
    reflection = client.reflect(memory_bank_id="bank_test_202", topic="deal_strategy")
    assert reflection["status"] == "success"
    assert reflection["total_memories_consolidated"] == 1
    assert "budget" in reflection["key_fact_dimensions"]
    assert "competitor" in reflection["key_fact_dimensions"]
    assert len(reflection["consolidated_beliefs"]) > 0

