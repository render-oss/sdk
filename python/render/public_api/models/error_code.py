from enum import Enum


class ErrorCode(str, Enum):
    CURSOR_ORIGIN_RECEIPT_EXPIRED = "cursor_origin_receipt_expired"
    CURSOR_ORIGIN_RECEIPT_INVALID = "cursor_origin_receipt_invalid"
    DUPLICATE_SAVED_SEARCH_NAME = "duplicate_saved_search_name"
    MULTIPLE_REGIONS = "multiple_regions"
    PREAUTH_ATTEMPT_SPENT = "preauth_attempt_spent"
    PREAUTH_CONSENT_REQUIRED = "preauth_consent_required"
    PREAUTH_DECLINED = "preauth_declined"
    PREAUTH_NO_PAYMENT_METHOD = "preauth_no_payment_method"
    PREAUTH_UNAVAILABLE = "preauth_unavailable"
    TOO_MANY_RESOURCES = "too_many_resources"

    def __str__(self) -> str:
        return str(self.value)
