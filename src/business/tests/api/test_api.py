from unittest.mock import patch

from django.test import TestCase

from src.business.api import create_business, get_business, health_check, list_businesses
from src.business.schemas.business_schemas import BusinessDataCreationResponseSchema, BusinessSchema


class TestBusinessApi(TestCase):
    def test_health_check_returns_ok(self):
        result = health_check(None)

        assert result == {"status": "ok"}

    @patch("src.business.api.get_businesses")
    def test_list_businesses_returns_service_payload(self, mock_get_businesses):
        expected = {"data": []}
        mock_get_businesses.return_value = expected

        response = list_businesses(None)

        assert response == expected
        mock_get_businesses.assert_called_once()

    @patch("src.business.api.save_business")
    def test_create_business_calls_save_business(self, mock_save_business):
        expected = BusinessDataCreationResponseSchema(data={"id": 1})
        mock_save_business.return_value = expected

        payload = BusinessSchema(
            business_name="Acme Corp",
            contacts=[
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "address_line1": "1 Main Street",
                    "city": "Gotham",
                    "state": "NY",
                    "zip_code": "10001",
                }
            ],
        )

        response = create_business(None, payload=payload)

        mock_save_business.assert_called_once_with(payload)
        assert response == expected

    @patch("src.business.api.get_business_by_id")
    def test_get_business_returns_service_payload(self, mock_get_business_by_id):
        expected = {"data": {"business_name": "Acme Corp"}}
        mock_get_business_by_id.return_value = expected

        response = get_business(None, business_id=42)

        assert response == expected
        mock_get_business_by_id.assert_called_once_with(42)
