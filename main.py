import socket
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "it works !"}


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # sends nothing, just selects the internet-facing interface
        return s.getsockname()[0]
    finally:
        s.close()
        
@app.get("/greeting")
def greeting(name: str):
    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }

@app.get("/addition")
def add_numbers(a: int, b: int):
    return {"result a+b=": a + b, "developer": "Dev1"}

@app.post("/multiply")
def multiply(a: int, b: int):
    return {"result a*b=": a * b, "developer": "Dev1"}

class DivideRequest(BaseModel):
    a: float
    b: float


@app.post("/divide")
def divide(data: DivideRequest):
    if data.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed"
        )

    return {
        "result a/b=": data.a / data.b,
        "developer": "Dev2"
    }
