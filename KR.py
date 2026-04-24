class Notification:
    def __init__(self, message: str):
        self.message = message


class EmailNotification(Notification):
    def __init__(self, message: str, email: str):
        super().__init__(message)
        self.email = email

    def process(self):
        print(f"Email на {self.email}: {self.message}")


class SMSNotification(Notification):
    def __init__(self, message: str, phone: str):
        super().__init__(message)
        self.phone = phone

    def process(self):
        print(f"SMS на {self.phone}: {self.message}")
items = [EmailNotification("Привет", "a@b.com"),
         SMSNotification("Пока", "+79001234567")]
for item in items:
    item.process()

