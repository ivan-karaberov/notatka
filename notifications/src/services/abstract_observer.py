from abc import ABC, abstractclassmethod

from type import Message


class AbstractMessageObserver(ABC):
    @abstractclassmethod
    async def send_message(self, message: Message):
        """Отправить сообщение"""
        pass


class AbstractMessagePublisher(ABC):
    """
        Интерфейс издателя объявляет набор методов для управлениями подписчиками.
    """

    @abstractclassmethod
    def attach(self, observer: AbstractMessageObserver) -> None:
        """Присоединяет наблюдателя к издателю."""
        pass

    @abstractclassmethod
    def detach(self, observer: AbstractMessageObserver) -> None:
        """Отсоединяет наблюдателя от издателя"""
        pass

    @abstractclassmethod
    async def notify(self, observer_id: str) -> None:
        """Запуск отправки сообщения в конкретном подписчике"""
        pass