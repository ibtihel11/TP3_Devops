from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "it works !"}


@app.get("/addition")
def add_numbers(a: int, b: int):
    return {"result a+b=": a + b, "developer": "Dev1"}