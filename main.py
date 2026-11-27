"""Small FastAPI application used for the CI/CD practical work (TP3)."""

import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

ITEMS = {
    1: {"name": "Item 1"},
    2: {"name": "Item 2"},
}


class DivideRequest(BaseModel):
    """Body of the /divide request."""

    a: float
    b: float


class UpdateRequest(BaseModel):
    """Body of the /update/{item_id} request."""

    name: str


def get_ip():
    """Return the IP address of the interface connected to the internet."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # UDP connect sends nothing, it only selects the outgoing interface.
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    finally:
        sock.close()


@app.get("/")
def read_root():
    """Return a simple message to check that the API is running."""
    return {"message": "it works !"}


@app.get("/greeting")
def greeting(name: str):
    """Greet the given name and return information about the host."""
    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }


@app.get("/addition")
def add_numbers(a: int, b: int):
    """Return the sum of a and b."""
    return {"result a+b=": a + b, "developer": "Dev1"}


@app.get("/subtract")
def subtract(a: int, b: int):
    """Return the difference a - b."""
    return {"result": a - b}


@app.post("/multiply")
def multiply(a: int, b: int):
    """Return the product of a and b."""
    return {"result a*b=": a * b, "developer": "Dev1"}


@app.post("/divide")
def divide(data: DivideRequest):
    """Return a / b, or an HTTP 400 error if b is zero."""
    if data.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed",
        )

    return {
        "result a/b=": data.a / data.b,
        "developer": "Dev2",
    }


@app.put("/update/{item_id}")
def update_item(item_id: int, data: UpdateRequest):
    """Rename an item, or return an HTTP 404 error if it does not exist."""
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")

    ITEMS[item_id]["name"] = data.name

    return {
        "message": "Item updated successfully",
        "id": item_id,
        "item": ITEMS[item_id],
        "developer": "Dev2",
    }


@app.delete("/remove/{item_id}")
def remove_item(item_id: int):
    """Delete an item, or return an HTTP 404 error if it does not exist."""
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")

    removed = ITEMS.pop(item_id)

    return {
        "message": "Item deleted successfully",
        "id": item_id,
        "item": removed,
        "developer": "Dev1",
    }
