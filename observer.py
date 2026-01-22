
from abc import ABC, abstractmethod


#  Observer Interface 
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


#  Concrete Observers 
class EmailObserver(Observer):
    def update(self, message: str):
        print(f"[Email] Received update: {message}")


class SmsObserver(Observer):
    def update(self, message: str):
        print(f"[SMS] Received update: {message}")


#  Subject (Observable) 
class NotificationCenter:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)


#  Example Usage 
if __name__ == "__main__":
    center = NotificationCenter()

    email_user = EmailObserver()
    sms_user = SmsObserver()

    center.subscribe(email_user)
    center.subscribe(sms_user)

    center.notify("New file uploaded!")
