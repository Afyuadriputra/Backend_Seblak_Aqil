(function () {
  const script = document.currentScript;
  const page = script?.dataset.page || detectPage();
  const base = script?.dataset.base || "..";
  const apiBase = localStorage.getItem("SEBLAK_API_BASE") || "http://127.0.0.1:8000";

  const routes = {
    login: `${base}/login_seblak_rika/code.html`,
    dashboard: `${base}/dashboard_seblak_rika/code.html`,
    kategori: `${base}/kategori_seblak_rika/code.html`,
    produk: `${base}/kelola_produk_seblak_rika/code.html`,
    metode: `${base}/metode_pembayaran_seblak_rika/code.html`,
    pesanan: `${base}/pesanan_seblak_rika/code.html`,
    riwayat: `${base}/riwayat_stok_seblak_rika/code.html`,
    audit: `${base}/audit_log_seblak_rika/code.html`,
  };

  const navItems = [
    ["dashboard", "Dashboard", "dashboard"],
    ["kategori", "Kategori", "category"],
    ["produk", "Produk", "inventory_2"],
    ["metode", "Metode Pembayaran", "payments"],
    ["pesanan", "Pesanan", "shopping_cart"],
    ["riwayat", "Riwayat Stok", "history"],
    ["audit", "Audit Log", "assignment"],
  ];

  const contracts = {
    dashboard: { endpoint: "GET /dashboard/summary", fields: ["total_produk", "total_pelanggan", "total_pesanan", "total_omzet"] },
    kategori: { endpoint: "GET /kategori", fields: ["id", "nama_kategori", "deskripsi", "dibuat_pada"] },
    produk: { endpoint: "GET /produk/admin/semua", fields: ["id", "nama_produk", "nama_kategori", "harga", "stok", "status_tersedia"] },
    metode: { endpoint: "GET /metode-pembayaran", fields: ["nama_metode", "tipe_metode", "nomor_rekening", "gambar_qr", "status_aktif"] },
    pesanan: { endpoint: "GET /pesanan", fields: ["kode_pesanan", "nama_pelanggan", "status_pembayaran", "status_pesanan", "total_harga"] },
    riwayat: { endpoint: "GET /riwayat-stok", fields: ["produk_id", "jenis_perubahan", "stok_sebelum", "jumlah_perubahan", "stok_sesudah"] },
    audit: { endpoint: "GET /audit-log", fields: ["admin_id", "aksi", "entity", "entity_id", "deskripsi"] },
  };

  const mock = {
    dashboardSummary: {
      total_produk: 12,
      total_pelanggan: 30,
      total_pesanan: 45,
      pesanan_selesai: 20,
      pembayaran_menunggu_verifikasi: 5,
      produk_stok_rendah: 3,
      total_omzet: "350000.00",
      tanggal_dari: "2026-05-01T00:00:00",
      tanggal_sampai: "2026-05-31T23:59:59",
    },
    kategori: [
      { id: 1, nama_kategori: "Seblak Kuah", deskripsi: "Menu seblak berkuah pedas", dibuat_pada: "2026-05-04T00:00:00", diperbarui_pada: "2026-05-04T00:00:00" },
      { id: 2, nama_kategori: "Seblak Kering", deskripsi: "Camilan seblak kering", dibuat_pada: "2026-05-04T00:00:00", diperbarui_pada: "2026-05-04T00:00:00" },
      { id: 3, nama_kategori: "Minuman", deskripsi: "Minuman pendamping", dibuat_pada: "2026-05-04T00:00:00", diperbarui_pada: "2026-05-04T00:00:00" },
    ],
    produk: [
      { id: 1, kategori_id: 1, nama_kategori: "Seblak Kuah", nama_produk: "Seblak Komplit Spesial", deskripsi: "Seblak kuah lengkap level pedas", harga: "25000.00", stok: 18, gambar: "storage/uploads/produk/seblak-komplit.png", status_tersedia: true, dibuat_pada: "2026-05-04T00:00:00" },
      { id: 2, kategori_id: 1, nama_kategori: "Seblak Kuah", nama_produk: "Seblak Ceker Mercon", deskripsi: "Seblak ceker pedas", harga: "20000.00", stok: 4, gambar: "storage/uploads/produk/seblak-ceker.png", status_tersedia: true, dibuat_pada: "2026-05-04T00:00:00" },
      { id: 3, kategori_id: 2, nama_kategori: "Seblak Kering", nama_produk: "Macaroni Bantet Pedas", deskripsi: "Seblak kering pedas", harga: "10000.00", stok: 0, gambar: null, status_tersedia: false, dibuat_pada: "2026-05-04T00:00:00" },
    ],
    metode: [
      { id: 1, nama_metode: "Transfer BCA", tipe_metode: "transfer_bank", nama_bank: "BCA", nomor_rekening: "1234567890", nama_pemilik_rekening: "Seblak Rika", gambar_qr: null, status_aktif: true },
      { id: 2, nama_metode: "QRIS", tipe_metode: "qris", nama_bank: null, nomor_rekening: null, nama_pemilik_rekening: null, gambar_qr: "storage/uploads/metode_pembayaran/qris.png", status_aktif: true },
    ],
    pesanan: [
      { id: 10, pelanggan_id: 1, metode_pembayaran_id: 1, nama_metode_pembayaran: "Transfer BCA", tipe_metode_pembayaran: "transfer_bank", kode_pesanan: "ORD-20260504-ABC12345", tanggal_pesanan: "2026-05-04T10:30:00", total_harga: "50000.00", nama_pelanggan: "Budi", no_telepon_pelanggan: "08123456789", alamat_pelanggan: "Jl. Mawar No. 10", catatan: "Pedas level 3", status_pembayaran: "menunggu_verifikasi", status_pesanan: "menunggu_konfirmasi", detail_pesanan: [{ nama_produk: "Seblak Komplit Spesial", harga_produk: "25000.00", jumlah: 2, subtotal: "50000.00" }] },
      { id: 11, pelanggan_id: 2, metode_pembayaran_id: 2, nama_metode_pembayaran: "QRIS", tipe_metode_pembayaran: "qris", kode_pesanan: "ORD-20260504-QR445566", tanggal_pesanan: "2026-05-04T11:15:00", total_harga: "20000.00", nama_pelanggan: "Siti", no_telepon_pelanggan: "081288889999", alamat_pelanggan: "Jl. Melati No. 5", catatan: null, status_pembayaran: "diterima", status_pesanan: "diproses", detail_pesanan: [{ nama_produk: "Seblak Ceker Mercon", harga_produk: "20000.00", jumlah: 1, subtotal: "20000.00" }] },
    ],
    riwayat: [
      { id: 1, produk_id: 1, admin_id: 1, nama_produk: "Seblak Komplit Spesial", jenis_perubahan: "masuk", stok_sebelum: 8, jumlah_perubahan: 10, stok_sesudah: 18, keterangan: "Produksi batch pagi", dibuat_pada: "2026-05-04T08:00:00" },
      { id: 2, produk_id: 2, admin_id: 1, nama_produk: "Seblak Ceker Mercon", jenis_perubahan: "keluar", stok_sebelum: 6, jumlah_perubahan: 2, stok_sesudah: 4, keterangan: "Pesanan online", dibuat_pada: "2026-05-04T10:30:00" },
    ],
    audit: [
      { id: 1, admin_id: 1, aksi: "create", entity: "produk", entity_id: 1, deskripsi: "Menambahkan produk Seblak Komplit Spesial", metadata_json: "{\"stok\":18}", dibuat_pada: "2026-05-04T08:00:00" },
      { id: 2, admin_id: 1, aksi: "update", entity: "pesanan", entity_id: 10, deskripsi: "Mengubah status pembayaran ke menunggu_verifikasi", metadata_json: "{\"status_pembayaran\":\"menunggu_verifikasi\"}", dibuat_pada: "2026-05-04T10:35:00" },
    ],
  };

  document.documentElement.lang = "id";
  document.body.classList.add("admin-shell-ready", `admin-page-${page}`);
  window.SEBLAK_ADMIN_MOCK = mock;
  window.SEBLAK_ADMIN_API = { apiBase, request, routes };

  if (page === "login") initLogin();
  else initAdminPage();

  function detectPage() {
    const path = location.pathname;
    if (path.includes("login")) return "login";
    if (path.includes("kategori")) return "kategori";
    if (path.includes("produk")) return "produk";
    if (path.includes("metode")) return "metode";
    if (path.includes("pesanan")) return "pesanan";
    if (path.includes("riwayat")) return "riwayat";
    if (path.includes("audit")) return "audit";
    return "dashboard";
  }

  function initLogin() {
    normalizeLinks();
    enhanceLoginForm();
    enhanceA11y();
  }

  function initAdminPage() {
    normalizeLinks();
    markActiveNav();
    renderShell();
    enhanceA11y();
    loadPageData();
  }

  function normalizeLinks() {
    document.querySelectorAll('a[href="#"]').forEach((link) => {
      const label = normalize(link.textContent);
      const item = navItems.find(([, name]) => label.includes(normalize(name)));
      link.href = item ? routes[item[0]] : routes.dashboard;
    });
    document.querySelectorAll("a").forEach((link) => {
      const label = normalize(link.textContent);
      if (label.includes("logout") || label.includes("keluar")) link.href = routes.login;
    });
  }

  function markActiveNav() {
    document.querySelectorAll("aside nav a, nav.fixed.left-0 a").forEach((link) => {
      const label = normalize(link.textContent);
      const active = navItems.some(([key, name]) => key === page && label.includes(normalize(name)));
      if (active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  function renderShell() {
    const main = document.querySelector("main");
    if (!main) return;
    main.classList.add("admin-main");
    main.innerHTML = `
      <section class="admin-api-panel" aria-live="polite">
        <header class="admin-page-header">
          <div>
            <p class="admin-eyebrow">Seblak Rika Admin</p>
            <h1>${pageTitle()}</h1>
            <div class="admin-contract-strip">
              <span class="admin-contract-pill"><strong>Endpoint</strong>${contracts[page].endpoint}</span>
              ${contracts[page].fields.map((field) => `<span class="admin-contract-pill">${field}</span>`).join("")}
            </div>
          </div>
          <div class="admin-header-actions">
            <label class="admin-api-base">
              API Base
              <input id="adminApiBase" type="url" value="${escapeHtml(apiBase)}" autocomplete="off" />
            </label>
            <button class="admin-button admin-button--ghost" id="adminSaveApiBase" type="button">
              <span class="material-symbols-outlined" aria-hidden="true">settings</span>
              Simpan Base
            </button>
            <button class="admin-button" id="adminReloadData" type="button">
              <span class="material-symbols-outlined" aria-hidden="true">refresh</span>
              Muat Ulang
            </button>
          </div>
        </header>
        <div class="admin-alert admin-alert--info" id="adminDataNotice">Memuat data...</div>
        <div id="adminPageContent"></div>
      </section>
    `;

    main.querySelector("#adminSaveApiBase").addEventListener("click", () => {
      const input = main.querySelector("#adminApiBase");
      localStorage.setItem("SEBLAK_API_BASE", input.value.replace(/\/$/, ""));
      setNotice("Base API disimpan. Muat ulang halaman untuk memakai base baru.", "ok");
    });
    main.querySelector("#adminReloadData").addEventListener("click", loadPageData);
  }

  async function loadPageData() {
    setNotice("Memuat data...", "info");
    try {
      if (page === "dashboard") {
        const [summary, lowStock] = await Promise.all([
          fetchOrMock("/dashboard/summary", mock.dashboardSummary),
          fetchOrMock("/dashboard/produk-stok-rendah", { threshold: 5, items: mock.produk.filter((item) => item.stok < 5) }),
        ]);
        renderDashboard(summary, unwrapList(lowStock.items || lowStock));
      } else if (page === "kategori") {
        renderKategori(await fetchOrMock("/kategori?limit=100", mock.kategori));
      } else if (page === "produk") {
        renderProduk(await fetchOrMock("/produk/admin/semua?limit=100", mock.produk));
      } else if (page === "metode") {
        renderMetode(await fetchOrMock("/metode-pembayaran?limit=100", mock.metode));
      } else if (page === "pesanan") {
        renderPesanan(await fetchOrMock("/pesanan?limit=100", mock.pesanan));
      } else if (page === "riwayat") {
        renderRiwayat(await fetchOrMock("/riwayat-stok?limit=100", mock.riwayat));
      } else if (page === "audit") {
        renderAudit(await fetchOrMock("/audit-log?limit=100", mock.audit));
      }
      enhanceA11y();
    } catch (error) {
      setNotice(error.message || "Gagal memuat data.", "bad");
    }
  }

  async function fetchOrMock(path, fallback) {
    try {
      const data = await request(path);
      setNotice("Data berhasil dimuat dari backend API.", "ok");
      return data;
    } catch (error) {
      setNotice(`Backend belum tersedia atau token belum valid. Menampilkan mock sesuai kontrak: ${error.message}`, "waiting");
      return fallback;
    }
  }

  async function request(path, options = {}) {
    const token = localStorage.getItem("access_token") || localStorage.getItem("token");
    const headers = new Headers(options.headers || {});
    if (!headers.has("Content-Type") && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
    if (token) headers.set("Authorization", `Bearer ${token}`);

    const response = await fetch(`${apiBase}${path}`, { ...options, headers });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.message || payload.detail || `HTTP ${response.status}`);
    return payload.data ?? payload;
  }

  function enhanceLoginForm() {
    const loginForm = document.querySelector("form");
    if (!loginForm) return;
    const loginButton = document.getElementById("login-button") || loginForm.querySelector('button[type="submit"]');
    const buttonText = document.getElementById("button-text");
    const loadingSpinner = document.getElementById("loading-spinner");
    const errorMessage = document.getElementById("error-message");
    const errorText = document.getElementById("error-text");

    const clone = loginForm.cloneNode(true);
    loginForm.replaceWith(clone);
    clone.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = document.getElementById("login-button") || clone.querySelector('button[type="submit"]');
      const text = document.getElementById("button-text") || button;
      const spinner = document.getElementById("loading-spinner");
      const errorBox = document.getElementById("error-message");
      const errorLabel = document.getElementById("error-text");
      button.disabled = true;
      text.classList.add("opacity-0");
      spinner?.classList.remove("hidden");
      errorBox?.classList.add("hidden");

      try {
        const formData = new FormData(clone);
        const payload = {
          email: formData.get("email"),
          kata_sandi: formData.get("kata_sandi"),
        };
        const data = await request("/auth/login", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("token_type", data.token_type || "bearer");
        window.location.href = routes.dashboard;
      } catch (error) {
        errorLabel.textContent = `${error.message}. Pastikan backend aktif dan email/kata sandi benar.`;
        errorBox?.classList.remove("hidden");
      } finally {
        button.disabled = false;
        text.classList.remove("opacity-0");
        spinner?.classList.add("hidden");
      }
    });
    void loginButton;
    void buttonText;
    void loadingSpinner;
    void errorMessage;
    void errorText;
  }

  function renderDashboard(summary, lowStock) {
    const cards = [
      ["Total Produk", summary.total_produk, "inventory_2"],
      ["Total Pelanggan", summary.total_pelanggan, "group"],
      ["Total Pesanan", summary.total_pesanan, "shopping_cart"],
      ["Pesanan Selesai", summary.pesanan_selesai, "task_alt"],
      ["Menunggu Verifikasi", summary.pembayaran_menunggu_verifikasi, "pending_actions"],
      ["Stok Rendah", summary.produk_stok_rendah, "warning"],
      ["Total Omzet", formatCurrency(summary.total_omzet), "payments"],
    ];
    setContent(`
      <div class="admin-stat-grid">${cards.map(([label, value, icon]) => statCard(label, value, icon)).join("")}</div>
      <section class="admin-card">
        <div class="admin-card__header"><h2>Produk Stok Rendah</h2><span>Threshold &lt; 5</span></div>
        ${renderTable(["Produk", "Kategori", "Harga", "Stok", "Status"], lowStock.map((item) => [
          item.nama_produk,
          item.nama_kategori || "-",
          formatCurrency(item.harga),
          item.stok,
          statusBadge(item.status_tersedia ? "tersedia" : "tidak_tersedia"),
        ]))}
      </section>
    `);
  }

  function renderKategori(items) {
    const rows = unwrapList(items).map((item) => [
      item.id,
      item.nama_kategori,
      item.deskripsi || "-",
      formatDate(item.dibuat_pada),
      rowActions(["Edit", "Hapus"]),
    ]);
    setContent(dataToolbar("Tambah Kategori", "/kategori") + renderTable(["ID", "Nama Kategori", "Deskripsi", "Dibuat", "Aksi"], rows));
  }

  function renderProduk(items) {
    const rows = unwrapList(items).map((item) => [
      item.id,
      item.nama_produk,
      item.nama_kategori || `Kategori #${item.kategori_id}`,
      formatCurrency(item.harga),
      item.stok,
      statusBadge(item.status_tersedia ? "tersedia" : "tidak_tersedia"),
      rowActions(["Stok", "Edit", "Gambar", "Hapus"]),
    ]);
    setContent(dataToolbar("Tambah Produk", "/produk") + renderTable(["ID", "Nama Produk", "Kategori", "Harga", "Stok", "Status", "Aksi"], rows));
  }

  function renderMetode(items) {
    const rows = unwrapList(items).map((item) => [
      item.id,
      item.nama_metode,
      statusBadge(item.tipe_metode),
      item.nama_bank || "-",
      item.nomor_rekening || item.gambar_qr || "-",
      statusBadge(item.status_aktif ? "aktif" : "nonaktif"),
      rowActions(["Edit", "QR", "Hapus"]),
    ]);
    setContent(dataToolbar("Tambah Metode", "/metode-pembayaran") + renderTable(["ID", "Nama Metode", "Tipe", "Bank", "Rekening / QR", "Status", "Aksi"], rows));
  }

  function renderPesanan(items) {
    const rows = unwrapList(items).map((item) => [
      item.kode_pesanan,
      item.nama_pelanggan,
      item.no_telepon_pelanggan,
      item.nama_metode_pembayaran || "-",
      formatCurrency(item.total_harga),
      statusBadge(item.status_pembayaran),
      statusBadge(item.status_pesanan),
      rowActions(["Detail", "Status"]),
    ]);
    setContent(dataToolbar("Buat Pesanan", "/pesanan") + renderTable(["Kode", "Pelanggan", "Telepon", "Metode", "Total", "Pembayaran", "Pesanan", "Aksi"], rows));
  }

  function renderRiwayat(items) {
    const rows = unwrapList(items).map((item) => [
      item.id,
      item.nama_produk || `Produk #${item.produk_id}`,
      statusBadge(item.jenis_perubahan),
      item.stok_sebelum,
      item.jumlah_perubahan,
      item.stok_sesudah,
      item.keterangan || "-",
      formatDate(item.dibuat_pada),
    ]);
    setContent(dataToolbar("Catat Perubahan Stok", "/riwayat-stok") + renderTable(["ID", "Produk", "Jenis", "Sebelum", "Jumlah", "Sesudah", "Keterangan", "Dibuat"], rows));
  }

  function renderAudit(items) {
    const rows = unwrapList(items).map((item) => [
      item.id,
      item.admin_id || "-",
      statusBadge(item.aksi),
      item.entity,
      item.entity_id || "-",
      item.deskripsi || "-",
      formatDate(item.dibuat_pada),
    ]);
    setContent(renderTable(["ID", "Admin", "Aksi", "Entity", "Entity ID", "Deskripsi", "Dibuat"], rows));
  }

  function dataToolbar(label, endpoint) {
    return `
      <div class="admin-toolbar">
        <div>
          <strong>Siap API</strong>
          <span>Form aksi memakai kontrak backend ${endpoint}. Tombol disiapkan untuk integrasi POST/PUT/PATCH/DELETE.</span>
        </div>
        <button class="admin-button" type="button"><span class="material-symbols-outlined" aria-hidden="true">add</span>${label}</button>
      </div>
    `;
  }

  function renderTable(headers, rows) {
    return `
      <section class="admin-card">
        <div class="admin-table-wrap">
          <table class="admin-table">
            <thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
            <tbody>
              ${rows.length ? rows.map((row) => `<tr>${row.map((cell) => `<td>${cell ?? "-"}</td>`).join("")}</tr>`).join("") : `<tr><td colspan="${headers.length}">Belum ada data.</td></tr>`}
            </tbody>
          </table>
        </div>
      </section>
    `;
  }

  function statCard(label, value, icon) {
    return `
      <article class="admin-stat-card">
        <span class="material-symbols-outlined" aria-hidden="true">${icon}</span>
        <div><p>${label}</p><strong>${value ?? 0}</strong></div>
      </article>
    `;
  }

  function rowActions(labels) {
    return `<div class="admin-row-actions">${labels.map((label) => `<button class="admin-icon-button" type="button" aria-label="${label}">${label}</button>`).join("")}</div>`;
  }

  function statusBadge(value) {
    const safe = String(value ?? "-");
    const tone = {
      belum_dibayar: "waiting",
      menunggu_verifikasi: "waiting",
      diterima: "ok",
      ditolak: "bad",
      menunggu_konfirmasi: "waiting",
      diproses: "info",
      selesai: "ok",
      dibatalkan: "bad",
      tersedia: "ok",
      tidak_tersedia: "bad",
      aktif: "ok",
      nonaktif: "bad",
      masuk: "ok",
      keluar: "bad",
      penyesuaian: "info",
      qris: "info",
      transfer_bank: "info",
      create: "ok",
      update: "info",
      delete: "bad",
    }[safe] || "info";
    return `<span class="admin-status admin-status--${tone}">${safe}</span>`;
  }

  function setContent(html) {
    const content = document.getElementById("adminPageContent");
    if (content) content.innerHTML = html;
  }

  function setNotice(message, tone) {
    const notice = document.getElementById("adminDataNotice");
    if (!notice) return;
    notice.textContent = message;
    notice.className = `admin-alert admin-alert--${tone || "info"}`;
  }

  function pageTitle() {
    return {
      dashboard: "Ringkasan Dashboard",
      kategori: "Manajemen Kategori",
      produk: "Manajemen Produk",
      metode: "Metode Pembayaran",
      pesanan: "Manajemen Pesanan",
      riwayat: "Riwayat Stok",
      audit: "Audit Log",
    }[page] || "Dashboard";
  }

  function unwrapList(value) {
    if (Array.isArray(value)) return value;
    if (Array.isArray(value?.items)) return value.items;
    if (Array.isArray(value?.data)) return value.data;
    return [];
  }

  function formatCurrency(value) {
    const number = Number(value || 0);
    return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(number);
  }

  function formatDate(value) {
    if (!value) return "-";
    return new Intl.DateTimeFormat("id-ID", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
  }

  function enhanceA11y() {
    document.querySelectorAll("button").forEach((button) => {
      if (!button.textContent.trim() && !button.getAttribute("aria-label")) button.setAttribute("aria-label", "Tombol aksi");
      button.className = button.className.replace(/\btransition-all\b/g, "transition-colors");
    });
    document.querySelectorAll("input, select, textarea").forEach((field, index) => {
      if (!field.name) field.name = field.id || `admin_field_${index + 1}`;
      if (!field.id) field.id = field.name;
      if (field.matches('input[type="text"], input[type="url"], textarea, select')) field.setAttribute("autocomplete", "off");
      if (field.matches('input[type="email"]')) {
        field.setAttribute("autocomplete", "username");
        field.setAttribute("spellcheck", "false");
      }
      if (field.matches('input[type="password"]')) field.setAttribute("autocomplete", "current-password");
    });
    document.querySelectorAll("img").forEach((img) => {
      if (!img.alt) img.alt = "Gambar data Seblak Rika";
      if (!img.width) img.width = img.naturalWidth || 80;
      if (!img.height) img.height = img.naturalHeight || 80;
      if (!img.loading) img.loading = "lazy";
    });
  }

  function normalize(value) {
    return (value || "").trim().replace(/\s+/g, " ").toLowerCase();
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
  }
})();
