from datetime import date
from typing import Optional

from ninja import Field, Schema
from pydantic import ConfigDict, RootModel


class COBusiness(Schema):
    model_config = ConfigDict(populate_by_name=True)
    entity_id: Optional[int] = Field(None, description="CO entity ID", alias="entityid")
    business_name: Optional[str] = Field(None, description="CO entity name", alias="entityname")
    address_line1: Optional[str] = Field(None, description="CO principal address", alias="principaladdress1")
    city: Optional[str] = Field(None, description="CO principal city", alias="principalcity")
    state: Optional[str] = Field(None, description="CO principal state", alias="principalstate")
    zip_code: Optional[str] = Field(None, description="CO principal zip code", alias="principalzipcode")
    status: Optional[str] = Field(None, description="CO business status", alias="entitystatus")
    business_established_date: Optional[date] = Field(
        None, description="CO business established date", alias="entityformdate"
    )


class COBusinessList(RootModel):
    model_config = ConfigDict(populate_by_name=True)

    root: list[COBusiness]


class COBusinessDataList(Schema):
    data: list[COBusiness]
