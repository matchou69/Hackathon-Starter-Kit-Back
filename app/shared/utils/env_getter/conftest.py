import os
import pytest


TEMP_ENV_VARS = {
    '__VAR1': '1',
    '__VAR2': '2',
    '__VAR3': '3',
}

@pytest.fixture(scope="module")
def temp_vars():
    return list(TEMP_ENV_VARS.items())

@pytest.fixture(scope="module", autouse=True)
def tests_setup_and_teardown():
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    yield
    os.environ.clear()
    os.environ.update(old_environ)

