import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import audit, rate_limit, store
from app.core.security import create_access_token
from app.core.config import settings


@pytest.fixture(autouse=True)
def clean_state():
    store.reset_for_tests()
    rate_limit.reset_for_tests()
    yield
    store.reset_for_tests()


client = TestClient(app)


def register(email="a@example.com"):
    response = client.post("/api/v1/auth/register", json={"email": email, "password": "correct-horse-12", "full_name": "Test User"})
    assert response.status_code == 201, response.text
    return response.json()["access_token"]


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_registration_cannot_assign_role_or_tenant():
    response = client.post("/api/v1/auth/register", json={"email": "x@example.com", "password": "correct-horse-12", "full_name": "X", "role": "admin"})
    assert response.status_code == 422
    token = register()
    user = next(iter(store.users.values()))
    assert user["role"] == "analyst"
    assert user["tenant_id"] != ""
    assert "password_hash" in user and user["password_hash"] != "correct-horse-12"
    assert client.get("/api/v1/entities/", params={"q": "ab"}, headers=bearer(token)).status_code == 200


def test_authentication_and_stale_claims_fail_closed():
    assert client.get("/api/v1/alerts/").status_code == 401
    token = register()
    assert client.get("/api/v1/alerts/", headers=bearer(token)).status_code == 200
    assert client.get("/api/v1/alerts/", headers=bearer(token + "x")).status_code == 401
    user = next(iter(store.users.values()))
    forged = create_access_token(user["id"], tenant_id="other", role="admin")
    assert client.get("/api/v1/alerts/", headers=bearer(forged)).status_code == 401
    user["active"] = False
    assert client.get("/api/v1/alerts/", headers=bearer(token)).status_code == 401


def test_login_and_duplicate_account():
    register()
    assert client.post("/api/v1/auth/login", json={"email": "a@example.com", "password": "wrong"}).status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "a@example.com", "password": "correct-horse-12"}).status_code == 200
    assert client.post("/api/v1/auth/register", json={"email": "a@example.com", "password": "correct-horse-12", "full_name": "X"}).status_code == 409


def test_scaffold_writes_do_not_claim_success():
    token = register()
    headers = bearer(token)
    assert client.post("/api/v1/alerts/abc/actions", json={"action": "freeze"}, headers=headers).status_code == 403
    assert client.post("/api/v1/alerts/abc/actions", json={"action": "flag"}, headers=headers).status_code == 501
    assert client.post("/api/v1/cases/abc/notes", json={"content": "note"}, headers=headers).status_code == 501
    assert client.patch("/api/v1/cases/abc/assign", params={"assignee_id": "u"}, headers=headers).status_code == 403
    assert client.get("/api/v1/reports/generate/sar", headers=headers).status_code == 501


def test_audit_chain_detects_tampering_and_separates_tenants():
    register()
    register("b@example.com")
    first, second = list(store.users.values())
    assert audit.verify(first["tenant_id"])
    assert audit.verify(second["tenant_id"])
    assert len(store.audit_events[first["tenant_id"]]) == 1
    store.audit_events[first["tenant_id"]][0]["action"] = "forged"
    assert not audit.verify(first["tenant_id"])
    assert audit.verify(second["tenant_id"])


def test_login_rate_limit():
    for _ in range(10):
        assert client.post("/api/v1/auth/login", json={"email": "absent@example.com", "password": "wrong"}).status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "absent@example.com", "password": "wrong"}).status_code == 429


def test_production_cannot_start_on_memory_store(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    with pytest.raises(RuntimeError, match="durable tenant and audit storage"):
        with TestClient(app):
            pass


def test_protected_reports_and_cases_reject_anonymous_requests():
    assert client.get("/api/v1/reports/templates").status_code == 401
    assert client.get("/api/v1/cases/").status_code == 401
    assert client.post("/api/v1/cases/", json={"title": "X"}).status_code == 401
