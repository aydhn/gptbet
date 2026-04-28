from typing import List
from sports_signal_bot.approvals.contracts import ReviewItemRecord

class ApprovalReporter:
    @staticmethod
    def generate_review_message(item: ReviewItemRecord) -> str:
        """Generate a dry-run Telegram/console message for a review item."""
        msg = (
            f"⚠️ REVIEW REQUIRED [{item.risk_level.upper()}]\n"
            f"Title: {item.title}\n"
            f"Summary: {item.summary}\n"
            f"Request ID: {item.request_ref}\n"
            f"Priority: {item.priority}\n"
        )
        if item.suggested_actions:
            msg += "\nSuggested Actions:\n"
            for act in item.suggested_actions:
                msg += f"- {act}\n"

        msg += f"\nCLI:\npython -m sports_signal_bot.main show-approval-request --request-id {item.request_ref}"
        return msg
