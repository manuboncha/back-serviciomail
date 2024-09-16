class EmailProviderSendEmailException(Exception):

    def __init__(self, provider_name: str, status_code: int, error_detail: str) -> None:
        super().__init__(f"{provider_name} failed with status code {status_code}: {error_detail}")
        self.provider_name = provider_name
        self.status_code = status_code
        self.error_detail = error_detail
