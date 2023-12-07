import os

import pytest

from shared.utils.env_getter.env_getter import EnvironmentGetter
from shared.utils.env_getter.errors import EnvironmentVariableNotFound, SeveralEnvironmentVariablesNotFound


def test_get_or_fail_no_error(unset_env_vars):
    name, value = unset_env_vars[0], "aaa"
    os.environ[name] = value
    res = EnvironmentGetter.get_or_fail(name)
    assert res == value


def test_get_or_fail_error(unset_env_vars):
    name, value = unset_env_vars[0], "aaa"
    with pytest.raises(EnvironmentVariableNotFound) as err:
        EnvironmentGetter.get_or_fail(name)


def test_fail_if_missing_no_error(temp_env_vars):
    env_getter = EnvironmentGetter()
    for name, value in temp_env_vars:
        env_getter.get(name, required=True)
    env_getter.fail_if_missing()


def test_fail_if_missing_error(temp_env_vars, unset_env_vars, unset_env_vars_descriptions):
    env_getter = EnvironmentGetter()
    for name, value in temp_env_vars:
        env_getter.get(name, required=True)
    for name, description in zip(unset_env_vars, unset_env_vars_descriptions):
        env_getter.get(name, required=True, description=description)

    with pytest.raises(SeveralEnvironmentVariablesNotFound) as error:
        env_getter.fail_if_missing()
    print(error, flush=True)
    for description in unset_env_vars_descriptions:
        assert description in str(error), f"Description of environment variable not printed in the error"


def test_fail_if_missing_scope_no_error(temp_env_vars):
    env_getter = EnvironmentGetter()
    scope1 = env_getter.scope("Scope 1")
    for name, value in temp_env_vars:
        scope1.get(name, required=True)
    scope2 = env_getter.scope("Scope 2")
    for name, value in temp_env_vars:
        scope2.get(name, required=True)
    env_getter.fail_if_missing()


def test_fail_if_missing_scope_error(temp_env_vars, unset_env_vars, unset_env_vars_descriptions):
    env_getter = EnvironmentGetter()
    scope1 = env_getter.scope("Scope 1")
    scope2 = env_getter.scope("Scope 2")
    for name, value in temp_env_vars:
        scope1.get(name, required=True)
        scope2.get(name, required=True)
    for name, description in zip(unset_env_vars, unset_env_vars_descriptions):
        scope1.get(name, required=True, description=description)
        scope2.get(name, required=True, description=description)

    with pytest.raises(SeveralEnvironmentVariablesNotFound) as error:
        env_getter.fail_if_missing()
    print(error, flush=True)
    for description in unset_env_vars_descriptions:
        assert\
            str(error).count(description) >= 2,\
            f"Description of environment variable not printed in the error in both scopes"
