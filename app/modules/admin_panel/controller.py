# ruff: noqa: E501
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Admin Panel"])


@router.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def admin_panel():
    return ADMIN_HTML


ADMIN_HTML = r"""
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Admin Seblak Rika</title>
  <style>
    :root {
      --ink: #17211b;
      --muted: #66736a;
      --paper: #f7f3ea;
      --panel: #fffdf7;
      --line: #ded6c7;
      --brand: #b32222;
      --leaf: #376b4a;
      --gold: #c58b2b;
      --shadow: 0 18px 50px rgba(39, 31, 20, .12);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(179,34,34,.08), transparent 35%),
        radial-gradient(circle at 80% 0%, rgba(197,139,43,.2), transparent 32%),
        var(--paper);
      font-family: "Trebuchet MS", Verdana, sans-serif;
    }
    button, input, select, textarea { font: inherit; }
    .shell { min-height: 100vh; display: grid; grid-template-columns: 260px 1fr; }
    aside {
      padding: 24px 18px;
      border-right: 1px solid var(--line);
      background: rgba(255,253,247,.84);
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
    }
    .brand { font-size: 24px; font-weight: 900; letter-spacing: .2px; margin-bottom: 6px; }
    .sub { color: var(--muted); font-size: 12px; margin-bottom: 22px; }
    nav { display: grid; gap: 8px; }
    nav button {
      border: 1px solid transparent;
      background: transparent;
      text-align: left;
      padding: 11px 12px;
      border-radius: 8px;
      cursor: pointer;
      color: var(--ink);
    }
    nav button.active, nav button:hover {
      border-color: var(--line);
      background: #fff8e7;
      color: var(--brand);
    }
    main { padding: 28px; overflow: auto; }
    .topbar { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 20px; }
    h1 { margin: 0; font-size: 30px; }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 18px;
      margin-bottom: 18px;
    }
    .grid { display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 14px; }
    .metric { border-left: 4px solid var(--brand); }
    .metric .n { font-size: 26px; font-weight: 900; margin-top: 6px; }
    .muted { color: var(--muted); font-size: 13px; }
    .row { display: flex; gap: 10px; flex-wrap: wrap; align-items: end; }
    input, select, textarea {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 10px;
      background: #fff;
      min-width: 150px;
    }
    textarea { min-height: 42px; }
    label { display: grid; gap: 5px; color: var(--muted); font-size: 12px; }
    .btn {
      border: 0;
      border-radius: 7px;
      padding: 10px 13px;
      background: var(--ink);
      color: white;
      cursor: pointer;
    }
    .btn.red { background: var(--brand); }
    .btn.green { background: var(--leaf); }
    .btn.gold { background: var(--gold); }
    .btn.light { background: #efe7d6; color: var(--ink); }
    table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
    th, td { border-bottom: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; font-size: 13px; }
    th { background: #f0e7d6; color: #3b3328; }
    .hidden { display: none !important; }
    .login {
      max-width: 420px;
      margin: 10vh auto;
    }
    .notice { padding: 10px 12px; border-radius: 8px; margin-bottom: 14px; background: #fff4d8; color: #6a4610; }
    .danger { background: #ffe8e8; color: #842020; }
    @media (max-width: 920px) {
      .shell { grid-template-columns: 1fr; }
      aside { position: relative; height: auto; }
      .grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 560px) {
      main { padding: 16px; }
      .grid { grid-template-columns: 1fr; }
      input, select, textarea { width: 100%; }
    }
  </style>
</head>
<body>
  <section id="loginView" class="login card">
    <h1>Admin Seblak Rika</h1>
    <p class="muted">Masuk untuk mengelola produk, pesanan, pembayaran, stok, dan audit.</p>
    <div id="loginMsg"></div>
    <label>Email <input id="email" value="admin@example.com"></label><br>
    <label>Kata sandi <input id="password" type="password" value="password123"></label><br>
    <button class="btn red" onclick="login()" type="button">Masuk</button>
  </section>

  <section id="appView" class="shell hidden">
    <aside>
      <div class="brand">Seblak Rika</div>
      <div class="sub">Admin dashboard</div>
      <nav id="nav"></nav>
      <button class="btn light" style="margin-top:18px;width:100%" onclick="logout()">Keluar</button>
    </aside>
    <main>
      <div class="topbar">
        <div>
          <h1 id="pageTitle">Dashboard</h1>
          <div class="muted" id="pageSub">Ringkasan operasional toko</div>
        </div>
        <button class="btn green" onclick="refresh()">Refresh</button>
      </div>
      <div id="msg"></div>
      <section id="content"></section>
    </main>
  </section>

<script>
const state = { token: localStorage.getItem("admin_token"), page: "dashboard" };
const pages = [
  ["dashboard", "Dashboard"], ["kategori", "Kategori"], ["produk", "Produk"],
  ["metode", "Pembayaran"], ["pesanan", "Pesanan"], ["pelanggan", "Pelanggan"],
  ["stok", "Riwayat Stok"], ["audit", "Audit Log"]
];

function headers(json=true) {
  const h = { Authorization: `Bearer ${state.token}` };
  if (json) h["Content-Type"] = "application/json";
  return h;
}
async function api(path, opts={}) {
  opts.headers = opts.headers || headers(!(opts.body instanceof FormData));
  const res = await fetch(path, opts);
  const body = await res.json().catch(() => ({}));
  if (!res.ok || body.success === false) throw new Error(body.message || `HTTP ${res.status}`);
  return body.data;
}
function money(v) { return `Rp ${Number(v || 0).toLocaleString("id-ID")}`; }
function showMsg(text, bad=false) {
  document.getElementById("msg").innerHTML = text ? `<div class="notice ${bad?'danger':''}">${text}</div>` : "";
}
function renderNav() {
  document.getElementById("nav").innerHTML = pages.map(([id, label]) =>
    `<button class="${state.page===id?'active':''}" onclick="go('${id}')">${label}</button>`
  ).join("");
}
function go(page) { state.page = page; renderNav(); refresh(); }
function ensureAuth() {
  document.getElementById("loginView").classList.toggle("hidden", !!state.token);
  document.getElementById("appView").classList.toggle("hidden", !state.token);
  if (state.token) { renderNav(); refresh(); }
}
async function login() {
  const loginMsg = document.getElementById("loginMsg");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  try {
    loginMsg.innerHTML = "";
    const data = await api("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: emailInput.value, kata_sandi: passwordInput.value })
    });
    state.token = data.access_token;
    localStorage.setItem("admin_token", state.token);
    ensureAuth();
  } catch (e) {
    loginMsg.innerHTML = `<div class="notice danger">${e.message}</div>`;
  }
}
function logout() { localStorage.removeItem("admin_token"); state.token = ""; ensureAuth(); }
async function refresh() {
  showMsg("");
  const map = { dashboard, kategori, produk, metode, pesanan, pelanggan, stok, audit };
  try { await map[state.page](); } catch(e) { showMsg(e.message, true); }
}

async function dashboard() {
  pageTitle.textContent = "Dashboard";
  pageSub.textContent = "Ringkasan, omzet, pembayaran, dan stok rendah";
  content.innerHTML = `
    <div class="card row">
      <label>Dari <input id="tglDari" type="datetime-local"></label>
      <label>Sampai <input id="tglSampai" type="datetime-local"></label>
      <label>Threshold stok <input id="stokThreshold" type="number" value="5"></label>
      <button class="btn" onclick="dashboard()">Terapkan</button>
    </div><div id="dashData"></div>`;
  const q = new URLSearchParams();
  if (tglDari.value) q.set("tanggal_dari", new Date(tglDari.value).toISOString());
  if (tglSampai.value) q.set("tanggal_sampai", new Date(tglSampai.value).toISOString());
  q.set("stok_threshold", stokThreshold.value || 5);
  const d = await api(`/dashboard/summary?${q}`);
  const low = await api(`/dashboard/produk-stok-rendah?threshold=${stokThreshold.value || 5}`);
  dashData.innerHTML = `
    <div class="grid">
      ${metric("Produk", d.total_produk)} ${metric("Pelanggan", d.total_pelanggan)}
      ${metric("Pesanan", d.total_pesanan)} ${metric("Selesai", d.pesanan_selesai)}
      ${metric("Menunggu bayar", d.pembayaran_menunggu_verifikasi)}
      ${metric("Stok rendah", d.produk_stok_rendah)} ${metric("Omzet", money(d.total_omzet))}
    </div>
    <div class="card"><h3>Produk stok rendah</h3>${table(low.items, ["id","nama_produk","nama_kategori","stok","harga"])}</div>`;
}
function metric(label, value) { return `<div class="card metric"><div class="muted">${label}</div><div class="n">${value}</div></div>`; }

async function kategori() {
  pageTitle.textContent = "Kategori"; pageSub.textContent = "Kelola kategori produk";
  content.innerHTML = `
    <div class="card row">
      <label>Nama <input id="katNama"></label><label>Deskripsi <input id="katDesk"></label>
      <button class="btn red" onclick="createKategori()">Tambah</button>
    </div><div id="katList"></div>`;
  const data = await api("/kategori?limit=100");
  katList.innerHTML = table(data, ["id","nama_kategori","deskripsi"]);
}
async function createKategori() {
  await api("/kategori", { method:"POST", body:JSON.stringify({ nama_kategori:katNama.value, deskripsi:katDesk.value }) });
  await kategori();
}

async function produk() {
  pageTitle.textContent = "Produk"; pageSub.textContent = "Produk, stok, status, dan gambar";
  const kats = await api("/kategori?limit=100");
  content.innerHTML = `
    <div class="card row">
      <label>Kategori <select id="pKat">${kats.map(k=>`<option value="${k.id}">${k.nama_kategori}</option>`)}</select></label>
      <label>Nama <input id="pNama"></label><label>Harga <input id="pHarga" type="number"></label>
      <label>Stok <input id="pStok" type="number" value="0"></label>
      <button class="btn red" onclick="createProduk()">Tambah</button>
    </div>
    <div class="card row"><label>Cari <input id="pSearch"></label><button class="btn" onclick="loadProduk()">Cari</button></div>
    <div id="produkList"></div>`;
  await loadProduk();
}
async function loadProduk() {
  const q = new URLSearchParams({ limit: 100 });
  if (window.pSearch && pSearch.value) q.set("search", pSearch.value);
  const data = await api(`/produk/admin/semua?${q}`);
  produkList.innerHTML = table(data, ["id","nama_produk","nama_kategori","harga","stok","status_tersedia","gambar"]) +
    `<div class="card row"><label>ID Produk <input id="imgProdukId" type="number"></label><label>Gambar <input id="imgProdukFile" type="file"></label><button class="btn gold" onclick="uploadProdukImage()">Upload gambar</button></div>`;
}
async function createProduk() {
  await api("/produk", { method:"POST", body:JSON.stringify({ kategori_id:+pKat.value, nama_produk:pNama.value, harga:pHarga.value, stok:+pStok.value }) });
  await produk();
}
async function uploadProdukImage() {
  const fd = new FormData(); fd.append("file", imgProdukFile.files[0]);
  await api(`/produk/${imgProdukId.value}/gambar`, { method:"PATCH", headers:{ Authorization:`Bearer ${state.token}` }, body:fd });
  await loadProduk();
}

async function metode() {
  pageTitle.textContent = "Pembayaran"; pageSub.textContent = "Metode pembayaran dan QR";
  content.innerHTML = `
    <div class="card row">
      <label>Nama <input id="mNama"></label><label>Tipe <select id="mTipe"><option value="qris">QRIS</option><option value="transfer_bank">Transfer Bank</option></select></label>
      <label>Bank <input id="mBank"></label><label>Rekening <input id="mRek"></label><label>Pemilik <input id="mPemilik"></label>
      <label>QR path <input id="mQr" value="qris.png"></label><button class="btn red" onclick="createMetode()">Tambah</button>
    </div><div id="metodeList"></div>`;
  const data = await api("/metode-pembayaran?limit=100");
  metodeList.innerHTML = table(data, ["id","nama_metode","tipe_metode","status_aktif","nama_bank","nomor_rekening","gambar_qr"]) +
    `<div class="card row"><label>ID Metode <input id="qrMetodeId" type="number"></label><label>QR <input id="qrFile" type="file"></label><button class="btn gold" onclick="uploadQr()">Upload QR</button></div>`;
}
async function createMetode() {
  const body = { nama_metode:mNama.value, tipe_metode:mTipe.value, gambar_qr:mQr.value || "qris.png", nama_bank:mBank.value || null, nomor_rekening:mRek.value || null, nama_pemilik_rekening:mPemilik.value || null };
  await api("/metode-pembayaran", { method:"POST", body:JSON.stringify(body) });
  await metode();
}
async function uploadQr() {
  const fd = new FormData(); fd.append("file", qrFile.files[0]);
  await api(`/metode-pembayaran/${qrMetodeId.value}/gambar-qr`, { method:"PATCH", headers:{ Authorization:`Bearer ${state.token}` }, body:fd });
  await metode();
}

async function pesanan() {
  pageTitle.textContent = "Pesanan"; pageSub.textContent = "Verifikasi pembayaran dan status pesanan";
  content.innerHTML = `<div class="card row">
    <label>Status Bayar <select id="fBayar"><option></option><option>belum_dibayar</option><option>menunggu_verifikasi</option><option>diterima</option><option>ditolak</option></select></label>
    <label>Status Pesanan <select id="fPes"><option></option><option>menunggu_konfirmasi</option><option>diproses</option><option>selesai</option><option>dibatalkan</option></select></label>
    <button class="btn" onclick="loadPesanan()">Filter</button></div><div id="pesananList"></div>`;
  await loadPesanan();
}
async function loadPesanan() {
  const q = new URLSearchParams({ limit: 100 });
  if (fBayar.value) q.set("status_pembayaran", fBayar.value);
  if (fPes.value) q.set("status_pesanan", fPes.value);
  const data = await api(`/pesanan?${q}`);
  pesananList.innerHTML = table(data, ["id","kode_pesanan","nama_pelanggan","nama_metode_pembayaran","total_harga","status_pembayaran","status_pesanan"]) +
    `<div class="card row"><label>ID <input id="orderId" type="number"></label><label>Status Bayar <select id="newBayar"><option>diterima</option><option>ditolak</option><option>menunggu_verifikasi</option></select></label><button class="btn green" onclick="setBayar()">Update bayar</button><label>Status Pesanan <select id="newPes"><option>diproses</option><option>selesai</option><option>dibatalkan</option><option>menunggu_konfirmasi</option></select></label><button class="btn gold" onclick="setPesanan()">Update pesanan</button></div>`;
}
async function setBayar(){ await api(`/pesanan/${orderId.value}/status-pembayaran`, { method:"PATCH", body:JSON.stringify({status_pembayaran:newBayar.value}) }); await loadPesanan(); }
async function setPesanan(){ await api(`/pesanan/${orderId.value}/status-pesanan`, { method:"PATCH", body:JSON.stringify({status_pesanan:newPes.value}) }); await loadPesanan(); }

async function pelanggan() {
  pageTitle.textContent = "Pelanggan"; pageSub.textContent = "Data pelanggan checkout";
  content.innerHTML = `<div class="card row"><label>Cari <input id="custSearch"></label><button class="btn" onclick="pelanggan()">Cari</button></div><div id="custList"></div>`;
  const q = new URLSearchParams({ limit: 100 }); if (custSearch.value) q.set("search", custSearch.value);
  const data = await api(`/pelanggan?${q}`);
  custList.innerHTML = table(data, ["id","nama_pelanggan","no_telepon","alamat"]);
}

async function stok() {
  pageTitle.textContent = "Riwayat Stok"; pageSub.textContent = "Stok masuk, keluar, penyesuaian";
  content.innerHTML = `<div class="card row">
    <label>ID Produk <input id="stokProduk" type="number"></label><label>Jenis <select id="stokJenis"><option>masuk</option><option>keluar</option><option>penyesuaian</option></select></label>
    <label>Jumlah <input id="stokJumlah" type="number"></label><label>Stok baru <input id="stokBaru" type="number"></label><label>Keterangan <input id="stokKet"></label><button class="btn red" onclick="createStok()">Simpan</button>
  </div><div id="stokList"></div>`;
  const data = await api("/riwayat-stok?limit=100");
  stokList.innerHTML = table(data, ["id","produk_id","admin_id","jenis_perubahan","stok_sebelum","jumlah_perubahan","stok_sesudah","keterangan"]);
}
async function createStok() {
  const body = { produk_id:+stokProduk.value, jenis_perubahan:stokJenis.value, jumlah_perubahan:+stokJumlah.value, keterangan:stokKet.value || null };
  if (stokJenis.value === "penyesuaian") body.stok_baru = +stokBaru.value;
  await api("/riwayat-stok", { method:"POST", body:JSON.stringify(body) });
  await stok();
}

async function audit() {
  pageTitle.textContent = "Audit Log"; pageSub.textContent = "Jejak aktivitas penting";
  const data = await api("/audit-log?limit=100");
  content.innerHTML = table(data, ["id","admin_id","aksi","entity","entity_id","deskripsi","dibuat_pada"]);
}
function table(rows, cols) {
  rows = rows || [];
  if (!rows.length) return `<div class="card muted">Belum ada data.</div>`;
  return `<div class="card"><table><thead><tr>${cols.map(c=>`<th>${c}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr>${cols.map(c=>`<td>${r[c] ?? ""}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
ensureAuth();
</script>
</body>
</html>
"""
