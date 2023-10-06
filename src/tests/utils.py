import os
import shutil
from os import pardir, path
from pathlib import Path

REPO_DIR = Path(path.abspath(path.join(__file__, pardir, pardir, pardir)))

TESTDATA_DIR = REPO_DIR / "testdata"
TEST_TEMPLATES_DIR = TESTDATA_DIR / "templates"
TEST_TEMP_DIR = REPO_DIR / "test-run-result"


def recreate_folder(folder: Path):
    if folder.exists():
        shutil.rmtree(folder)

    os.makedirs(folder)
    return folder
