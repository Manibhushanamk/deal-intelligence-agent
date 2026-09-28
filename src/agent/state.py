from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    account_id: str
    opportunity_id: str
    account_name: str
    current_stage: str
    arr: float
    stakeholders: List[Dict[str, Any]] = Field(default_factory=list)
    interactions: List[Dict[str, Any]] = Field(default_factory=list)
    recalled_memories: List[Dict[str, Any]] = Field(default_factory=list)
    analytics_results: Dict[str, Any] = Field(default_factory=dict)
    pitch_narrative: Optional[str] = None
    staged_actions: List[Dict[str, Any]] = Field(default_factory=list)
    execution_status: str = "initialized"
