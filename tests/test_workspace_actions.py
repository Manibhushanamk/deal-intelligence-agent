import pytest
from src.workspace.calendar_service import CalendarService
from src.workspace.gmail_service import GmailService
from src.mcp.server import MCPServer

def test_calendar_service():
    cal = CalendarService()
    freebusy = cal.query_freebusy("2025-03-10T00:00:00Z", "2025-03-10T23:59:59Z", ["ae@example.com"])
    assert "suggested_free_window" in freebusy

    event = cal.schedule_meeting(
        summary="Demo Call",
        description="Product Demo",
        start_time="2025-03-10T15:00:00Z",
        end_time="2025-03-10T16:00:00Z",
        attendees=["ae@example.com", "prospect@example.com"]
    )
    assert event["status"] == "confirmed"
    assert "https://meet.google.com/" in event["conference_link"]

def test_gmail_service():
    gmail = GmailService()
    draft = gmail.create_followup_draft("buyer@example.com", "Proposal", "<p>Proposal attached</p>")
    assert draft["status"] == "staged_for_review"
    assert len(gmail.list_drafts()) == 1

    send_res = gmail.send_draft(draft["draft_id"])
    assert send_res["status"] == "sent"

def test_mcp_server_workspace_tools():
    server = MCPServer()
    tools = server.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "google_calendar_freebusy" in tool_names
    assert "google_calendar_schedule" in tool_names
    assert "gmail_create_draft" in tool_names
    assert "neon_persist_deal_record" in tool_names

    # Test FreeBusy MCP Tool
    res_fb = server.handle_tool_call(
        "google_calendar_freebusy",
        {"time_min": "2026-09-29T09:00:00Z", "time_max": "2026-09-29T18:00:00Z", "calendar_ids": ["ae@test.com"]}
    )
    assert res_fb["status"] == "success"
    assert "suggested_free_window" in res_fb["result"]

    # Test Calendar Schedule MCP Tool
    res_sched = server.handle_tool_call(
        "google_calendar_schedule",
        {
            "summary": "Executive Alignment",
            "description": "Product Demo",
            "start_time": "2026-09-29T15:00:00Z",
            "end_time": "2026-09-29T16:00:00Z",
            "attendees": ["ae@test.com", "buyer@test.com"]
        }
    )
    assert res_sched["status"] == "success"
    assert res_sched["result"]["status"] == "confirmed"
    assert "https://meet.google.com/" in res_sched["result"]["conference_link"]

    # Test Gmail Create Draft MCP Tool
    res_draft = server.handle_tool_call(
        "gmail_create_draft",
        {"to_email": "buyer@test.com", "subject": "Proposal", "body_html": "<p>ROI Analysis</p>"}
    )
    assert res_draft["status"] == "success"
    assert res_draft["result"]["status"] == "staged_for_review"

    # Test Neon Persist Deal Record MCP Tool
    res_neon = server.handle_tool_call(
        "neon_persist_deal_record",
        {"account_id": "acc_1", "opportunity_id": "opp_1", "deal_data": {"arr": 50000}}
    )
    assert res_neon["status"] == "success"
    assert "persisted_to_neon" in res_neon["result"]["status"]

    # Test Invalid Tool Error Handling
    res_err = server.handle_tool_call("unknown_tool", {})
    assert res_err["status"] == "error"
    assert "Unknown MCP tool" in res_err["error"]
