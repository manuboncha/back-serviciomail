class Email:

    def __init__(self, to: str, subject: str, body: str, id: int = None) -> None:
        self.id = id
        self.to = to
        self.subject = subject
        self.body = body
