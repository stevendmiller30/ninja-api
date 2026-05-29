from typing import Optional

from ninja import Field, Schema


# generic Contact schema
class BusinessContactSchema(Schema):
    first_name: str = Field(..., description="The first name of the contact")
    last_name: str = Field(..., description="The last name of the contact")
    address_line1: str = Field(..., description="contact address line 1")
    address_line2: Optional[str] = Field(None, description="contact address line 2")
    city: str = Field(..., description="contact city")
    state: str = Field(..., description="contact state")
    zip_code: str = Field(..., description="contact zip code")
    email: Optional[str] = Field(None, description="contact email")
    phone_number: Optional[str] = Field(None, description="contact phone number")


# generic Business schema for request and response
class BusinessSchema(Schema):
    business_name: str = Field(..., description="The name of the business")
    contacts: list[BusinessContactSchema] = Field(..., description="List of contacts for the business")

    class Config:
        from_attributes = True


# data wrapper for Business response
class BusinessDataResponseSchema(Schema):
    data: BusinessSchema = Field(..., description="The business data")


# classes to structure response data after creation of business and business contact
class BusinessSchemaResponse(Schema):
    id: int = Field(..., description="The unique identifier of the business")


class BusinessDataCreationResponseSchema(Schema):
    data: BusinessSchemaResponse = Field(..., description="The business data")


class BusinessListResponseSchema(Schema):
    id: int = Field(..., description="The unique identifier of the business")
    business_name: str = Field(..., description="The name of the business")
    contacts: Optional[list[BusinessContactSchema]] = Field(None, description="List of contacts for the business")


class BusinessDataListResponseSchema(Schema):
    data: list[BusinessListResponseSchema] = Field(..., description="List of businesses")
