from fastapi import status


class APIException(Exception):
    status_code = None
    detail = None

    def __str__(self):
        return f"{self.detail}"


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="User already exists."


class UsernameAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Username already exists."


class EmailAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="Email already exists."


class UserAlreadyLinkedEmailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail="User already linked email attached."


class UnauthorizedUserException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail="No rights to perform this action"


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail="Invalid token error"


class TokenExpiredException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Token has expired"


class InvalidRefreshTokenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Invalid refresh token"


class ConfirmationCodeIncorrectException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid confirmation code"


class ConfirmationCodeAlreadySentException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Сonfirmation code already sent"


class EmailNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Email not found"