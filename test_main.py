"""Unit tests for the FastAPI application defined in main.py."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items(monkeypatch):
    """Give every test a fresh copy of the in-memory items."""
    monkeypatch.setattr(
        main, "ITEMS", {1: {"name": "Item 1"}, 2: {"name": "Item 2"}}
    )


# ---------- /subtract ----------

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
    """/subtract returns a - b for valid integers."""
    response = client.get("/subtract", params={"a": a, "b": b})

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
    """/subtract returns 422 for missing or invalid parameters."""
    response = client.get("/subtract", params=params)

    assert response.status_code == 422


# ---------- / ----------

def test_read_root():
    """The root endpoint returns the welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works !"}


# ---------- get_ip and /greeting ----------

def test_get_ip():
    """get_ip returns the address chosen by the socket (mocked)."""
    fake_socket = MagicMock()
    fake_socket.getsockname.return_value = ("192.168.1.10", 12345)
    with patch("main.socket.socket", return_value=fake_socket):
        assert main.get_ip() == "192.168.1.10"
    fake_socket.connect.assert_called_once_with(("8.8.8.8", 80))
    fake_socket.close.assert_called_once()


def test_greeting():
    """/greeting returns the name, the developer and the (mocked) IP."""
    with patch("main.get_ip", return_value="1.2.3.4"):
        response = client.get("/greeting", params={"name": "Ibtihel"})
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Hello, Ibtihel"
    assert data["IP"] == "1.2.3.4"
    assert data["developer"] == "Dev2"
    assert "hostname" in data


# ---------- /addition and /multiply ----------

def test_addition():
    """/addition returns a + b."""
    response = client.get("/addition", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result a+b="] == 5


def test_multiply():
    """/multiply returns a * b."""
    response = client.post("/multiply", params={"a": 4, "b": 3})
    assert response.status_code == 200
    assert response.json()["result a*b="] == 12


# ---------- /divide ----------

def test_divide_valid():
    """/divide returns a / b when b is not zero."""
    response = client.post("/divide", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json()["result a/b="] == 2.5


def test_divide_by_zero():
    """/divide returns 400 when b is zero."""
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Division by zero is not allowed"


# ---------- /update/{item_id} ----------

def test_update_item_success():
    """/update renames an existing item."""
    response = client.put("/update/1", json={"name": "Renamed"})
    assert response.status_code == 200
    assert response.json()["item"] == {"name": "Renamed"}


def test_update_item_not_found():
    """/update returns 404 for an unknown item."""
    response = client.put("/update/99", json={"name": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


# ---------- /remove/{item_id} ----------

def test_remove_item_success():
    """/remove deletes an existing item."""
    response = client.delete("/remove/1")
    assert response.status_code == 200
    assert response.json()["item"] == {"name": "Item 1"}
    assert 1 not in main.ITEMS


def test_remove_item_not_found():
    """/remove returns 404 for an unknown item."""
    response = client.delete("/remove/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
