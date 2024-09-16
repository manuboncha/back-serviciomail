class EmailNotFoundException(Exception):

    def __init__(self, email_id) -> None:
        super().__init__(f"Email with ID {email_id} not found.")
        self.email_id = email_id
