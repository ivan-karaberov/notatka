class APIException(Exception):
    status_code = None
    detail = None

    def __str__(self):
        return f"{self.detail}"