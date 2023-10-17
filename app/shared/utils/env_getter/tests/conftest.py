import os
import pytest


TEMP_ENV_VARS = {
    '__VAR1': '1',
    '__VAR2': '2',
    '__VAR3': '3',
}

TEMP_ENV_VARS_DESCRIPTIONS = [
    'this is __VAR1',
    'this is __VAR2',
    'this is __VAR3',
]

UNSET_ENV_VARS = [
    '__VAR4'
]

UNSET_ENV_VARS_DESCRIPTIONS = [
    'this is __VAR4'
]


@pytest.fixture()
def temp_env_vars():
    return list(TEMP_ENV_VARS.items())


@pytest.fixture()
def unset_env_vars():
    return list(UNSET_ENV_VARS)


@pytest.fixture()
def temp_env_vars_descriptions():
    return list(TEMP_ENV_VARS_DESCRIPTIONS)


@pytest.fixture()
def unset_env_vars_descriptions():
    return list(UNSET_ENV_VARS_DESCRIPTIONS)


@pytest.fixture(scope="function", autouse=True)
def tests_setup_and_teardown():
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    yield
    os.environ.clear()
    os.environ.update(old_environ)

