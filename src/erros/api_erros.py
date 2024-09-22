from fastapi import status


class APIException(Exception):
    status_code = None
    detail = None

    def __str__(self):
        return f"{self.detail}"


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="User already exists."
