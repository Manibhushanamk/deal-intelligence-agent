from typing import Dict, Any, List, Optional
from src.workspace.calendar_service import CalendarService
from src.workspace.gmail_service import GmailService
from src.workspace.neon_client import NeonDatabaseClient

class WorkspaceMCPTools:
    """
    Model Context Protocol (MCP) standardized tools wrapper for Google Workspace
    actions and Neon database persistence operations.
    """
    def __init__(
        self,
        calendar_service: CalendarService,
        gmail_service: GmailService,
        neon_client: Optional[NeonDatabaseClient] = None
    ):
        self.calendar_service = calendar_service
        self.gmail_service = gmail_service
        self.neon_client = neon_client or NeonDatabaseClient()

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Returns JSON schemas for standardized MCP tools.
        """
        return [
            {
                "name": "google_calendar_freebusy",
                "description": "Query Google Calendar FreeBusy availability for participants.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time_min": {"type": "string"},
                        "time_max": {"type": "string"},
                        "calendar_ids": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["time_min", "time_max", "calendar_ids"]
                }
            },
            {
                "name": "google_calendar_schedule",
                "description": "Schedule a Google Calendar meeting with Google Meet video link.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "description": {"type": "string"},
                        "start_time": {"type": "string"},
                        "end_time": {"type": "string"},
                        "attendees": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["summary", "description", "start_time", "end_time", "attendees"]
                }
            },
            {
                "name": "gmail_create_draft",
                "description": "Create an RFC 2822 formatted follow-up email draft in Gmail.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {"type": "string"},
                        "subject": {"type": "string"},
                        "body_html": {"type": "string"}
                    },
                    "required": ["to_email", "subject", "body_html"]
                }
            },
            {
                "name": "neon_persist_deal_record",
                "description": "Persists structured deal state and interaction log into Neon DB.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "opportunity_id": {"type": "string"},
                        "deal_data": {"type": "object"}
                    },
                    "required": ["account_id", "opportunity_id", "deal_data"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes named MCP tool with validated arguments.
        """
        if tool_name == "google_calendar_freebusy":
            return self.calendar_service.query_freebusy(
                arguments.get("time_min", ""),
                arguments.get("time_max", ""),
                arguments.get("calendar_ids", [])
            )
        elif tool_name == "google_calendar_schedule":
            return self.calendar_service.schedule_meeting(
                arguments.get("summary", ""),
                arguments.get("description", ""),
                arguments.get("start_time", ""),
                arguments.get("end_time", ""),
                arguments.get("attendees", [])
            )
        elif tool_name == "gmail_create_draft":
            return self.gmail_service.create_followup_draft(
                arguments.get("to_email", ""),
                arguments.get("subject", ""),
                arguments.get("body_html", "")
            )
        elif tool_name == "neon_persist_deal_record":
            return self.neon_client.persist_deal_record(
                account_id=arguments.get("account_id", ""),
                opportunity_id=arguments.get("opportunity_id", ""),
                deal_data=arguments.get("deal_data", {})
            )
        else:
            raise ValueError(f"Unknown MCP tool: {tool_name}")
