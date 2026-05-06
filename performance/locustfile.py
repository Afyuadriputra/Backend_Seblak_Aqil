import os

from locust import HttpUser, between, task


class PublicAndAdminApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.order_code = os.getenv("ORDER_CODE", "ORD-STAGING-DUMMY")
        self.phone = os.getenv("ORDER_PHONE", "08123456789")
        self.admin_token = os.getenv("ADMIN_TOKEN")
        self.checkout_product_id = int(os.getenv("CHECKOUT_PRODUCT_ID", "1"))
        self.checkout_payment_method_id = int(os.getenv("CHECKOUT_PAYMENT_METHOD_ID", "1"))
        self.enable_checkout = os.getenv("ENABLE_CHECKOUT", "false").lower() == "true"

    @task(5)
    def browse_products(self):
        self.client.get("/produk", name="GET /produk")

    @task(3)
    def browse_categories(self):
        self.client.get("/kategori", name="GET /kategori")

    @task(3)
    def browse_active_payment_methods(self):
        self.client.get("/metode-pembayaran/aktif", name="GET /metode-pembayaran/aktif")

    @task(2)
    def track_order(self):
        self.client.post(
            "/pesanan/lacak",
            json={"kode_pesanan": self.order_code, "no_telepon": self.phone},
            name="POST /pesanan/lacak",
        )

    @task(1)
    def checkout_staging_order(self):
        if not self.enable_checkout:
            return
        self.client.post(
            "/pesanan",
            json={
                "nama_pelanggan": "Load Test",
                "no_telepon": self.phone,
                "alamat": "Alamat staging",
                "metode_pembayaran_id": self.checkout_payment_method_id,
                "items": [{"produk_id": self.checkout_product_id, "jumlah": 1}],
            },
            name="POST /pesanan",
        )

    @task(1)
    def admin_dashboard_summary(self):
        if not self.admin_token:
            return
        self.client.get(
            "/dashboard/summary",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            name="GET /dashboard/summary",
        )


# Run:
# locust -f performance/locustfile.py --host=http://localhost:8000
