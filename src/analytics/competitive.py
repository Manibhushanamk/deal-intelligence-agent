from typing import List, Dict, Any

class RealTimeCompetitiveIntelligence:
    """
    Extracts competitor mentions, triggers automated battlecard counters, and monitors market shifts across deal pipelines.
    """
    BATTLECARDS = {
        "salesforce": {
            "competitor_name": "Salesforce Sales Cloud",
            "weaknesses": ["High total cost of ownership", "Complex implementation setup", "Steep learning curve for reps"],
            "differentiators": ["Native AI agent automation", "Zero-friction workflow setup", "Transparent flat pricing"],
            "objection_handling": "While Salesforce is robust, implementation takes 6+ months. Our solution deploys in 2 weeks with automated Hindsight memory."
        },
        "hubspot": {
            "competitor_name": "HubSpot Sales Hub",
            "weaknesses": ["Limited enterprise customization", "Expensive tiered seats at scale", "Basic AI memory depth"],
            "differentiators": ["Deep long-term multi-session memory", "Cross-deal predictive reasoning", "Enterprise RBAC"],
            "objection_handling": "HubSpot works for SMBs, but lacks cross-session cognitive retention required for complex multi-month B2B sales cycles."
        },
        "gong": {
            "competitor_name": "Gong.io",
            "weaknesses": ["Passive recording without autonomous agent execution", "High seat cost for full analytics"],
            "differentiators": ["Autonomous action execution via Google Workspace", "Active memory-driven agent follow-ups"],
            "objection_handling": "Gong records what happened; our Deal Intelligence Agent acts on it by scheduling meetings and drafting follow-ups."
        }
    }

    def extract_competitor_mentions(self, text: str) -> List[str]:
        """
        Scans transcript text for competitor mentions.
        """
        text_lower = text.lower()
        found = []
        for comp in self.BATTLECARDS.keys():
            if comp in text_lower:
                found.append(comp)
        return found

    def get_battlecard(self, competitor_key: str) -> Dict[str, Any]:
        """
        Retrieves contextual battlecard for a given competitor.
        """
        key = competitor_key.lower()
        return self.BATTLECARDS.get(key, {
            "competitor_name": competitor_key.capitalize(),
            "weaknesses": ["Unknown competitor baseline"],
            "differentiators": ["Focus on customer-specific ROI and AI agent capabilities"],
            "objection_handling": "Highlight superior multi-session memory and Google Workspace automation."
        })

    def analyze_pipeline_competitor_density(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates frequency of emerging competitors across active deal pipelines.
        """
        counts = {}
        for inter in interactions:
            mentions = self.extract_competitor_mentions(inter.get("content", ""))
            for comp in mentions:
                counts[comp] = counts.get(comp, 0) + 1

        return {
            "competitor_mention_counts": counts,
            "most_frequent_competitor": max(counts, key=counts.get) if counts else "None"
        }
