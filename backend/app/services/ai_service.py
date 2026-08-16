"""Azure AI Foundry Model Router client. Failures return None — never raise to callers."""

from __future__ import annotations

import json
import logging
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

# Foundry agent Responses: v1 and 2025-11-15-preview work. v2 and 2025-04-01-preview do not.
_SUPPORTED_VERSIONS = ("v1", "2025-11-15-preview")
_working_url: str | None = None


def is_configured() -> bool:
    settings = get_settings()
    return bool(settings.azure_ai_endpoint and settings.azure_key)


def complete(prompt: str, *, max_output_tokens: int = 400) -> str | None:
    settings = get_settings()
    if not settings.azure_ai_endpoint or not settings.azure_key:
        logger.info("Azure AI is not configured; skipping model call")
        return None

    headers = {
        "Content-Type": "application/json",
        "api-key": settings.azure_key,
        "Authorization": f"Bearer {settings.azure_key}",
    }
    payloads = [
        {
            "model": settings.azure_ai_model,
            "input": prompt,
            "max_output_tokens": max_output_tokens,
        },
        {
            "model": settings.azure_ai_model,
            "input": prompt,
        },
    ]

    try:
        with httpx.Client(timeout=settings.azure_ai_timeout_seconds) as client:
            last_error = None
            for url in _candidate_urls(settings):
                for body in payloads:
                    try:
                        response = client.post(url, headers=headers, json=body)
                        if response.status_code >= 400:
                            last_error = response.text[:300]
                            if "API version not supported" in response.text:
                                break
                            logger.warning("Azure AI HTTP %s: %s", response.status_code, last_error)
                            continue
                        text = _extract_text(response.json())
                        if text:
                            _remember_url(url)
                            return text.strip()
                    except httpx.TimeoutException:
                        logger.warning("Azure AI request timed out")
                        return None
                    except httpx.HTTPError as exc:
                        logger.warning("Azure AI HTTP error: %s", exc)
                        continue
            if last_error:
                logger.warning("Azure AI request failed after retries: %s", last_error)
    except Exception as exc:  # noqa: BLE001 — AI must never break a page
        logger.warning("Azure AI call failed: %s", exc)
        return None
    return None


def _candidate_urls(settings) -> list[str]:
    base, embedded_version = _strip_api_version(settings.azure_ai_endpoint)
    configured = (embedded_version or settings.azure_ai_api_version or "v1").strip()
    versions: list[str] = []
    for version in (configured, *_SUPPORTED_VERSIONS):
        if version and version not in versions:
            versions.append(version)
    joiner = "&" if "?" in base else "?"
    urls = [f"{base}{joiner}api-version={version}" for version in versions]
    if _working_url and _working_url in urls:
        return [_working_url, *[url for url in urls if url != _working_url]]
    return urls


def _strip_api_version(endpoint: str) -> tuple[str, str | None]:
    parts = urlsplit(endpoint.strip())
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "api-version"]
    embedded = dict(parse_qsl(parts.query)).get("api-version")
    rebuilt = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    return rebuilt.rstrip("?"), embedded


def _remember_url(url: str) -> None:
    global _working_url
    _working_url = url


def complete_json(prompt: str) -> dict | list | None:
    raw = complete(prompt + "\n\nReply with JSON only.", max_output_tokens=600)
    if not raw:
        return None
    return parse_json(raw)


def parse_json(raw: str) -> dict | list | None:
    cleaned = raw.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", cleaned)
    if fenced:
        cleaned = fenced.group(1).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                return None
        start = cleaned.find("[")
        end = cleaned.rfind("]")
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


def _extract_text(data: object) -> str | None:
    if not isinstance(data, dict):
        return None
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return data["output_text"]
    output = data.get("output")
    if isinstance(output, list):
        chunks: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("text"):
                        chunks.append(str(part["text"]))
            elif isinstance(content, str):
                chunks.append(content)
        if chunks:
            return "\n".join(chunks)
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if isinstance(message, dict) and message.get("content"):
            return str(message["content"])
        if isinstance(choices[0], dict) and choices[0].get("text"):
            return str(choices[0]["text"])
    if isinstance(data.get("content"), str):
        return data["content"]
    return None
