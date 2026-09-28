import logging
from typing import Dict, Any, List, Optional
from src.agent.state import AgentState
from src.memory.hindsight_client import HindsightClient
from src.analytics.cross_deal import CrossDealAnalytics
from src.analytics.relationship import MultiSessionRelationshipIntelligence
from src.analytics.competitive import RealTimeCompetitiveIntelligence
from src.analytics.win_loss import PredictiveWinLossReasoning
from src.narrative.pitch_builder import PitchBuilder
from src.narrative.report_generator import ReportGenerator
from src.mcp.server import MCPServer

logger = logging.getLogger("DealIntelligenceAgent")
logger.setLevel(logging.INFO)

class DealIntelligenceAgent:
    """
    Main cognitive agent orchestrating Hindsight persistent memory,
    cross-deal analytics, competitive intelligence, predictive win-loss reasoning,
    Google Workspace MCP actions, and dossier reporting.
    """
    def __init__(
        self,
        hindsight_client: Optional[HindsightClient] = None,
        mcp_server: Optional[MCPServer] = None
    ):
        self.memory = hindsight_client or HindsightClient()
        self.mcp_server = mcp_server or MCPServer()
        self.cross_deal = CrossDealAnalytics(self.memory)
        self.relationship = MultiSessionRelationshipIntelligence(self.memory)
        self.competitive = RealTimeCompetitiveIntelligence()
        self.win_loss = PredictiveWinLossReasoning()
        self.pitch_builder = PitchBuilder()
        self.report_generator = ReportGenerator()

    def process_deal(self, state: AgentState) -> AgentState:
        """
        Main execution loop processing deal context, memory retention & recall,
        intelligence calculations, and workspace MCP tool staging.
        """
        logger.info(f"[DIA Agent] Processing deal for Account '{state.account_name}' ({state.account_id})")

        # 1. Retain interaction events in Hindsight persistent memory
        for inter in state.interactions:
            self.memory.retain(
                namespace=state.account_id,
                key=inter.get("interaction_id", "gen_key"),
                data=inter
            )

        # 2. Recall historical context from Hindsight & Reflect on beliefs
        recalled = self.memory.recall(
            namespace=state.account_id,
            query="security compliance pricing budget competitor SSO",
            top_k=5
        )
        state.recalled_memories = recalled
        state.consolidated_reflection = self.memory.reflect(
            namespace=state.account_id,
            topic="deal_strategy"
        )

        # 3. Execute Core Intelligence Modules
        pain_points = self.cross_deal.mine_recurring_pain_points(state.interactions)
        health = self.relationship.compute_account_health_score(
            interactions=state.interactions,
            stakeholders=state.stakeholders,
            days_since_last_contact=5
        )

        # Collect competitor mentions across interactions
        all_text = " ".join([i.get("content", "") for i in state.interactions])
        competitors = self.competitive.extract_competitor_mentions(all_text)
        battlecards = [self.competitive.get_battlecard(c) for c in competitors]

        win_loss_diag = self.win_loss.compute_deal_win_probability(
            deal_stage=state.current_stage,
            arr=state.arr,
            stakeholders=state.stakeholders,
            days_in_stage=12,
            has_budget_approval=True
        )

        state.analytics_results = {
            "recurring_pain_points": pain_points,
            "account_health": health,
            "competitors_mentioned": competitors,
            "battlecards": battlecards,
            "win_loss_diagnostics": win_loss_diag
        }

        # 4. Synthesize Dynamic Pitch Narrative
        pitch_res = self.pitch_builder.synthesize_pitch_narrative(
            account_name=state.account_name,
            deal_stage=state.current_stage,
            recalled_memories=recalled,
            competitors_mentioned=competitors,
            win_probability=win_loss_diag["win_probability"]
        )
        state.pitch_narrative = pitch_res["narrative_text"]

        # 5. Stage MCP Workspace Actions (Calendar & Gmail)
        action_draft = self.mcp_server.handle_tool_call(
            "gmail_create_draft",
            {
                "to_email": "buyer@" + state.account_name.lower().replace(" ", "") + ".com",
                "subject": f"Follow-up & Executive Summary - {state.account_name}",
                "body_html": f"<p>{state.pitch_narrative.replace('\n', '<br>')}</p>"
            }
        )

        action_calendar = self.mcp_server.handle_tool_call(
            "google_calendar_schedule",
            {
                "summary": f"Executive Alignment Call - {state.account_name}",
                "description": f"Next Best Action: {win_loss_diag['prescriptive_next_best_actions'][0]}",
                "start_time": "2025-03-15T10:00:00Z",
                "end_time": "2025-03-15T10:30:00Z",
                "attendees": ["ae@company.com", "buyer@" + state.account_name.lower().replace(" ", "") + ".com"]
            }
        )

        state.staged_actions = [action_draft, action_calendar]
        state.execution_status = "completed"

        logger.info(f"[DIA Agent] Successfully completed processing for {state.account_name}")
        return state
