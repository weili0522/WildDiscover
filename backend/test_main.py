from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_valid_prediction():
    response = client.get(
        "/api/v1/predict/pilot-bird",
        params={"latitude": -23, "longitude": 133}
    )
    assert response.status_code == 200
    assert response.json()["type"] == "FeatureCollection"


def test_species_not_found():
    response = client.get("/api/v1/predict/abc")
    assert response.status_code == 404
    assert response.json()["detail"] == "Species not found"


def test_latitude_outside_australia():
    response = client.get(
        "/api/v1/predict/pilot-bird",
        params={"latitude": 0, "longitude": 133}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == \
        "Latitude is outside the supported Australian bounds"


def test_longitude_outside_australia():
    response = client.get(
        "/api/v1/predict/pilot-bird",
        params={"latitude": -23, "longitude": 100}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == \
        "Longitude is outside the supported Australian bounds"