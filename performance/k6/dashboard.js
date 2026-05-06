import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: Number(__ENV.VUS || 3),
  duration: __ENV.DURATION || "30s",
  thresholds: {
    http_req_duration: ["p(95)<800"],
    http_req_failed: ["rate<0.10"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const ADMIN_TOKEN = __ENV.ADMIN_TOKEN || "";

export default function () {
  if (!ADMIN_TOKEN) {
    return;
  }

  const response = http.get(`${BASE_URL}/dashboard/summary`, {
    headers: { Authorization: `Bearer ${ADMIN_TOKEN}` },
  });
  check(response, {
    "dashboard status is safe": (r) => [200, 401, 403, 429].includes(r.status),
  });
}
