from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="CI/CD API Testing Demo",
    description="A small FastAPI service for CI/CD, API automation, and DeepSeek-assisted test generation.",
    version="0.1.0",
)


class Operation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class CalculateRequest(BaseModel):
    left: float = Field(..., description="The left operand.")
    right: float = Field(..., description="The right operand.")
    operation: Operation = Field(..., description="The calculation operation.")


class CalculateResponse(BaseModel):
    result: float


class TextSummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize.")
    max_length: int = Field(80, ge=10, le=300, description="Maximum summary length.")


class TextSummaryResponse(BaseModel):
    summary: str
    original_length: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/calculate", response_model=CalculateResponse)
def calculate(payload: CalculateRequest) -> CalculateResponse:
    if payload.operation == Operation.add:
        result = payload.left + payload.right
    elif payload.operation == Operation.subtract:
        result = payload.left - payload.right
    elif payload.operation == Operation.multiply:
        result = payload.left * payload.right
    else:
        if payload.right == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = payload.left / payload.right

    return CalculateResponse(result=result)


@app.post("/api/summarize", response_model=TextSummaryResponse)
def summarize_text(payload: TextSummaryRequest) -> TextSummaryResponse:
    summary = payload.text.strip()
    if len(summary) > payload.max_length:
        summary = summary[: payload.max_length].rstrip() + "..."

    return TextSummaryResponse(summary=summary, original_length=len(payload.text))
