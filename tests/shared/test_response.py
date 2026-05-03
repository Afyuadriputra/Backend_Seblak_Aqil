from app.shared.response import error_response, success_response


def test_success_response_without_meta():
    response = success_response(
        message="Data berhasil diambil",
        data={"id": 1},
    )

    assert response["success"] is True
    assert response["message"] == "Data berhasil diambil"
    assert response["data"] == {"id": 1}
    assert "meta" not in response


def test_success_response_with_meta():
    response = success_response(
        message="Data berhasil diambil",
        data=[],
        meta={"page": 1, "limit": 10},
    )

    assert response["success"] is True
    assert response["message"] == "Data berhasil diambil"
    assert response["data"] == []
    assert response["meta"] == {"page": 1, "limit": 10}


def test_error_response_without_errors():
    response = error_response(message="Terjadi kesalahan")

    assert response["success"] is False
    assert response["message"] == "Terjadi kesalahan"
    assert response["errors"] is None


def test_error_response_with_errors():
    response = error_response(
        message="Input tidak valid",
        errors={"nama_produk": "Wajib diisi"},
    )

    assert response["success"] is False
    assert response["message"] == "Input tidak valid"
    assert response["errors"] == {"nama_produk": "Wajib diisi"}
