import os
from collections import defaultdict
from typing import List, Dict
from uuid import uuid4

from .errors import OneVariableErrorData, EnvironmentVariableNotFound, EnvironmentErrorData, \
    SeveralEnvironmentVariablesNotFound


class EnvironmentGetter:
    class Scope:
        def __init__(self, env_getter: 'EnvironmentGetter', description: str):
            self.env_getter = env_getter
            self.description = description
            self.uuid = uuid4()

        def __hash__(self):
            return hash(self.uuid)

        def get(self, variable_name, description=None, required=False):
            return self.env_getter.get(variable_name, required=required, description=description, _scope=self)

    def __init__(self):
        self.variables: List[str] = []
        self.required_list: List[bool] = []
        self.values: List[str | None] = []
        self.descriptions: List[str | None] = []
        self.scopes: Dict[int, EnvironmentGetter.Scope] = dict()
        self.size = 0

    def get(self, variable_name, description=None, required=True, _scope: Scope | None = None) -> str:
        value = os.getenv(variable_name)
        self.variables.append(variable_name)
        self.required_list.append(required)
        self.values.append(value)
        self.descriptions.append(description)

        if _scope is not None:
            self.scopes[self.size] = _scope
        self.size += 1

        return value

    @staticmethod
    def get_or_fail(variable_name, description=None) -> str:
        value = os.getenv(variable_name)
        if value is None:
            raise EnvironmentVariableNotFound(variable_name, description)
        return value

    def fail_if_missing(self):
        def filter_errors(x):
            i, (variable, required, value, description) = x
            return required and (value is None)

        error_items = list(filter(
            filter_errors,
            enumerate(zip(self.variables, self.required_list, self.values, self.descriptions))
        ))
        if len(error_items) == 0:
            return

        errors_scoped_dict: defaultdict[EnvironmentGetter.Scope, List[OneVariableErrorData]] = defaultdict(list)
        errors_not_scoped: List[OneVariableErrorData] = []
        for i, (variable, required, value, description) in error_items:
            variable_error: OneVariableErrorData = {
                "variable": variable,
                "description": description
            }
            if i in self.scopes:
                errors_scoped_dict[self.scopes[i]].append(variable_error)
            else:
                errors_not_scoped.append(variable_error)
        errors: EnvironmentErrorData = {
            "errors_scoped": [{
                "scope_description": scope.description,
                "variables": variable_errors
            } for scope, variable_errors in errors_scoped_dict.items()],
            "errors_not_scoped": errors_not_scoped
        }

        raise SeveralEnvironmentVariablesNotFound(errors)

    def scope(self, description: str):
        return EnvironmentGetter.Scope(self, description)
