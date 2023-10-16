import os

from shared.utils.env_getter.env_getter import EnvironmentGetter


def test_get_or_fail_no_error(temp_vars):
    env_getter = EnvironmentGetter()
    VAR_NAME = "__VAL1"
    os.environ[VAR_NAME] = "a"
    value = env_getter.get_or_fail(VAR_NAME)
    assert value == "a"


def test_get_or_fail_error():
    env_getter = EnvironmentGetter()
    VAR_NAME = "__VAL1"
    # os.environ[VAR_NAME] = "a"
    value = env_getter.get_or_fail(VAR_NAME)
    assert value == "a"
