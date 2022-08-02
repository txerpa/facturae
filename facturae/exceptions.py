class FacturaeError(Exception):
    """Base class for all Facturae exceptions."""

    def __init__(self, message, *args):
        self.message = message
        super().__init__(self.message, *args)

    def __str__(self):
        return repr(self.message)


class FacturaeValidationError(FacturaeError):
    pass


class FacturaeSignError(FacturaeError):
    pass


class VersionNotFound(FacturaeError):
    """File version not found"""

    def __init__(self, e, msg=None):
        self.original_error = e
        self.msg = msg or f"Version not found in XML - {str(e)}"
        super().__init__(self.msg, self.original_error)


class AccountantValidation(FacturaeError):
    def __init__(self, msg):
        self.msg = f"Accountant Validation - {msg}"
        super().__init__(self.msg)
