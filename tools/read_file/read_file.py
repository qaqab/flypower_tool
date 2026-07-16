from __future__ import annotations

import json
import re
from collections.abc import Generator
from urllib.parse import urlparse

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class ReadFileTool(Tool):
    _TAG_NAME = "FLYPOWER_CONTEXT"
    _INTERNAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "web", "nginx", "api"}

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        urls = self._parse_urls(tool_parameters.get("url_list"))
        if not urls:
            error = "Provide at least one public HTTP or HTTPS URL."
            yield self.create_json_message({"urls": [], "error": error})
            yield self.create_text_message("[]")
            return

        context = {
            "version": 1,
            "type": "flypower_context",
            "urls": urls,
        }
        encoded_context = json.dumps(context, ensure_ascii=False, separators=(",", ":"))
        yield self.create_json_message({"urls": urls})
        yield self.create_text_message(f"<{self._TAG_NAME}>{encoded_context}</{self._TAG_NAME}>")

    @classmethod
    def _parse_urls(cls, value: object) -> list[str]:
        if not isinstance(value, str):
            return []

        urls: list[str] = []
        seen: set[str] = set()
        for raw_url in re.split(r"[,\r\n]+", value):
            url = raw_url.strip().strip('"').strip("'")
            if not cls._is_public_http_url(url) or url in seen:
                continue
            seen.add(url)
            urls.append(url)
        return urls

    @classmethod
    def _is_public_http_url(cls, url: str) -> bool:
        parsed = urlparse(url)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and parsed.hostname not in cls._INTERNAL_HOSTS
        )
