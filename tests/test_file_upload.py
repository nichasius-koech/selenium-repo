import re
import pytest
from pathlib import Path, PureWindowsPath

file_path = Path(__file__).parent.parent / "resources/upload_file.txt"


@pytest.fixture
def uploaded_file(file_upload):
    """Upload file and return FileUpload page object."""
    file_upload.upload_file(str(file_path))
    return file_upload

@pytest.mark.ui
def test_correct_file_selected(uploaded_file):
    """Verify correct file is selected."""
    uploaded_name = PureWindowsPath(uploaded_file.get_uploaded_file()).name
    assert uploaded_name.lower() == file_path.name.lower()

@pytest.mark.ui
def test_file_upload_success(uploaded_file):
    """Verify file upload is successful."""
    uploaded_file.tap_submit_btn()
    assert uploaded_file.is_file_submitted()

@pytest.mark.ui
def test_error_count_in_file():
    """Verify the number of lines containing the word 'ERROR' in file."""
    expected_errors = 5
    pattern = re.compile(r"\berror\b", re.IGNORECASE)
    with file_path.open() as file:
        num_error_lines = sum(1 for line in file if pattern.search(line))
    assert num_error_lines == expected_errors