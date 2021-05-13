"""Project utilities."""
from zipfile import ZipFile


def extract_zip_file(file_path: str, output_path: str) -> None:
    """Extract files from zip files."""
    with ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(path=output_path)
