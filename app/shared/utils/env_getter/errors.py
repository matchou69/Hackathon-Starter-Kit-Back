from typing import List, TypedDict


class OneVariableErrorData(TypedDict):
    variable: str
    description: str | None


class OneScopeErrorData(TypedDict):
    scope_description: str
    variables: List[OneVariableErrorData]


class EnvironmentErrorData(TypedDict):
    errors_scoped: List[OneScopeErrorData]
    errors_not_scoped: List[OneVariableErrorData]


class EnvironmentVariableNotFound(Exception):
    def __init__(self, variable: str, description: str | None):
        message = f"Missing required environment variable named {variable}"
        if description is not None:
            message += f": {description}"
        super().__init__(message)


class SeveralEnvironmentVariablesNotFound(Exception):
    @staticmethod
    def _format_one_error(err: OneVariableErrorData) -> str:
        message_one = "- " + err["variable"]
        if err["description"] is not None:
            message_one += f": {err['description']}"
        return message_one

    @staticmethod
    def _format_list_error(variable_errors: List[OneVariableErrorData]) -> str:
        message = "\n".join(
            SeveralEnvironmentVariablesNotFound._format_one_error(err)
            for err in variable_errors
        )
        return message

    def __init__(self, errors: EnvironmentErrorData):
        message = f"One or several environment variables are missing.\n"
        if len(errors["errors_not_scoped"]) > 0:
            message += SeveralEnvironmentVariablesNotFound._format_list_error(errors["errors_not_scoped"]) + "\n"
            message += "\n"

        if len(errors["errors_scoped"]) > 0:
            for scope_error in errors["errors_scoped"]:
                message += "Environment scope: " + scope_error["scope_description"] + "\n"
                message += SeveralEnvironmentVariablesNotFound._format_list_error(scope_error["variables"]) + "\n"
                message += "\n"

        super().__init__(message)
