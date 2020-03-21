import http


class CustomHTTPException(Exception):
    def __init__(self, status_code: int, detail: list = None) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
