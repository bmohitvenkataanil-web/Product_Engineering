import os
import json
import logging
import httpx
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("llm_service")

class LLMService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL or "llama-3.3-70b-versatile"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def generate_json(self, prompt: str, system_prompt: str = "") -> Optional[Dict[str, Any]]:
        """Call Groq API requesting JSON output."""
        if not self.is_available():
            logger.info("Groq API key not set or empty. Using intelligent rule-based agent engine.")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt + "\nReturn ONLY valid raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                res = client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                if res.status_code == 200:
                    content = res.json()["choices"][0]["message"]["content"]
                    try:
                        return json.loads(content)
                    except Exception:
                        # Attempt cleaning markdown backticks if present
                        cleaned = content.strip()
                        if cleaned.startswith("```json"):
                            cleaned = cleaned[7:]
                        if cleaned.endswith("```"):
                            cleaned = cleaned[:-3]
                        return json.loads(cleaned)
                else:
                    logger.warning(f"Groq API error {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Groq request failed: {e}")

        return None

    def generate_text(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Call Groq API for raw text response."""
        if not self.is_available():
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                res = client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                if res.status_code == 200:
                    return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Groq text generation failed: {e}")

        return None

llm_service = LLMService()
