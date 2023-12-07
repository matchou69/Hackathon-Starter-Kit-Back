class HelloWorldService:
    @staticmethod
    def is_greeting(value: str) -> bool:
        value_lowercase = value.lower()
        return "hello" in value_lowercase
