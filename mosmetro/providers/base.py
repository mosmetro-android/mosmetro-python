from requests import Response


class Provider:
    def __init__(self, response: Response):
        self.response = response

    def run(self) -> bool:
        raise NotImplementedError()

    @staticmethod
    def match(response: Response):
        raise NotImplementedError()
