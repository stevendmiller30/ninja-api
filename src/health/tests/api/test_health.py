import json

from django.test import TestCase
from django.urls import reverse

TWO_HUNDRED_OK = 200


class TestApiHealthCheck(TestCase):
    def test_health_check(self):
        # ARRANGE
        url = reverse("api-1.0.0:health-check")

        # ACT
        response = self.client.get(url)
        resp_data = json.loads(response.content.decode("utf-8"))

        # ASSERT
        assert response.status_code == TWO_HUNDRED_OK
        self.assertEqual(resp_data["status"], "ok")
