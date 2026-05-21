import pytest
import copy
import importlib


app_module = importlib.import_module("src.app")


def _clone_activities():
    return copy.deepcopy(app_module.activities)


def _restore_activities(original):
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture(autouse=True)
def reset_activities():
    original = _clone_activities()
    yield
    _restore_activities(original)
