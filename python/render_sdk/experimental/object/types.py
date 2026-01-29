"""Type definitions for the experimental object storage API."""

from dataclasses import dataclass
from datetime import datetime

# Re-export Region from the generated models for user convenience.
# While region accepts strings, exporting Region allows users to see
# available values via IDE autocomplete.
from render_sdk.public_api.models.region import Region  # noqa: F401

# Type alias for owner ID format
OwnerID = str  # Should match pattern tea-xxxxx


@dataclass
class UploadResponse:
    """Response containing upload URL and metadata."""

    url: str
    """Presigned upload URL"""

    expires_at: datetime
    """Expiration timestamp"""

    max_size_bytes: int
    """Maximum size allowed for upload"""


@dataclass
class DownloadResponse:
    """Response containing download URL and metadata."""

    url: str
    """Presigned download URL"""

    expires_at: datetime
    """Expiration timestamp"""


@dataclass
class ObjectData:
    """Downloaded object data."""

    data: bytes
    """Binary content"""

    size: int
    """Size in bytes"""

    content_type: str | None = None
    """MIME type if available"""


@dataclass
class PutObjectResult:
    """Result from uploading an object."""

    etag: str | None = None
    """ETag from storage provider"""
