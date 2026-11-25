from document_processing.classifier import classify_document
from document_processing.validator import validate_file
from document_processing.extractor import extract_text
import pytest

def test_classifies_invoice():
    assert classify_document("invoice_01.pdf", "") == "Finance"

def test_classifies_hr_content():
    assert classify_document("document.txt", "employee leave request") == "HR"

def test_rejects_unsupported_extension():
    with pytest.raises(ValueError):
        validate_file("malware.exe", 100)

def test_rejects_empty_file():
    with pytest.raises(ValueError):
        validate_file("empty.txt", 0)

def test_rejects_oversized_file():
    with pytest.raises(ValueError):
        validate_file("large.txt", 11 * 1024 * 1024)

def test_extracts_text_file():
    assert extract_text(b"hello workflow", ".txt") == "hello workflow"
