from datetime import date
from typing import Annotated, Optional

from ninja import Field, FilterLookup, FilterSchema, Schema
from pydantic import ConfigDict, RootModel, model_validator


class Person(Schema):
    model_config = ConfigDict(populate_by_name=True)

    first_name: Optional[str] = Field(None, alias="firstname")
    last_name: Optional[str] = Field(None, alias="lastname")
    birth_date: Optional[date] = Field(None, alias="birthday")


class USSenator(Schema):
    model_config = ConfigDict(populate_by_name=True)

    description: Optional[str] = Field(None)
    term_end_date: Optional[date] = Field(None, alias="enddate")
    website: Optional[str] = Field(None)
    state: Optional[str] = Field(None)
    person: Optional[Person] = Field(None)
    political_party: Optional[str] = Field(None, alias="party")
    phone_number: Optional[str] = Field(None, alias="phone")


class USSenatorList(RootModel):
    model_config = ConfigDict(populate_by_name=True)

    root: list[USSenator]


class USSenatorDataList(Schema):
    data: list[USSenator]


class SenatorFilterSchema(FilterSchema):
    state: Annotated[Optional[str], FilterLookup("state__iexact")] = None
    first_name: Annotated[Optional[str], FilterLookup("first_name__icontains")] = None
    last_name: Annotated[Optional[str], FilterLookup("last_name__icontains")] = None

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_filter(cls, data):

        if isinstance(data, dict):
            # Check if any of our expected fields have a non-empty value
            allowed_fields = {"state", "first_name", "last_name"}

            # Extract values that are present and not empty strings/None
            has_value = any(data.get(field) for field in allowed_fields if data.get(field) is not None)

            if not has_value:
                raise ValueError("At least one search filter ('state', 'first_name', or 'last_name') must be provided.")

        return data
