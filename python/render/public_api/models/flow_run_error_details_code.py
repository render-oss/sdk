from enum import Enum


class FlowRunErrorDetailsCode(str, Enum):
    FLOW_DETERMINISM_ERROR = "flow_determinism_error"
    FLOW_HISTORY_TOO_LARGE = "flow_history_too_large"
    FLOW_PAYLOAD_TOO_LARGE = "flow_payload_too_large"
    FLOW_STEP_LIMIT_EXCEEDED = "flow_step_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
