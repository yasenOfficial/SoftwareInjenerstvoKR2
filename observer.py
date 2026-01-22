from abc import ABC, abstractmethod
from datetime import datetime
import random


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


#  Observer Interface 
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: str):
        pass


#  Concrete Observers 
class EmailObserver(Observer):
    def __init__(self, email: str):
        self.email = email

    def update(self, event_type: str, data: str):
        print(
            f"{Style.CYAN}[EMAIL → {self.email}] [{timestamp()}] "
            f"{Style.RESET}{Style.BOLD}{event_type}:{Style.RESET} {data}"
        )


class SmsObserver(Observer):
    def __init__(self, phone: str):
        self.phone = phone

    def update(self, event_type: str, data: str):
        print(
            f"{Style.GREEN}[SMS → {self.phone}] [{timestamp()}] "
            f"{Style.RESET}{Style.BOLD}{event_type}:{Style.RESET} {data}"
        )


class SlackObserver(Observer):
    def __init__(self, username: str):
        self.username = username

    def update(self, event_type: str, data: str):
        print(
            f"{Style.MAGENTA}[Slack @{self.username}] [{timestamp()}] "
            f"{Style.RESET}{Style.BOLD}{event_type}:{Style.RESET} {data}"
        )


#  Subject (Observable) 
class NotificationCenter:
    def __init__(self):
        self._observers: list[Observer] = []
        self.activity_log = []

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event_type: str, message: str):
        log_entry = f"{event_type}: {message}"
        self.activity_log.append(log_entry)

        for observer in self._observers:
            observer.update(event_type, message)

    def random_event(self):
        event_type = random.choice(["INFO", "WARNING", "UPLOAD", "DELETE"])
        file = random.choice(["photo.png", "report.pdf", "data.csv"])
        self.notify(event_type, f"Event triggered for {file}")



if __name__ == "__main__":
    center = NotificationCenter()

    center.subscribe(EmailObserver("john@example.com"))
    center.subscribe(SmsObserver("+359888123456"))
    center.subscribe(SlackObserver("alice"))

    center.notify("UPLOAD", "User uploaded file 'homework.docx'")
    center.notify("DELETE", "User deleted file 'old_photo.jpg'")

    print("\n--- Random events simulation ---\n")
    for _ in range(3):
        center.random_event()
