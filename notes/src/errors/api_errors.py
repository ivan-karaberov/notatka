from fastapi import status


class APIException(Exception):
    status_code = None
    detail = None

    def __str__(self):
        return f"{self.detail}"
    

class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail="Invalid token error"


class TokenExpiredException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Token has expired"


class NoteNotSavedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Note not saved"


class UserNotHavePermissions(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User does not have permissions"


class NoteNotFoundException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Note not found"


class NoteNotUpdatedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    deatil = "Note not updated"


class NoteNotDeletedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Note not deleted"


class ReceivingTokenException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An error occurred when receiving the token"