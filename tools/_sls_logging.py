from __future__ import annotations

import time
from typing import Any

from aliyun.log import LogClient, LogItem, PutLogsRequest


SLS_LOGSTORE = "flyfus-dify-llm-log"


def write_tool_log(credentials: dict[str, Any], log_id: str, event: str, **fields: object) -> None:
    endpoint = str(credentials.get("sls_endpoint") or "").strip()
    project = str(credentials.get("sls_project") or "").strip()
    access_key_id = str(credentials.get("sls_access_key_id") or "").strip()
    access_key_secret = str(credentials.get("sls_access_key_secret") or "").strip()
    if not endpoint or not project or not access_key_id or not access_key_secret:
        return

    contents = [("log_id", log_id), ("event", event), ("source", "flypower_tool")]
    contents.extend((key, str(value)) for key, value in fields.items() if value is not None)
    try:
        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents(contents)
        LogClient(endpoint, access_key_id, access_key_secret).put_logs(
            PutLogsRequest(project, SLS_LOGSTORE, "flypower-tool", "", [log_item])
        )
    except Exception:
        # Diagnostic delivery must never change the tool invocation result.
        return
