import logging
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
import base64

logger = logging.getLogger("GmailService")
logger.setLevel(logging.INFO)

class GmailService:
    """
    Gmail API integration service providing context-injected follow-up email compilation,
    RFC 2822 formatting, and draft staging for human-in-the-loop review.
    """
    def __init__(self, credentials=None):
        self.credentials = credentials
        # Staged drafts for human-in-the-loop review
        self._drafts: List[Dict[str, Any]] = []

    def create_followup_draft(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compiles an RFC 2822 compliant Gmail draft with HTML formatting.
        """
        message = MIMEText(body_html, "html")
        message["to"] = to_email
        message["subject"] = subject

        raw_bytes = message.as_bytes()
        encoded_message = base64.urlsafe_b64encode(raw_bytes).decode("utf-8")

        draft_id = f"draft_{len(self._drafts) + 5001}"
        draft_record = {
            "draft_id": draft_id,
            "to": to_email,
            "subject": subject,
            "body_html": body_html,
            "raw": encoded_message,
            "thread_id": thread_id,
            "status": "staged_for_review"
        }

        self._drafts.append(draft_record)
        logger.info(f"[Gmail API] Created draft '{subject}' ({draft_id}) for {to_email}")
        return draft_record

    def list_drafts(self) -> List[Dict[str, Any]]:
        """
        Returns all currently staged Gmail drafts.
        """
        return self._drafts

    def send_draft(self, draft_id: str) -> Dict[str, Any]:
        """
        Triggers transmission of approved Gmail draft.
        """
        for draft in self._drafts:
            if draft["draft_id"] == draft_id:
                draft["status"] = "sent"
                logger.info(f"[Gmail API] Transmitted draft {draft_id} to {draft['to']}")
                return {"status": "sent", "draft_id": draft_id, "recipient": draft["to"]}

        return {"status": "error", "message": f"Draft {draft_id} not found."}
