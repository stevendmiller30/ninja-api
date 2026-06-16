import pytest
from pydantic import ValidationError

from src.business.schemas.business_schemas import (
    BusinessContactSchema,
    BusinessDataCreationResponseSchema,
    BusinessDataListResponseSchema,
    BusinessDataResponseSchema,
    BusinessListResponseSchema,
    BusinessSchema,
    BusinessSchemaResponse,
)

# --- Mock Data Fixtures ---


@pytest.fixture
def valid_contact_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "address_line1": "123 Main St",
        "address_line2": "Suite 100",
        "city": "Gotham",
        "state": "NY",
        "zip_code": "10001",
        "email": "john.doe@example.com",
        "phone_number": "555-0199",
    }


@pytest.fixture
def valid_business_data(valid_contact_data):
    return {
        "business_name": "Wayne Enterprises",
        "contacts": [valid_contact_data],
    }


# --- Tests for BusinessContactSchema ---


def test_business_contact_schema_valid(valid_contact_data):
    """Test that a valid contact payload passes validation."""
    contact = BusinessContactSchema(**valid_contact_data)
    assert contact.first_name == "John"
    assert contact.email == "john.doe@example.com"


def test_business_contact_schema_optional_fields(valid_contact_data):
    """Test that optional fields default to None if omitted."""
    del valid_contact_data["address_line2"]
    del valid_contact_data["email"]
    del valid_contact_data["phone_number"]

    contact = BusinessContactSchema(**valid_contact_data)
    assert contact.address_line2 is None
    assert contact.email is None
    assert contact.phone_number is None


@pytest.mark.parametrize("missing_field", ["first_name", "last_name", "address_line1", "city", "state", "zip_code"])
def test_business_contact_schema_missing_required(valid_contact_data, missing_field):
    """Test that missing required fields raise a ValidationError."""
    del valid_contact_data[missing_field]
    with pytest.raises(ValidationError) as exc_info:
        BusinessContactSchema(**valid_contact_data)

    assert missing_field in str(exc_info.value)


# --- Tests for BusinessSchema & BusinessDataResponseSchema ---


def test_business_schema_valid(valid_business_data):
    """Test the core BusinessSchema with valid nested contacts."""
    business = BusinessSchema(**valid_business_data)
    assert business.business_name == "Wayne Enterprises"
    assert len(business.contacts) == 1
    assert business.contacts[0].first_name == "John"


def test_business_data_response_schema(valid_business_data):
    """Test the data wrapper envelope for a single business response."""
    payload = {"data": valid_business_data}
    response = BusinessDataResponseSchema(**payload)
    assert response.data.business_name == "Wayne Enterprises"


# --- Tests for Creation Responses ---


def test_business_schema_response_valid():
    """Test the basic ID tracking schema."""
    obj = BusinessSchemaResponse(id=42)
    assert obj.id == 42


def test_business_data_creation_response_schema():
    """Test the data wrapper envelope for a creation response."""
    payload = {"data": {"id": 101}}
    response = BusinessDataCreationResponseSchema(**payload)
    assert response.data.id == 101


# --- Tests for List Responses ---


def test_business_list_response_schema_with_contacts(valid_contact_data):
    """Test list item schema including contacts."""
    payload = {"id": 1, "business_name": "Acme Corp", "contacts": [valid_contact_data]}
    obj = BusinessListResponseSchema(**payload)
    assert obj.id == 1
    assert len(obj.contacts) == 1


def test_business_list_response_schema_without_contacts():
    """Test list item schema where contacts are omitted/None."""
    payload = {"id": 2, "business_name": "Stark Industries", "contacts": None}
    obj = BusinessListResponseSchema(**payload)
    assert obj.contacts is None


def test_business_data_list_response_schema(valid_contact_data):
    """Test the wrapper schema for returning a list of businesses."""
    payload = {
        "data": [
            {"id": 1, "business_name": "Company A", "contacts": [valid_contact_data]},
            {"id": 2, "business_name": "Company B", "contacts": None},
        ]
    }
    response = BusinessDataListResponseSchema(**payload)
    assert len(response.data) == 2
    assert response.data[0].business_name == "Company A"
    assert response.data[1].contacts is None


# --- Test ORM / Attribute Loading (`from_attributes = True`) ---


def test_business_schema_from_attributes():
    """Test that the schema can load data from an object-like structure (mocking Django ORM)."""

    class MockContact:
        first_name = "Bruce"
        last_name = "Wayne"
        address_line1 = "100 Mountain Drive"
        address_line2 = None
        city = "Gotham"
        state = "NJ"
        zip_code = "07001"
        email = "bruce@wayne.com"
        phone_number = None

    class MockBusiness:
        business_name = "Wayne Enterprises"
        contacts = [MockContact()]

    # Because class Config: from_attributes = True is set, model_validate works on ORM objects
    business_schema = BusinessSchema.model_validate(MockBusiness())
    assert business_schema.business_name == "Wayne Enterprises"
    assert business_schema.contacts[0].first_name == "Bruce"
