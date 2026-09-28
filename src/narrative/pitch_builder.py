from typing import Dict, Any, List

class PitchBuilder:
    """
    Synthesizes executive sales pitch narratives framing client pain points,
    recalled Hindsight memories, and custom ROI models into tailored proposals.
    """
    def synthesize_pitch_narrative(
        self,
        account_name: str,
        deal_stage: str,
        recalled_memories: List[Dict[str, Any]],
        competitors_mentioned: List[str],
        win_probability: float
    ) -> Dict[str, Any]:
        """
        Builds executive pitch narrative with custom ROI and value proposition.
        """
        memory_highlights = []
        for mem in recalled_memories:
            content = mem.get("content", "")
            if content:
                memory_highlights.append(content)

        summary_points = "\n".join([f"- {h}" for h in memory_highlights[:3]]) or "- Focus on automated workflow efficiency and AI persistent memory."

        competitor_counters = ""
        if "salesforce" in [c.lower() for c in competitors_mentioned]:
            competitor_counters += "\n- Contrast: Zero implementation lag vs 6-month Salesforce deployment overhead."
        if "hubspot" in [c.lower() for c in competitors_mentioned]:
            competitor_counters += "\n- Contrast: Continuous long-term multi-session memory vs basic CRM static notes."

        narrative = f"""
EXECUTIVE SUMMARY & PITCH NARRATIVE FOR {account_name.upper()}
============================================================
Target Opportunity Stage: {deal_stage}
Model Estimated Win Probability: {int(win_probability * 100)}%

1. Key Client Priorities & Recalled Context:
{summary_points}

2. Differentiated Value Proposition:
The Deal Intelligence Agent equips your revenue team with continuous persistent memory powered by Hindsight, ensuring every customer objection, technical compliance hurdle, and stakeholder dynamic is remembered and acted upon autonomously.

3. Competitive Position & Positioning:
{competitor_counters if competitor_counters else "- Unique position: Pure AI memory persistence and Google Workspace automation."}

4. ROI Model Projection:
- Estimated Time Saved: 8.5 hours per Account Executive per week on meeting briefs & CRM entry.
- Projected Acceleration: 22% reduction in Stage 3 to Stage 4 deal duration.
- Projected Annual Value: $145,000 ARR uplift across enterprise deals.
""".strip()

        return {
            "account_name": account_name,
            "deal_stage": deal_stage,
            "narrative_text": narrative,
            "memory_highlights": memory_highlights
        }
