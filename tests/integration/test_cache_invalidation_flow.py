import pytest

from app.modules.kategori.schema import KategoriCreate, KategoriUpdate
from app.modules.kategori.service import create_kategori, update_kategori
from app.modules.metode_pembayaran.schema import (
    MetodePembayaranCreate,
    MetodePembayaranStatusUpdate,
)
from app.modules.metode_pembayaran.service import create_metode, update_status
from app.modules.produk.schema import ProdukCreate, ProdukStokUpdate, ProdukUpdate
from app.modules.produk.service import create_produk, update_produk, update_produk_stok
from tests.conftest import seed_catalog

pytestmark = pytest.mark.integration


def test_public_product_list_should_use_cache_hit(isolated_client, monkeypatch):
    cached = {
        "data": [{"id": 1, "nama_produk": "Cached Seblak"}],
        "meta": {"page": 1, "limit": 20, "total": 1, "total_pages": 1},
    }
    monkeypatch.setattr("app.modules.produk.controller.get_json_cache", lambda key: cached)

    response = isolated_client["client"].get("/produk")

    assert response.status_code == 200
    assert response.json()["data"][0]["nama_produk"] == "Cached Seblak"


def test_public_product_list_should_set_cache_on_miss(isolated_client, monkeypatch):
    calls = []
    with isolated_client["session_factory"]() as db:
        seed_catalog(db)
    monkeypatch.setattr("app.modules.produk.controller.get_json_cache", lambda key: None)
    monkeypatch.setattr(
        "app.modules.produk.controller.set_json_cache",
        lambda key, value, ttl: calls.append((key, value, ttl)),
    )

    response = isolated_client["client"].get("/produk")

    assert response.status_code == 200
    assert calls
    assert calls[0][0].startswith("produk:public:")


def test_product_cache_should_be_invalidated_on_create_update_and_stock_change(
    isolated_client,
    monkeypatch,
):
    deleted = []
    monkeypatch.setattr("app.modules.produk.service.delete_pattern", deleted.append)

    with isolated_client["session_factory"]() as db:
        kategori = create_kategori(db, KategoriCreate(nama_kategori="Seblak", deskripsi=None))
        produk = create_produk(
            db,
            ProdukCreate(
                kategori_id=kategori.id,
                nama_produk="Seblak Original",
                deskripsi=None,
                harga="15000.00",
                stok=10,
            ),
        )
        update_produk(db, produk.id, ProdukUpdate(nama_produk="Seblak Updated"))
        update_produk_stok(db, produk.id, ProdukStokUpdate(stok=8))

    assert deleted.count("produk:public:*") >= 3
    assert "dashboard:*" in deleted


def test_category_update_should_invalidate_category_and_product_cache(
    isolated_client,
    monkeypatch,
):
    deleted = []
    monkeypatch.setattr("app.modules.kategori.service.delete_pattern", deleted.append)

    with isolated_client["session_factory"]() as db:
        kategori = create_kategori(db, KategoriCreate(nama_kategori="Seblak", deskripsi=None))
        update_kategori(db, kategori.id, KategoriUpdate(nama_kategori="Seblak Baru"))

    assert "kategori:*" in deleted
    assert "produk:public:*" in deleted


def test_payment_method_update_should_invalidate_payment_method_cache(
    isolated_client,
    monkeypatch,
):
    deleted = []
    monkeypatch.setattr("app.modules.metode_pembayaran.service.delete_pattern", deleted.append)

    with isolated_client["session_factory"]() as db:
        metode = create_metode(
            db,
            MetodePembayaranCreate(
                nama_metode="Transfer BCA",
                tipe_metode="transfer_bank",
                nama_bank="BCA",
                nomor_rekening="1234567890",
                nama_pemilik_rekening="Seblak Rika",
            ),
        )
        update_status(db, metode.id, MetodePembayaranStatusUpdate(status_aktif=False))

    assert deleted.count("metode-pembayaran:*") >= 2
