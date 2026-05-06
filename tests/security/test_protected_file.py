import pytest

from tests.conftest import assert_no_sensitive_data, seed_order_with_proof

pytestmark = pytest.mark.security


def _seed_proof(isolated_client):
    proof_path = isolated_client["private_dir"] / "payment_proofs" / "proof.png"
    with isolated_client["session_factory"]() as db:
        return seed_order_with_proof(db, proof_path)


def test_protected_payment_proof_file_should_require_token(isolated_client):
    ids = _seed_proof(isolated_client)

    response = isolated_client["client"].get(f"/admin/bukti-pembayaran/{ids['bukti_id']}/file")

    assert response.status_code == 401


def test_protected_payment_proof_file_should_reject_invalid_token(isolated_client):
    ids = _seed_proof(isolated_client)

    response = isolated_client["client"].get(
        f"/admin/bukti-pembayaran/{ids['bukti_id']}/file",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert_no_sensitive_data(response.json())


def test_protected_payment_proof_file_should_reject_inactive_admin(isolated_client):
    ids = _seed_proof(isolated_client)

    response = isolated_client["client"].get(
        f"/admin/bukti-pembayaran/{ids['bukti_id']}/file",
        headers=isolated_client["headers"]["inactive"],
    )

    assert response.status_code == 401


def test_valid_admin_should_access_protected_payment_proof_file(isolated_client):
    ids = _seed_proof(isolated_client)

    response = isolated_client["client"].get(
        f"/admin/bukti-pembayaran/{ids['bukti_id']}/file",
        headers=isolated_client["headers"]["admin"],
    )

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.content.startswith(b"\x89PNG")


def test_missing_payment_proof_metadata_should_return_404(isolated_client):
    response = isolated_client["client"].get(
        "/admin/bukti-pembayaran/999999/file",
        headers=isolated_client["headers"]["admin"],
    )

    assert response.status_code == 404
    assert_no_sensitive_data(response.json())


def test_missing_physical_payment_proof_file_should_return_404(isolated_client):
    ids = _seed_proof(isolated_client)
    for file_path in (isolated_client["private_dir"] / "payment_proofs").glob("*"):
        file_path.unlink()

    response = isolated_client["client"].get(
        f"/admin/bukti-pembayaran/{ids['bukti_id']}/file",
        headers=isolated_client["headers"]["admin"],
    )

    assert response.status_code == 404
    assert_no_sensitive_data(response.json())


def test_private_payment_proof_path_should_not_be_public_static(isolated_client):
    ids = _seed_proof(isolated_client)

    response = isolated_client["client"].get(
        f"/storage/private/payment_proofs/{ids['bukti_id']}.png",
    )

    assert response.status_code == 404
