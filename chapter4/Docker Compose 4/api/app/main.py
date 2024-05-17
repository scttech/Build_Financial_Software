from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hellow World!"}


@app.get("/health/status")
def health_status():
    return {"status": "ok"}
