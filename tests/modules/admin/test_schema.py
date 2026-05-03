import pytest
from pydantic import ValidationError

from app.modules.admin.schema import AdminCreate, AdminPasswordUpdate, AdminUpdate


def test_admin_create_valid():
    schema = AdminCreate(
        nama_admin="Admin Seblak",
        email="admin@example.com",
        kata_sandi="password123",
    )

    assert schema.nama_admin == "Admin Seblak"
    assert schema.email == "admin@example.com"


def test_admin_create_rejects_short_password():
    with pytest.raises(ValidationError):
        AdminCreate(
            nama_admin="Admin Seblak",
            email="admin@example.com",
            kata_sandi="short",
        )


def test_admin_update_allows_partial_payload():
    schema = AdminUpdate(nama_admin="Admin Baru")

    assert schema.nama_admin == "Admin Baru"
    assert schema.email is None


def test_admin_password_update_requires_new_password_min_length():
    with pytest.raises(ValidationError):
        AdminPasswordUpdate(kata_sandi_lama="old", kata_sandi_baru="short")
