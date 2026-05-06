import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: Number(__ENV.VUS || 2),
  duration: __ENV.DURATION || "20s",
  thresholds: {
    http_req_duration: ["p(95)<1000"],
    http_req_failed: ["rate<0.20"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const PRODUCT_ID = Number(__ENV.CHECKOUT_PRODUCT_ID || 1);
const PAYMENT_METHOD_ID = Number(__ENV.CHECKOUT_PAYMENT_METHOD_ID || 1);
const ENABLE_CHECKOUT = String(__ENV.ENABLE_CHECKOUT || "false").toLowerCase() === "true";

export default function () {
  if (!ENABLE_CHECKOUT) {
    return;
  }

  const response = http.post(
    `${BASE_URL}/pesanan`,
    JSON.stringify({
      nama_pelanggan: "K6 Staging",
      no_telepon: __ENV.ORDER_PHONE || "08123456789",
      alamat: "Alamat staging",
      metode_pembayaran_id: PAYMENT_METHOD_ID,
      items: [{ produk_id: PRODUCT_ID, jumlah: 1 }],
    }),
    { headers: { "Content-Type": "application/json" } },
  );
  check(response, {
    "checkout status is safe": (r) => [201, 400, 429].includes(r.status),
  });
}
