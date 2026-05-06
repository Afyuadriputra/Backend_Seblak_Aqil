import pytest

from app.shared.exceptions import BadRequestException
from app.shared.file_validator import (
    generate_safe_filename,
    validate_file_extension,
    validate_file_size,
    validate_upload_content,
)


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        (b"\xff\xd8\xff\xe0jpeg", "image/jpeg"),
        (b"\x89PNG\r\n\x1a\npng", "image/png"),
        (b"RIFF\x10\x00\x00\x00WEBPwebp", "image/webp"),
    ],
)
def test_magic_bytes_valid_should_pass(content, content_type):
    validate_upload_content(content, content_type)


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        (b"<html></html>", "image/jpeg"),
        (b"not-png", "image/png"),
        (b"not-webp", "image/webp"),
    ],
)
def test_magic_bytes_invalid_should_fail(content, content_type):
    with pytest.raises(BadRequestException):
        validate_upload_content(content, content_type)


@pytest.mark.parametrize("filename", ["bukti.svg", "bukti.php", "bukti.js", "bukti.jpg.php"])
def test_dangerous_extensions_should_fail(filename):
    with pytest.raises(BadRequestException):
        validate_file_extension(filename)


def test_empty_file_size_should_fail():
    with pytest.raises(BadRequestException):
        validate_file_size(0)


def test_safe_filename_should_not_use_original_name():
    generated = generate_safe_filename("bukti pembayaran.png")

    assert generated != "bukti pembayaran.png"
    assert generated.endswith(".png")
