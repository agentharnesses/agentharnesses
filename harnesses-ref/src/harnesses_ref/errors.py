class HarnessError(Exception):
    pass


class ValidationError(HarnessError):
    def __init__(self, path: str, message: str):
        self.path = path
        super().__init__(f"{path}: {message}")


class ParseError(HarnessError):
    def __init__(self, path: str, message: str):
        self.path = path
        super().__init__(f"{path}: {message}")
