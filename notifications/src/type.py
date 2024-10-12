from enum import Enum
from dataclasses import dataclass


class ChannelType(Enum):
    email = "email"


class MessageType(Enum):
    confirmation_email = "confirmation_email"
    password_recovery = "password_recovery"


@dataclass
class Message:
    recipient: str
    recipient_name: str
    message: str
    message_type: MessageType