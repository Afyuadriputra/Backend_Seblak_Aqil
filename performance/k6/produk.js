import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || "30s",
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.05"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

export default function () {
  const response = http.get(`${BASE_URL}/produk`);
  check(response, {
    "status is not 500": (r) => r.status < 500,
    "json response": (r) => String(r.headers["Content-Type"]).includes("application/json"),
  });
}
