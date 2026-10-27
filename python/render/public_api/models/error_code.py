from enum import Enum


class ErrorCode(str, Enum):
    BUILD_NOT_FOUND = "build_not_found"
    BUILD_NOT_SUCCEEDED = "build_not_succeeded"
    CURSOR_ORIGIN_RECEIPT_EXPIRED = "cursor_origin_receipt_expired"
    CURSOR_ORIGIN_RECEIPT_INVALID = "cursor_origin_receipt_invalid"
    DUPLICATE_SAVED_SEARCH_NAME = "duplicate_saved_search_name"
    INVALID_CURSOR = "invalid_cursor"
    INVALID_LIMIT = "invalid_limit"
    INVALID_OWNER_ID = "invalid_owner_id"
    INVALID_SANDBOX_GROUP_ID = "invalid_sandbox_group_id"
    INVALID_SANDBOX_PLAN = "invalid_sandbox_plan"
    INVALID_SNAPSHOT_ID = "invalid_snapshot_id"
    INVALID_SNAPSHOT_NAME = "invalid_snapshot_name"
    INVALID_STATUS = "invalid_status"
    INVALID_TIMEOUT_SECONDS = "invalid_timeout_seconds"
    MULTIPLE_REGIONS = "multiple_regions"
    PREAUTH_ATTEMPT_SPENT = "preauth_attempt_spent"
    PREAUTH_CONSENT_REQUIRED = "preauth_consent_required"
    PREAUTH_DECLINED = "preauth_declined"
    PREAUTH_NO_PAYMENT_METHOD = "preauth_no_payment_method"
    PREAUTH_UNAVAILABLE = "preauth_unavailable"
    SANDBOX_GROUP_LIMIT_REACHED = "sandbox_group_limit_reached"
    SANDBOX_GROUP_SUSPENDED = "sandbox_group_suspended"
    SANDBOX_NOT_RUNNING = "sandbox_not_running"
    SNAPSHOT_CREATING = "snapshot_creating"
    SNAPSHOT_NOT_AVAILABLE = "snapshot_not_available"
    SNAPSHOT_NOT_FOUND = "snapshot_not_found"
    SNAPSHOT_PLAN_MISMATCH = "snapshot_plan_mismatch"
    TOO_MANY_RESOURCES = "too_many_resources"

    def __str__(self) -> str:
        return str(self.value)
