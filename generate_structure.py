from pathlib import Path


def create_structure():
    # 1. File Root
    root_files = [
        "pyproject.toml",
        ".gitignore",
        ".env",
        ".env.example",
        "alembic.ini",
        "docker-compose.yml",
        "mkdocs.yml",
        "requirements.txt",
        "README.md",
    ]

    # 2. File App (Core & Shared)
    app_files = [
        "app/__init__.py",
        "app/main.py",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/core/dependencies.py",
        "app/core/logger.py",
        "app/core/middleware.py",
        "app/core/security.py",
        "app/shared/__init__.py",
        "app/shared/enums.py",
        "app/shared/exceptions.py",
        "app/shared/file_validator.py",
        "app/shared/pagination.py",
        "app/shared/response.py",
        "app/shared/utils.py",
        "app/modules/__init__.py",
    ]

    # 3. File Docs
    docs_files = [
        "docs/index.md",
        "docs/architecture.md",
        "docs/modules.md",
        "docs/database.md",
        "docs/api-flow.md",
        "docs/testing.md",
        "docs/security-performance.md",
    ]

    # 4. File Logs & Storage
    misc_files = ["logs/.gitkeep", "logs/app.log", "storage/uploads/bukti_pembayaran/.gitkeep"]

    # 5. File Tests Dasar
    test_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/core/__init__.py",
        "tests/shared/__init__.py",
        "tests/modules/__init__.py",
    ]

    # 6. Modul Aplikasi
    modules = [
        "admin",
        "auth",
        "bukti_pembayaran",
        "kategori",
        "metode_pembayaran",
        "pelanggan",
        "pesanan",
        "produk",
        "riwayat_stok",
    ]

    print("🚀 Memperbarui arsitektur proyek sesuai struktur terbaru...")

    all_files = root_files + app_files + docs_files + misc_files + test_files

    # Tambahkan file controller, service, repository, model ke masing-masing modul
    for mod in modules:
        all_files.extend(
            [
                f"app/modules/{mod}/__init__.py",
                f"app/modules/{mod}/controller.py",
                f"app/modules/{mod}/service.py",
                f"app/modules/{mod}/repository.py",
                f"app/modules/{mod}/model.py",
                f"tests/modules/{mod}/__init__.py",
                f"tests/modules/{mod}/test_controller.py",
                f"tests/modules/{mod}/test_service.py",
                f"tests/modules/{mod}/test_repository.py",
                f"tests/modules/{mod}/test_model.py",
            ]
        )

    # Eksekusi pembuatan file
    for f in all_files:
        file_path = Path(f)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)

    # Buat folder khusus yang mungkin kosong (selain dari file di atas)
    empty_dirs = ["alembic/versions"]

    for d in empty_dirs:
        dir_path = Path(d)
        dir_path.mkdir(parents=True, exist_ok=True)

    print("✅ Struktur arsitektur berhasil disesuaikan!")
    print("   - Folder docs/ dan file markdown sudah dibuat.")
    print("   - .gitkeep dan app.log sudah ada di tempatnya.")
    print("   - __init__.py sudah disebar dengan benar.")


if __name__ == "__main__":
    create_structure()
