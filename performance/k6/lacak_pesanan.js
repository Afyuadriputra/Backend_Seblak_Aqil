import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: Number(__ENV.VUS || 5),
  duration: __ENV.DURATION || "30s",
  thresholds: {
    http_req_duration: ["p(95)<700"],
    http_req_failed: ["rate<0.10"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const ORDER_CODE = __ENV.ORDER_CODE || "ORD-STAGING-DUMMY";
const ORDER_PHONE = __ENV.ORDER_PHONE || "08123456789";

export default function () {
  const response = http.post(
    `${BASE_URL}/pesanan/lacak`,
    JSON.stringify({ kode_pesanan: ORDER_CODE, no_telepon: ORDER_PHONE }),
    { headers: { "Content-Type": "application/json" } },
  );
  check(response, {
    "status is safe": (r) => [200, 404, 429].includes(r.status),
  });
}
