import pytest
from pydantic import ValidationError
from app.schemas.schemas import SubmissionIn, UserCreate
from app.services.rate_limit import Limiter


def test_submission_valid_data():
    assert SubmissionIn(data={"name": "Ali"}).data["name"] == "Ali"


def test_submission_too_many_fields():
    with pytest.raises(ValidationError):
        SubmissionIn(data={f"field{i}": i for i in range(21)})


def test_submission_requires_object():
    with pytest.raises(ValidationError):
        SubmissionIn(data="invalid")


def test_password_minimum_length():
    with pytest.raises(ValidationError):
        UserCreate(email="ali@example.com", password="short")


def test_limiter_allows_requests():
    limiter = Limiter(limit=2, window=60)
    assert limiter.allow("client-1")
    assert limiter.allow("client-1")


def test_limiter_blocks_excess_requests():
    limiter = Limiter(limit=2, window=60)
    limiter.allow("client-1")
    limiter.allow("client-1")
    assert not limiter.allow("client-1")


def test_limiter_separates_clients():
    limiter = Limiter(limit=1, window=60)
    assert limiter.allow("client-1")
    assert limiter.allow("client-2")
