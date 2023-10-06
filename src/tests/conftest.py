from pathlib import Path

import pytest

from tests.utils import TEST_TEMP_DIR, recreate_folder


@pytest.fixture(scope="session")
def shared_test_dir() -> Path:
    return recreate_folder(TEST_TEMP_DIR)


@pytest.fixture()
def tmp_test_dir(request, shared_test_dir) -> Path:
    return recreate_folder(shared_test_dir / request.node.name)
