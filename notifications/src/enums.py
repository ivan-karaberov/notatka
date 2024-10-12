from enum import Enum


class EmailType(Enum):
    confirmation_email = "confirmation_email"
    password_recovery = "password_recovery"