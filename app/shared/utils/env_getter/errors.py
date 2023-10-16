from typing import List, TypedDict

from errors import CustomError


class OneVariableErrorDict(TypedDict):
    variable: str
    description: str | None


class OneScopeErrorDict(TypedDict):
    scope_description: str
    variables: List[OneVariableErrorDict]


class EnvironmentErrorDict(TypedDict):
    errors_scoped: List[OneScopeErrorDict]
    errors_not_scoped: List[OneVariableErrorDict]


class EnvironmentVariableNotFound(CustomError):
    def __init__(self, variable: str, description: str | None):
        message = f"Missing required environment variable named {variable}"
        if description is not None:
            message += f": {description}"
        super(message)


class SeveralEnvironmentVariablesNotFound(CustomError):
    @staticmethod
    def _format_one_error(err: OneVariableErrorDict) -> str:
        message_one = err["variable"]
        if err["description"] is not None:
            message_one += f": {err['description']}"
        return message_one

    @staticmethod
    def _format_list_error(variable_errors: List[OneVariableErrorDict]) -> str:
        message = "\n".join(
            SeveralEnvironmentVariablesNotFound._format_one_error(err)
            for err in variable_errors
        )
        return message

    def __init__(self, errors: EnvironmentErrorDict):
        message = f"One or several environment variables are missing.\n"
        if len(errors["errors_not_scoped"]) > 0:
            message += SeveralEnvironmentVariablesNotFound._format_list_error(errors["errors_not_scoped"]) + "\n"

        if len(errors["errors_scoped"]) > 0:
            for scope_error in errors["errors_scoped"]:
                message += "---"
                message += "Error scope: " + scope_error["scope_description"] + "\n"
                message += "---"
                message += SeveralEnvironmentVariablesNotFound._format_list_error(scope_error["variables"]) + "\n"

        super(message)

