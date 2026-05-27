import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


# Keep an original snapshot to restore before each test
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities to a fresh copy before each test
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)
