import pytest

from app.core.dependencies import require_any_role, require_role
from app.modules.admin.model import Admin
from app.shared.exceptions import ForbiddenException

pytestmark = pytest.mark.security


def _admin(role: str, is_active: bool = True) -> Admin:
    return Admin(
        id=1,
        nama_admin=f"Admin {role}",
        email=f"{role}@example.com",
        kata_sandi="hashed",
        role=role,
        is_active=is_active,
    )


def test_superadmin_should_access_superadmin_only_endpoint(isolated_client):
    response = isolated_client["client"].get(
        "/audit-log",
        headers=isolated_client["headers"]["superadmin"],
    )

    assert response.status_code == 200


@pytest.mark.parametrize("role", ["admin", "staff"])
def test_non_superadmin_should_be_rejected_from_superadmin_only_endpoint(isolated_client, role):
    response = isolated_client["client"].get(
        "/audit-log",
        headers=isolated_client["headers"][role],
    )

    assert response.status_code == 403


def test_public_should_not_access_audit_log(isolated_client):
    response = isolated_client["client"].get("/audit-log")

    assert response.status_code == 401


def test_require_role_should_accept_matching_role():
    dependency = require_role("superadmin")

    assert dependency(_admin("superadmin")).role == "superadmin"


def test_require_role_should_reject_wrong_role():
    dependency = require_role("superadmin")

    with pytest.raises(ForbiddenException):
        dependency(_admin("admin"))


@pytest.mark.parametrize("role", ["superadmin", "admin"])
def test_require_any_role_should_accept_allowed_roles(role):
    dependency = require_any_role(["superadmin", "admin"])

    assert dependency(_admin(role)).role == role


def test_require_any_role_should_reject_staff():
    dependency = require_any_role(["superadmin", "admin"])

    with pytest.raises(ForbiddenException):
        dependency(_admin("staff"))


def test_inactive_admin_should_be_rejected_even_when_role_matches(isolated_client):
    response = isolated_client["client"].get(
        "/auth/me",
        headers=isolated_client["headers"]["inactive"],
    )

    assert response.status_code == 401


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_audit_log_should_be_read_only(method, isolated_client):
    response = isolated_client["client"].request(
        method.upper(),
        "/audit-log",
        headers=isolated_client["headers"]["superadmin"],
        json={"aksi": "ubah"},
    )

    assert response.status_code in {405, 404}
