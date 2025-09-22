import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.custom_domain_domain_type import CustomDomainDomainType
from ..models.custom_domain_verification_status import CustomDomainVerificationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_domain_server import CustomDomainServer


T = TypeVar("T", bound="CustomDomain")


@_attrs_define
class CustomDomain:
    """
    Attributes:
        id (str):
        name (str):
        domain_type (CustomDomainDomainType):
        public_suffix (str):
        redirect_for_name (str):
        verification_status (CustomDomainVerificationStatus):
        created_at (datetime.datetime):
        server (Union[Unset, CustomDomainServer]):
    """

    id: str
    name: str
    domain_type: CustomDomainDomainType
    public_suffix: str
    redirect_for_name: str
    verification_status: CustomDomainVerificationStatus
    created_at: datetime.datetime
    server: Union[Unset, "CustomDomainServer"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        domain_type = self.domain_type.value

        public_suffix = self.public_suffix

        redirect_for_name = self.redirect_for_name

        verification_status = self.verification_status.value

        created_at = self.created_at.isoformat()

        server: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.server, Unset):
            server = self.server.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "domainType": domain_type,
                "publicSuffix": public_suffix,
                "redirectForName": redirect_for_name,
                "verificationStatus": verification_status,
                "createdAt": created_at,
            }
        )
        if server is not UNSET:
            field_dict["server"] = server

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_domain_server import CustomDomainServer

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        domain_type = CustomDomainDomainType(d.pop("domainType"))

        public_suffix = d.pop("publicSuffix")

        redirect_for_name = d.pop("redirectForName")

        verification_status = CustomDomainVerificationStatus(d.pop("verificationStatus"))

        created_at = isoparse(d.pop("createdAt"))

        _server = d.pop("server", UNSET)
        server: Union[Unset, CustomDomainServer]
        if isinstance(_server, Unset):
            server = UNSET
        else:
            server = CustomDomainServer.from_dict(_server)

        custom_domain = cls(
            id=id,
            name=name,
            domain_type=domain_type,
            public_suffix=public_suffix,
            redirect_for_name=redirect_for_name,
            verification_status=verification_status,
            created_at=created_at,
            server=server,
        )

        custom_domain.additional_properties = d
        return custom_domain

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
