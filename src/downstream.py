class SecretSendingException(Exception):
    """An exception we don't want clients to see."""


class PublicSendingException(Exception):
    """An exception we want to pass on to clients."""


class SendingService:
    @staticmethod
    def downstream_service_secret_exception():
        raise SecretSendingException("API Key invalid")

    @staticmethod
    def downstream_service_public_exception():
        raise PublicSendingException("Message too long")
