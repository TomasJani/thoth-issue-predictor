from zipfile import ZipFile, Path


def extract_zip_file(file_path: Path, output_path: Path) -> None:
    """Extract files from zip files.

    :param file_path: Path where the zip file is locally stored.
    """
    with ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(path=output_path)
