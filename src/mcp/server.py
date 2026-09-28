import logging
from typing import Dict, Any, List, Optional
from src.workspace.calendar_service import CalendarService
from src.workspace.gmail_service import GmailService
from src.mcp.workspace_tools import WorkspaceMCPTools

logger = logging.getLogger("MCPServer")
logger.setLevel(logging.INFO)

class MCPServer:
    """
    Model Context Protocol (MCP) server implementation for orchestrating workspace actions
    and Neon database interactions.
    """
    def __init__(
        self,
        calendar_service: Optional[CalendarService] = None,
        gmail_service: Optional[GmailService] = None
    ):
        self.calendar_service = calendar_service or CalendarService()
        self.gmail_service = gmail_service or GmailService()
        self.mcp_tools = WorkspaceMCPTools(self.calendar_service, self.gmail_service)

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Lists available MCP tool schemas.
        """
        return self.mcp_tools.get_tool_definitions()

    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles incoming MCP tool execution calls.
        """
        logger.info(f"[MCP Server] Executing tool '{tool_name}' with args: {arguments}")
        try:
            result = self.mcp_tools.execute_tool(tool_name, arguments)
            return {"status": "success", "tool": tool_name, "result": result}
        except Exception as e:
            logger.error(f"[MCP Server] Tool execution error in '{tool_name}': {str(e)}")
            return {"status": "error", "tool": tool_name, "error": str(e)}
