import socket

from fastapi import FastAPI

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