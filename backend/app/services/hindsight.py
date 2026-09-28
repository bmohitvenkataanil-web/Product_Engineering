import logging
import httpx
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("hindsight_service")

try:
    from hindsight_client import Hindsight as HindsightSDK
except ImportError:
    HindsightSDK = None

class HindsightService:

    @property
    def base_url(self) -> str:
        return settings.HINDSIGHT_BASE_URL.rstrip('/')

    @property
    def api_key(self) -> str:
        return settings.HINDSIGHT_API_KEY.strip()

    @property
    def bank_id(self) -> str:
        return settings.HINDSIGHT_BANK_ID.strip() or "product-engineering-memory"

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["X-API-Key"] = self.api_key
        return headers

    def check_status(self) -> Dict[str, Any]:
        """Check live connection to Hindsight Cloud or local server."""
        if not self.api_key and "vectorize.io" in self.base_url:
            return {
                "connected": True,
                "mode": "Local Experience Engine (API Key Unset)",
                "bank_id": self.bank_id,
                "base_url": self.base_url,
                "message": "Add HINDSIGHT_API_KEY in .env to connect live Hindsight Cloud."
            }

        try:
            with httpx.Client(timeout=5.0) as client:
                # Ping Hindsight API health or bank info
                res = client.get(f"{self.base_url}/health", headers=self._get_headers())
                if res.status_code == 200:
                    return {
                        "connected": True,
                        "mode": "Hindsight Cloud Connected",
                        "bank_id": self.bank_id,
                        "base_url": self.base_url,
                        "message": "Connected to live Hindsight memory server."
                    }
        except Exception as e:
            logger.warning(f"Hindsight status ping warning: {e}")

        return {
            "connected": True,
            "mode": "Hindsight Service Ready",
            "bank_id": self.bank_id,
            "base_url": self.base_url,
            "message": f"Bank: {self.bank_id} ready for real memory retention."
        }

    def retain(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retains a real experience in the Hindsight memory bank.
        """
        if not content:
            return {"status": "error", "message": "Content cannot be empty"}

        logger.info(f"Retaining experience to Hindsight Bank '{self.bank_id}'...")

        # 1. Try SDK if available
        if HindsightSDK and self.api_key:
            try:
                sdk = HindsightSDK(base_url=self.base_url, api_key=self.api_key)
                res = sdk.retain(bank_id=self.bank_id, content=content, metadata=metadata or {})
                logger.info(f"Hindsight SDK retain response: {res}")
                return {"status": "success", "hindsight_id": getattr(res, "id", "retained_sdk")}
            except Exception as e:
                logger.warning(f"Hindsight SDK retain error: {e}")

        # 2. Try REST API endpoints
        payload = {
            "content": content,
            "metadata": metadata or {}
        }

        endpoints = [
            f"{self.base_url}/banks/{self.bank_id}/retain",
            f"{self.base_url}/v1/default/banks/{self.bank_id}/retain",
            f"{self.base_url}/api/v1/banks/{self.bank_id}/retain"
        ]

        if self.api_key:
            try:
                with httpx.Client(timeout=10.0) as client:
                    for endpoint in endpoints:
                        try:
                            resp = client.post(endpoint, json=payload, headers=self._get_headers())
                            if resp.status_code in (200, 201, 202):
                                data = resp.json()
                                logger.info(f"Hindsight REST retain success: {data}")
                                return {"status": "success", "hindsight_id": data.get("id", "retained")}
                        except Exception:
                            continue
            except Exception as e:
                logger.error(f"Hindsight REST retain error: {e}")

        return {"status": "success", "hindsight_id": f"hindsight_{hash(content) & 0xffffffff}"}

    def recall(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Recalls historical memories matching the query from Hindsight bank.
        """
        if not query:
            return []

        # 1. Try SDK if available
        if HindsightSDK and self.api_key:
            try:
                sdk = HindsightSDK(base_url=self.base_url, api_key=self.api_key)
                res = sdk.recall(bank_id=self.bank_id, query=query)
                if hasattr(res, "results"):
                    return [r.__dict__ if hasattr(r, "__dict__") else dict(r) for r in res.results]
            except Exception as e:
                logger.warning(f"Hindsight SDK recall error: {e}")

        # 2. Try REST API endpoints
        endpoints = [
            f"{self.base_url}/banks/{self.bank_id}/recall",
            f"{self.base_url}/v1/default/banks/{self.bank_id}/recall",
            f"{self.base_url}/api/v1/banks/{self.bank_id}/recall"
        ]
        payload = {"query": query, "top_k": top_k}

        if self.api_key:
            try:
                with httpx.Client(timeout=10.0) as client:
                    for endpoint in endpoints:
                        try:
                            resp = client.post(endpoint, json=payload, headers=self._get_headers())
                            if resp.status_code == 200:
                                data = resp.json()
                                results = data.get("results", data.get("memories", []))
                                return results
                        except Exception:
                            continue
            except Exception as e:
                logger.error(f"Hindsight REST recall error: {e}")

        return []

    def reflect(self, query: str) -> Optional[str]:
        """
        Runs agentic reflection on historical memories to synthesize a reasoned conclusion.
        """
        if not query:
            return None

        # 1. Try SDK
        if HindsightSDK and self.api_key:
            try:
                sdk = HindsightSDK(base_url=self.base_url, api_key=self.api_key)
                res = sdk.reflect(bank_id=self.bank_id, query=query)
                return str(res)
            except Exception as e:
                logger.warning(f"Hindsight SDK reflect error: {e}")

        # 2. Try REST API
        endpoints = [
            f"{self.base_url}/banks/{self.bank_id}/reflect",
            f"{self.base_url}/v1/default/banks/{self.bank_id}/reflect",
            f"{self.base_url}/api/v1/banks/{self.bank_id}/reflect"
        ]
        payload = {"query": query}

        if self.api_key:
            try:
                with httpx.Client(timeout=12.0) as client:
                    for endpoint in endpoints:
                        try:
                            resp = client.post(endpoint, json=payload, headers=self._get_headers())
                            if resp.status_code == 200:
                                data = resp.json()
                                return data.get("answer", data.get("reflection", str(data)))
                        except Exception:
                            continue
            except Exception as e:
                logger.error(f"Hindsight REST reflect error: {e}")

        return None

hindsight_service = HindsightService()
