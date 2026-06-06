import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"left": 2, "right": 3, "operation": "add"}, 5),
        ({"left": 7, "right": 4, "operation": "subtract"}, 3),
        ({"left": 6, "right": 5, "operation": "multiply"}, 30),
        ({"left": 9, "right": 3, "operation": "divide"}, 3),
    ],
)
def test_calculate_supported_operations(payload, expected):
    response = client.post("/api/calculate", json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": expected}


def test_calculate_rejects_missing_required_field():
    response = client.post(
        "/api/calculate",
        json={"left": 1, "operation": "add"},
    )

    assert response.status_code == 422


def test_calculate_rejects_unknown_operation():
    response = client.post(
        "/api/calculate",
        json={"left": 1, "right": 2, "operation": "mod"},
    )

    assert response.status_code == 422


def test_calculate_rejects_division_by_zero():
    response = client.post(
        "/api/calculate",
        json={"left": 1, "right": 0, "operation": "divide"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Division by zero is not allowed."}


def test_summarize_returns_original_text_when_short_enough():
    response = client.post(
        "/api/summarize",
        json={"text": "FastAPI makes API testing straightforward.", "max_length": 80},
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "FastAPI makes API testing straightforward.",
        "original_length": 42,
    }


def test_summarize_truncates_long_text():
    response = client.post(
        "/api/summarize",
        json={"text": "abcdefghijklmnopqrstuvwxyz", "max_length": 10},
    )

    assert response.status_code == 200
    assert response.json() == {"summary": "abcdefghij...", "original_length": 26}


def test_summarize_rejects_empty_text():
    response = client.post(
        "/api/summarize",
        json={"text": "", "max_length": 80},
    )

    assert response.status_code == 422


def test_reverse_returns_reversed_text():
    response = client.post("/api/reverse", json={"text": "cicd"})

    assert response.status_code == 200
    assert response.json() == {"reversed_text": "dcic"}


def test_reverse_rejects_empty_text():
    response = client.post("/api/reverse", json={"text": ""})

    assert response.status_code == 422


def test_palindrome_accepts_phrase_ignoring_case_and_spaces():
    response = client.post("/api/palindrome", json={"text": "Never odd or even"})

    assert response.status_code == 200
    assert response.json() == {
        "is_palindrome": True,
        "normalized_text": "neveroddoreven",
    }


def test_palindrome_returns_false_for_non_palindrome():
    response = client.post("/api/palindrome", json={"text": "continuous delivery"})

    assert response.status_code == 200
    assert response.json() == {
        "is_palindrome": False,
        "normalized_text": "continuousdelivery",
    }


def test_palindrome_rejects_empty_text():
    response = client.post("/api/palindrome", json={"text": ""})

    assert response.status_code == 422
