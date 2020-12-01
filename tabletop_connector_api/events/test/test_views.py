import pytest
from rest_framework.test import APIClient


# @pytest.mark.django_db
# def test_CustomEventViewSetFound():
#     client = APIClient()
#     response = client.get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk')
#
#     assert response.status_code == 302


@pytest.mark.django_db
def test_CustomEventViewSetNotFound():
    client = APIClient()
    response = client.get('api/geteventbydistance/?distance=0&country=Poland&city=Gdansk')

    assert response.status_code == 404

