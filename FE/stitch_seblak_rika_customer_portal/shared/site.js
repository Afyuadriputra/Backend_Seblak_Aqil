(function () {
  const script = document.currentScript;
  const page = script?.dataset.page || "menu";
  const base = script?.dataset.base || "..";

  const routes = {
    menu: `${base}/home_menu_seblak_rika/code.html`,
    detail: `${base}/detail_produk_seblak_rika/code.html`,
    checkout: `${base}/keranjang_checkout_seblak_rika/code.html`,
    success: `${base}/pesanan_berhasil_seblak_rika/code.html`,
    upload: `${base}/upload_bukti_bayar_seblak_rika/code.html`,
    track: `${base}/lacak_pesanan_seblak_rika/code.html`,
  };

  const navItems = [
    { key: "menu", label: "Menu", icon: "restaurant_menu", href: routes.menu },
    { key: "checkout", label: "Checkout", icon: "shopping_basket", href: routes.checkout },
    { key: "track", label: "Lacak", icon: "local_shipping", href: routes.track },
    { key: "upload", label: "Upload", icon: "upload_file", href: routes.upload },
  ];

  document.body.classList.add("sr-shell-ready", `sr-page-${page}`);

  function icon(name) {
    const span = document.createElement("span");
    span.className = "material-symbols-outlined";
    span.setAttribute("aria-hidden", "true");
    span.textContent = name;
    return span;
  }

  function createHeader() {
    const header = document.createElement("header");
    header.className = "sr-site-header";

    const inner = document.createElement("div");
    inner.className = "sr-site-header__inner";

    const brand = document.createElement("a");
    brand.className = "sr-brand";
    brand.href = routes.menu;
    brand.setAttribute("aria-label", "Seblak Rika - kembali ke menu");

    const mark = document.createElement("span");
    mark.className = "sr-brand-mark";
    mark.appendChild(icon("local_fire_department"));
    brand.append(mark, document.createTextNode("Seblak Rika"));

    const nav = document.createElement("nav");
    nav.className = "sr-main-nav";
    nav.setAttribute("aria-label", "Navigasi utama");

    navItems.forEach((item) => {
      const link = document.createElement("a");
      link.className = "sr-nav-link";
      link.href = item.href;
      if (item.key === page) link.setAttribute("aria-current", "page");
      link.append(icon(item.icon), document.createTextNode(item.label));
      nav.appendChild(link);
    });

    inner.append(brand, nav);
    header.appendChild(inner);
    document.body.prepend(header);
  }

  function createBottomNav() {
    const nav = document.createElement("nav");
    nav.className = "sr-bottom-nav";
    nav.setAttribute("aria-label", "Navigasi bawah");

    navItems.forEach((item) => {
      const link = document.createElement("a");
      link.className = "sr-bottom-nav__link";
      link.href = item.href;
      if (item.key === page) link.setAttribute("aria-current", "page");
      link.append(icon(item.icon), document.createElement("span"));
      link.lastElementChild.textContent = item.label;
      nav.appendChild(link);
    });

    document.body.appendChild(nav);
  }

  function wirePageLinks() {
    document.querySelectorAll('a[href="#"]').forEach((link) => {
      const text = link.textContent.trim().toLowerCase();
      if (text.includes("menu")) link.href = routes.menu;
      if (text.includes("cart") || text.includes("checkout")) link.href = routes.checkout;
      if (text.includes("track") || text.includes("lacak")) link.href = routes.track;
      if (text.includes("upload")) link.href = routes.upload;
    });

    if (page === "menu") {
      document.querySelectorAll("h3").forEach((title) => {
        const text = title.textContent || "";
        const card = title.closest(".bg-surface-container-lowest");
        if (card && /Seblak|Makaroni|Es Teh|Komplit|Ceker/i.test(text)) {
          makeLink(card, routes.detail, `Buka detail ${text.trim()}`);
        }
      });
      const stickyCart = [...document.querySelectorAll("div")].find((node) =>
        node.textContent.trim().includes("Lanjut Bayar")
      );
      if (stickyCart) makeLink(stickyCart, routes.checkout, "Lanjut ke checkout");
    }

    if (page === "detail") {
      [...document.querySelectorAll("button")].forEach((button) => {
        if (button.textContent.includes("Tambah")) {
          button.addEventListener("click", () => {
            window.location.href = routes.checkout;
          });
        }
      });
    }

    if (page === "checkout") {
      [...document.querySelectorAll("div")].forEach((node) => {
        if (node.classList.contains("fixed") && node.textContent.includes("Total Pembayaran")) {
          node.classList.add("sr-checkout-sticky");
        }
      });
      [...document.querySelectorAll("button")].forEach((button) => {
        if (button.textContent.includes("Pesan Sekarang")) {
          button.addEventListener("click", () => {
            window.location.href = routes.success;
          });
        }
      });
    }

    if (page === "success") {
      [...document.querySelectorAll("button")].forEach((button) => {
        const text = button.textContent.trim();
        if (text.includes("Upload Bukti")) {
          button.addEventListener("click", () => {
            window.location.href = routes.upload;
          });
        }
        if (text.includes("Lacak Pesanan")) {
          button.addEventListener("click", () => {
            window.location.href = routes.track;
          });
        }
        if (text.includes("Salin")) {
          button.addEventListener("click", async () => {
            const code = document.querySelector("[data-order-code]")?.textContent?.trim() || "SBL-88291";
            await navigator.clipboard?.writeText(code);
            button.setAttribute("aria-live", "polite");
            button.querySelector("span:last-child").textContent = "Tersalin";
          });
        }
      });
    }

    if (page === "upload") {
      [...document.querySelectorAll("button")].forEach((button) => {
        if (button.textContent.includes("Kirim Bukti") || button.textContent.includes("Unggah")) {
          button.addEventListener("click", () => {
            window.location.href = routes.track;
          });
        }
      });
    }
  }

  function makeLink(element, href, label) {
    element.classList.add("sr-linkified");
    element.setAttribute("role", "link");
    element.setAttribute("tabindex", "0");
    element.setAttribute("aria-label", label);
    element.addEventListener("click", (event) => {
      const target = event.target;
      if (target.closest("button, a, input, textarea, select")) return;
      window.location.href = href;
    });
    element.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        window.location.href = href;
      }
    });
  }

  createHeader();
  createBottomNav();
  wirePageLinks();
})();
