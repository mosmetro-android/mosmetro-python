from requests import Response


class Result:
    def __init__(self, success: bool):
        self.success = success


class Redirect(Result):
    def __init__(self, url: str):
        super().__init__(True)
        self.url = url


class Provider:
    def __init__(self, response: Response):
        self.response = response

    def run(self) -> Result:
        raise NotImplementedError()

    @staticmethod
    def match(response: Response):
        raise NotImplementedError()
