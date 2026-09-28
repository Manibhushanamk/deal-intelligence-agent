#!/usr/bin/env python3
"""
Deal Intelligence Agent - End-to-End Enterprise Demo Script
-----------------------------------------------------------
Demonstrates continuous persistent memory (Hindsight SDK), cross-deal analytics,
predictive win-loss reasoning, Google Workspace MCP tools, and PDF dossier generation.
"""

import sys
import os
import json
from src.agent.state import AgentState
from src.agent.core import DealIntelligenceAgent
from src.narrative.report_generator import ReportGenerator

def main():
    print("=" * 80)
    print("      DEAL INTELLIGENCE AGENT (DIA) - ENTERPRISE DEMO RUNNER")
    print("=" * 80)

    # 1. Initialize Realistic Enterprise Deal State
    state = AgentState(
        account_id="acc_acme_corp_8821",
        opportunity_id="opp_cloud_migration_9912",
        account_name="Acme Corporation",
        current_stage="Proposal",
        arr=185000.00,
        stakeholders=[
            {
                "stakeholder_id": "stk_01",
                "name": "Sarah Jenkins",
                "role": "Champion",
                "email": "sjenkins@acmecorp.com",
                "sentiment": "Positive",
                "influence_level": "High"
            },
            {
                "stakeholder_id": "stk_02",
                "name": "David Miller",
                "role": "Economic Buyer",
                "email": "dmiller@acmecorp.com",
                "sentiment": "Neutral",
                "influence_level": "High"
            },
            {
                "stakeholder_id": "stk_03",
                "name": "Marcus Vance",
                "role": "Technical Evaluator",
                "email": "mvance@acmecorp.com",
                "sentiment": "Positive",
                "influence_level": "Medium"
            }
        ],
        interactions=[
            {
                "interaction_id": "int_discovery_01",
                "account_id": "acc_acme_corp_8821",
                "opportunity_id": "opp_cloud_migration_9912",
                "event_type": "call_transcript",
                "content": (
                    "Discovery call with Sarah Jenkins. Acme Corp requires SOC2 Type II compliance "
                    "and SAML 2.0 SSO integration. Current setup with legacy ERP is causing high latency. "
                    "Budget allocated is approximately $200k ARR."
                )
            },
            {
                "interaction_id": "int_tech_eval_02",
                "account_id": "acc_acme_corp_8821",
                "opportunity_id": "opp_cloud_migration_9912",
                "event_type": "meeting_summary",
                "content": (
                    "Technical deep-dive with Marcus Vance. Evaluated our AI memory architecture against Gong "
                    "and Salesforce Sales Cloud. Marcus noted Salesforce implementation would take 6+ months, "
                    "whereas our Hindsight persistent memory solution deploys seamlessly."
                )
            },
            {
                "interaction_id": "int_exec_review_03",
                "account_id": "acc_acme_corp_8821",
                "opportunity_id": "opp_cloud_migration_9912",
                "event_type": "email_thread",
                "content": (
                    "Email thread with David Miller (Economic Buyer). David expressed concern over seat-based pricing "
                    "expansion at scale. Requested custom ROI calculation and executive alignment briefing."
                )
            }
        ]
    )

    print(f"\n[1] Processing Deal State for Account: {state.account_name} (${state.arr:,.2f} ARR)")
    print(f"    - Current Stage: {state.current_stage}")
    print(f"    - Total Interactions Ingested: {len(state.interactions)}")
    print(f"    - Total Stakeholders Mapped: {len(state.stakeholders)}")

    # 2. Instantiate and Execute Deal Intelligence Agent
    agent = DealIntelligenceAgent()
    processed_state = agent.process_deal(state)

    # 3. Print Intelligence Results & Analytics
    print("\n" + "=" * 80)
    print("                        DIA ANALYTICS & INSIGHTS")
    print("=" * 80)

    analytics = processed_state.analytics_results

    # Hindsight Memory Reflection
    reflection = processed_state.consolidated_reflection or {}
    beliefs = reflection.get("consolidated_beliefs", [])
    if beliefs:
        print("\n▶ Hindsight Memory Reflection (Consolidated Beliefs):")
        for b in beliefs:
            print(f"    🧠 {b}")

    # Health Score
    health = analytics.get("account_health", {})
    print(f"\n▶ Account Health Score: {health.get('health_score')}/100 ({health.get('health_status')})")

    # Win Probability & Diagnostics
    win_loss = analytics.get("win_loss_diagnostics", {})
    print(f"▶ Computed Win Probability: {int(win_loss.get('win_probability', 0) * 100)}%")
    print("▶ Causal Risk Vectors:")
    for risk in win_loss.get("causal_risk_vectors", []):
        print(f"    - {risk}")
    print("▶ Prescriptive Next-Best-Actions (NBA):")
    for nba in win_loss.get("prescriptive_next_best_actions", []):
        print(f"    ✔ {nba}")

    # Competitors Mentioned
    competitors = analytics.get("competitors_mentioned", [])
    print(f"▶ Identified Competitor Mentions: {', '.join([c.capitalize() for c in competitors])}")

    # 4. Print Staged Workspace MCP Actions
    print("\n" + "=" * 80)
    print("                   STAGED WORKSPACE MCP ACTIONS")
    print("=" * 80)
    for idx, action in enumerate(processed_state.staged_actions, 1):
        print(f"\n[MCP Action #{idx}] Tool: {action.get('tool')}")
        res = action.get("result", {})
        if "draft_id" in res:
            print(f"    - Gmail Draft ID: {res.get('draft_id')}")
            print(f"    - Recipient: {res.get('to')}")
            print(f"    - Subject: {res.get('subject')}")
        elif "conference_link" in res:
            print(f"    - Meeting Event ID: {res.get('event_id')}")
            print(f"    - Summary: {res.get('summary')}")
            print(f"    - Google Meet Link: {res.get('conference_link')}")

    # 5. Generate PDF Deal Dossier
    print("\n" + "=" * 80)
    print("                 PROGRAMMATIC PDF DOSSIER GENERATION")
    print("=" * 80)

    pdf_filename = "acme_corp_deal_dossier.pdf"
    report_gen = ReportGenerator()
    pdf_path = report_gen.generate_pdf_dossier(
        output_filepath=pdf_filename,
        account_name=processed_state.account_name,
        opportunity_data={
            "stage": processed_state.current_stage,
            "arr": processed_state.arr
        },
        analytics_summary={
            "win_probability": win_loss.get("win_probability", 0.5),
            "health_status": health.get("health_status", "Healthy"),
            "top_risk": win_loss.get("causal_risk_vectors", ["None"])[0] if win_loss.get("causal_risk_vectors") else "None",
            "pitch_narrative": processed_state.pitch_narrative,
            "next_best_actions": win_loss.get("prescriptive_next_best_actions", [])
        }
    )

    print(f"\n Successfully generated Deal Dossier PDF: {os.path.abspath(pdf_path)}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
