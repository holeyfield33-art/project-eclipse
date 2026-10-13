import pytest
from datetime import datetime, timezone
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
    assert client.post("/api/v1/alerts/abc/actions", json={"action": "flag"}, headers=headers).status_code == 404
    assert client.post("/api/v1/cases/abc/notes", json={"content": "note"}, headers=headers).status_code == 404
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


def test_tenant_scoped_entity_alert_and_case_reads_and_links():
    token_a = register()
    token_b = register("b@example.com")
    user_a, user_b = list(store.users.values())
    now = datetime.now(timezone.utc)
    store.entities["ea"] = {"id": "ea", "tenant_id": user_a["tenant_id"], "name": "Alice", "entity_type": "person", "risk_score": 12}
    store.alerts["aa"] = {"id": "aa", "tenant_id": user_a["tenant_id"], "entity_id": "ea", "entity_name": "Alice",
                          "risk_score": 12, "severity": "low", "status": "new", "title": "Review", "description": "Sample", "created_at": now}
    assert [e["id"] for e in client.get("/api/v1/entities/", params={"q": "Ali"}, headers=bearer(token_a)).json()] == ["ea"]
    assert client.get("/api/v1/entities/", params={"q": "Ali"}, headers=bearer(token_b)).json() == []
    assert client.get("/api/v1/entities/ea", headers=bearer(token_b)).status_code == 404
    assert client.get("/api/v1/entities/ea/network", headers=bearer(token_b)).status_code == 404
    assert client.get("/api/v1/entities/ea/transactions", headers=bearer(token_b)).status_code == 404
    assert client.get("/api/v1/alerts/aa", headers=bearer(token_b)).status_code == 404
    assert client.get("/api/v1/alerts/", headers=bearer(token_b)).json() == []
    assert client.post("/api/v1/alerts/aa/actions", json={"action": "flag"}, headers=bearer(token_b)).status_code == 404
    assert client.post("/api/v1/alerts/aa/actions", json={"action": "flag"}, headers=bearer(token_a)).status_code == 501
    assert client.post("/api/v1/cases/", json={"title": "Cross tenant", "entity_ids": ["ea"]}, headers=bearer(token_b)).status_code == 404
    created = client.post("/api/v1/cases/", json={"title": "Review", "entity_ids": ["ea"], "alert_ids": ["aa"]}, headers=bearer(token_a))
    assert created.status_code == 201, created.text
    case_id = created.json()["id"]
    assert client.get(f"/api/v1/cases/{case_id}", headers=bearer(token_b)).status_code == 404
    assert client.get("/api/v1/cases/", headers=bearer(token_b)).json() == []
    assert client.post(f"/api/v1/cases/{case_id}/notes", json={"content": "no"}, headers=bearer(token_b)).status_code == 404
    noted = client.post(f"/api/v1/cases/{case_id}/notes", json={"content": "Review completed"}, headers=bearer(token_a))
    assert noted.status_code == 200
    assert noted.json()["notes"][0]["actor_id"] == user_a["id"]
    assert audit.verify(user_a["tenant_id"])
    assert all("Review completed" not in str(e) for e in store.audit_events[user_a["tenant_id"]])


def test_case_assignment_checks_role_and_assignee_tenant():
    analyst_token = register()
    manager = next(iter(store.users.values()))
    register("b@example.com")
    other = list(store.users.values())[1]
    case_id = client.post("/api/v1/cases/", json={"title": "Review"}, headers=bearer(analyst_token)).json()["id"]
    assert client.patch(f"/api/v1/cases/{case_id}/assign", params={"assignee_id": manager["id"]}, headers=bearer(analyst_token)).status_code == 403
    manager["role"] = "manager"  # trusted server-side provisioning in this test only
    manager_token = client.post("/api/v1/auth/login", json={"email": manager["email"], "password": "correct-horse-12"}).json()["access_token"]
    assert client.patch(f"/api/v1/cases/{case_id}/assign", params={"assignee_id": other["id"]}, headers=bearer(manager_token)).status_code == 404
    assigned = client.patch(f"/api/v1/cases/{case_id}/assign", params={"assignee_id": manager["id"]}, headers=bearer(manager_token))
    assert assigned.status_code == 200
    assert assigned.json()["assigned_to"] == manager["id"]
    assert audit.verify(manager["tenant_id"])
