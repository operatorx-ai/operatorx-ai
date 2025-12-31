from fastapi import FastAPI

app = FastAPI(title="OperatorX AI Backend")


@app.get("/")
def root():
    return {"message": "OperatorX AI backend is running"}
