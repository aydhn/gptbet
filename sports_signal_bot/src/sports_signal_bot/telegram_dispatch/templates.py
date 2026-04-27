from typing import Dict, Any, List
from .contracts import (
    MessageType,
    DispatchPayloadRecord,
    ReviewQueueRecord,
    SummaryMessageRecord,
    AlarmMessageRecord,
    MessageSeverity
)

class MessageTemplateEngine:
    def __init__(self, templates_config: Dict[str, Any]):
        self.config = templates_config
        self.profile = self._get_active_profile()

    def _get_active_profile(self) -> str:
        profiles = self.config.get("dispatch_profiles", {})
        if profiles.get("verbose"): return "verbose"
        if profiles.get("standard"): return "standard"
        return "short"

    def _escape_markdown_v2(self, text: str) -> str:
        """Escape special characters for Telegram MarkdownV2."""
        if not text:
            return ""
        # The characters to escape: _ * [ ] ( ) ~ ` > # + - = | { } . !
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        escaped_text = text
        for char in escape_chars:
            escaped_text = escaped_text.replace(char, f"\\{char}")
        return escaped_text

    def render_decision(self, payload: DispatchPayloadRecord, run_id: str = "N/A") -> str:
        """Render a decision message."""
        title = f"Decision: {payload.event_id} | {payload.market}"
        lines = [
            f"*{self._escape_markdown_v2(title)}*",
            f"Sport: {self._escape_markdown_v2(payload.sport)}",
            f"Action Class: {self._escape_markdown_v2(payload.decision_class)}",
            f"Signal Score: {payload.signal_score:.2f}",
            f"Edge: {payload.edge:.2f}",
            f"Allocated Stake: {payload.allocated_stake:.2f}u"
        ]

        if self.profile in ["standard", "verbose"]:
            lines.append(f"Rationale: {self._escape_markdown_v2(payload.rationale)}")
            lines.append(f"Run ID: {self._escape_markdown_v2(run_id)}")

        if payload.warnings:
            lines.append("\n*Warnings:*")
            for w in payload.warnings:
                lines.append(f"\\- {self._escape_markdown_v2(w)}")

        return "\n".join(lines)

    def render_review(self, record: ReviewQueueRecord) -> str:
        """Render a review queue item."""
        title = f"Review Required: {record.event_id}"
        lines = [
            f"*{self._escape_markdown_v2(title)}*",
            f"Sport: {self._escape_markdown_v2(record.sport)} | Market: {self._escape_markdown_v2(record.market)}",
            f"Priority: {self._escape_markdown_v2(record.priority.level)} \\({record.priority.score:.2f}\\)",
            "",
            "*Reasons:*"
        ]
        for reason in record.reasons:
            lines.append(f"\\- {self._escape_markdown_v2(reason.code)}: {self._escape_markdown_v2(reason.description)}")

        lines.append("")
        lines.append(f"*Signal Summary:* {self._escape_markdown_v2(record.signal_summary)}")
        return "\n".join(lines)

    def render_summary(self, summary: SummaryMessageRecord) -> str:
        title = f"Run Summary: {summary.run_id}"
        lines = [
            f"*{self._escape_markdown_v2(title)}*",
            f"Slot: {self._escape_markdown_v2(summary.slot)}",
            f"Universe Size: {summary.universe_size}",
            f"Approved: {summary.approved_count}",
            f"Candidate: {summary.candidate_count}",
            f"Watchlist: {summary.watchlist_count}",
            f"Fallback/Degrade: {summary.fallback_count}",
            f"Alarms: {summary.alarms_count}",
        ]

        if summary.top_decisions and self.profile in ["standard", "verbose"]:
            lines.append("\n*Top Decisions:*")
            for d in summary.top_decisions[:3]: # Show max 3 in summary
                 lines.append(f"\\- {self._escape_markdown_v2(d.event_id)} \\({self._escape_markdown_v2(d.market)}\\): {self._escape_markdown_v2(d.decision_class)}")

        return "\n".join(lines)

    def render_alarm(self, alarm: AlarmMessageRecord) -> str:
        # Alarms should probably always be verbose
        icon = "🚨" if alarm.severity == MessageSeverity.CRITICAL else "⚠️"
        title = f"{icon} {alarm.severity.value.upper()}: {alarm.incident_title}"
        lines = [
            f"*{self._escape_markdown_v2(title)}*",
            f"Failing Step: {self._escape_markdown_v2(alarm.failing_step)}",
            f"Run ID: {self._escape_markdown_v2(alarm.run_id)}",
            f"Cause: {self._escape_markdown_v2(alarm.cause)}",
            f"Impacted Events: {alarm.impacted_events_count}",
            f"Status: {self._escape_markdown_v2(alarm.status)}"
        ]
        return "\n".join(lines)

    def render_warning(self, title: str, description: str, run_id: str) -> str:
        lines = [
            f"*{self._escape_markdown_v2('WARNING: ' + title)}*",
            f"Run ID: {self._escape_markdown_v2(run_id)}",
            f"{self._escape_markdown_v2(description)}"
        ]
        return "\n".join(lines)
