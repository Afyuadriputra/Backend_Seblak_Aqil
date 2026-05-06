from pathlib import Path
from uuid import UUID

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.shared.exceptions import BadRequestException
from app.shared.file_validator import generate_safe_filename, validate_file_extension

pytestmark = pytest.mark.fuzz


@pytest.mark.parametrize(
    "filename",
    [
        "../../.env",
        "..\\..\\secret",
        "bukti.jpg.php",
        "bukti.png%00.exe",
        "",
        "x" * 300 + ".php",
    ],
)
def test_dangerous_upload_filenames_should_be_rejected(filename):
    with pytest.raises(BadRequestException):
        validate_file_extension(filename)


@pytest.mark.parametrize("filename", ["bukti.jpg", "bukti with space.png", "BUKTI.WEBP"])
def test_valid_upload_filename_should_generate_uuid_storage_name(filename):
    validate_file_extension(filename)

    generated = generate_safe_filename(filename)

    assert generated != filename
    assert Path(generated).suffix.lower() == Path(filename).suffix.lower()
    UUID(Path(generated).stem)


@given(
    name=st.text(
        alphabet=st.characters(
            whitelist_categories=("Ll", "Lu", "Nd"),
            whitelist_characters=" _-",
        ),
        min_size=0,
        max_size=80,
    ),
    ext=st.sampled_from([".jpg", ".jpeg", ".png", ".webp"]),
)
@settings(max_examples=40)
def test_valid_extension_fuzz_should_generate_uuid_filename(name, ext):
    filename = f"{name or 'bukti'}{ext}"

    validate_file_extension(filename)
    generated = generate_safe_filename(filename)

    assert generated != filename
    UUID(Path(generated).stem)


@given(filename=st.text(min_size=0, max_size=120))
@settings(max_examples=40)
def test_random_filename_fuzz_should_not_crash(filename):
    try:
        validate_file_extension(filename)
    except BadRequestException:
        return

    generated = generate_safe_filename(filename)
    UUID(Path(generated).stem)
