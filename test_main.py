import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 4, 6),       # Positive result
        (4, 10, -6),      # Negative result
        (10, 0, 10),      # Subtract zero
        (10, 10, 0),      # Equal numbers
        (0, 0, 0),        # Both numbers are zero
        (-5, -3, -2),     # Both numbers are negative
        (-5, 3, -8),      # Negative minus positive
        (5, -3, 8),       # Positive minus negative
    ]
)
def test_subtract_valid_cases(a, b, expected):
    response = client.get(
        "/subtract",
        params={"a": a, "b": b}
    )

    assert response.status_code == 200
    assert response.json() == {"result": expected}


@pytest.mark.parametrize(
    "params",
    [
        {"a": 10},                 # Missing b
        {"b": 4},                  # Missing a
        {},                        # Both parameters missing
        {"a": "abc", "b": 4},      # Invalid a
        {"a": 10, "b": "xyz"},     # Invalid b
    ]
)
def test_subtract_invalid_cases(params):
    response = client.get("/subtract", params=params)

    assert response.status_code == 422
