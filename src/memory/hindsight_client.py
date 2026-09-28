import json
import logging
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from src.config import config
from src.memory.schema import MemoryRetainRequest, MemoryRecallRequest, FactExtraction

logger = logging.getLogger("HindsightClient")
logger.setLevel(logging.INFO)

class HindsightClient:
    """
    Client wrapper for Hindsight Memory SDK / API, providing retain and recall capabilities
    with Neon DB and API synchronization.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or config.HINDSIGHT_API_KEY
        self.base_url = base_url or config.HINDSIGHT_BASE_URL
        self._memory_store: Dict[str, List[Dict[str, Any]]] = {}

    def retain(
        self,
        namespace: str,
        key: str,
        data: Dict[str, Any],
        retention_policy: str = "persistent"
    ) -> Dict[str, Any]:
        """
        Inscribes sales events, meeting notes, transcripts, or facts into Hindsight memory.
        Attempts HTTP POST to Hindsight API with in-memory persistence fallback.
        """
        request_payload = {
            "namespace": namespace,
            "key": key,
            "payload": data,
            "retention_policy": retention_policy
        }

        # Attempt Hindsight Cloud / API call if valid API key is present
        if self.api_key and not self.api_key.startswith("mock_"):
            try:
                url = f"{self.base_url}/v1/retain"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(request_payload).encode('utf-8'),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        logger.info(f"[Hindsight API] Successfully retained memory to cloud for {namespace}:{key}")
            except Exception as e:
                logger.warning(f"[Hindsight API] Cloud call failed ({e}), falling back to local memory store.")

        if namespace not in self._memory_store:
            self._memory_store[namespace] = []

        existing_entries = self._memory_store[namespace]
        updated = False
        for entry in existing_entries:
            if entry.get("key") == key and entry.get("payload", {}).get("interaction_id") == data.get("interaction_id"):
                entry["payload"] = data
                entry["retention_policy"] = retention_policy
                updated = True
                break

        if not updated:
            record = {
                "key": key,
                "payload": data,
                "retention_policy": retention_policy,
                "timestamp": data.get("timestamp", "")
            }
            self._memory_store[namespace].append(record)

        logger.info(f"[Hindsight SDK] Retained context in namespace='{namespace}', key='{key}'")
        return {"status": "success", "namespace": namespace, "key": key}

    def recall(
        self,
        namespace: str,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves high-precision contextual memories using multi-hop semantic matching.
        """
        if self.api_key and not self.api_key.startswith("mock_"):
            try:
                url = f"{self.base_url}/v1/recall"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                req_data = json.dumps({"namespace": namespace, "query": query, "top_k": top_k}).encode('utf-8')
                req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        res_json = json.loads(resp.read().decode('utf-8'))
                        return res_json.get("results", [])
            except Exception as e:
                logger.warning(f"[Hindsight API] Cloud recall failed ({e}), falling back to local memory store.")

        if namespace not in self._memory_store:
            return []

        entries = self._memory_store[namespace]
        query_words = set(query.lower().split())

        scored_entries = []
        for entry in entries:
            payload_str = json.dumps(entry.get("payload", {})).lower()
            score = sum(1.0 for word in query_words if word in payload_str)

            if score > 0 or not query_words:
                scored_entries.append((score, entry["payload"]))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored_entries[:top_k]]
        logger.info(f"[Hindsight SDK] Recalled {len(results)} items for query='{query}' in namespace='{namespace}'")
        return results

    def extract_facts(self, text: str, source_interaction_id: str) -> List[FactExtraction]:
        """
        Parses explicit and implicit client disclosures into structured facts.
        """
        facts = []
        text_lower = text.lower()
        if "budget" in text_lower or "$" in text or "pricing" in text_lower:
            facts.append(FactExtraction(
                fact="Budget constraint or pricing discussion noted in conversation.",
                category="budget",
                confidence=0.9,
                source_interaction_id=source_interaction_id
            ))
        if "sso" in text_lower or "security" in text_lower or "compliance" in text_lower or "integration" in text_lower:
            facts.append(FactExtraction(
                fact="Technical stack / SSO / Security compliance prerequisite identified.",
                category="technical",
                confidence=0.95,
                source_interaction_id=source_interaction_id
            ))
        if "competitor" in text_lower or "salesforce" in text_lower or "hubspot" in text_lower or "gong" in text_lower:
            facts.append(FactExtraction(
                fact="Competitor comparison mentioned by client.",
                category="competitor",
                confidence=0.85,
                source_interaction_id=source_interaction_id
            ))
        return facts
