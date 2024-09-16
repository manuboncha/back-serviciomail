class EmailProviderNotFoundConfigException(Exception):

    def __init__(self, provider_name: str) -> None:
        super().__init__(f"Email Provider {provider_name} does not have apy_key configured.")
        self.provider_name = provider_name
