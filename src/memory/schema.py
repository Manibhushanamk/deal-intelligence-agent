from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Stakeholder(BaseModel):
    stakeholder_id: str
    name: str
    role: str # e.g. "Economic Buyer", "Technical Evaluator", "Champion", "Blocker"
    email: Optional[str] = None
    sentiment: str = "Neutral" # e.g. "Positive", "Neutral", "Negative"
    influence_level: str = "Medium" # e.g. "High", "Medium", "Low"

class Opportunity(BaseModel):
    opportunity_id: str
    account_id: str
    deal_name: str
    stage: str # e.g. "Qualification", "Discovery", "Proposal", "Negotiation", "Closed Won", "Closed Lost"
    arr: float
    win_probability: float = 0.5
    stakeholders: List[Stakeholder] = Field(default_factory=list)

class InteractionPayload(BaseModel):
    interaction_id: str
    account_id: str
    opportunity_id: str
    stakeholder_id: Optional[str] = None
    event_type: str # e.g. "call_transcript", "meeting_summary", "email_thread"
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FactExtraction(BaseModel):
    fact: str
    category: str # "budget", "technical", "competitor", "sentiment", "milestone"
    confidence: float = 1.0
    source_interaction_id: str

class MemoryRetainRequest(BaseModel):
    namespace: str # account_id
    key: str # stakeholder_id or opportunity_id
    payload: Dict[str, Any]
    retention_policy: str = "persistent"

class MemoryRecallRequest(BaseModel):
    namespace: str # account_id
    query: str
    top_k: int = 5
