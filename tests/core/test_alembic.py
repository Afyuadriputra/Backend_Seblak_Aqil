from app.core.database import Base


def test_alembic_target_metadata_available():
    assert Base.metadata is not None


def test_model_imports_module_can_be_imported():
    import app.modules.model_imports  # noqa: F401
