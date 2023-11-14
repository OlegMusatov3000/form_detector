class ValidationException(Exception):
    pass


class EmailValidationException(ValidationException):
    pass


class PhoneValidationException(ValidationException):
    pass


class DateValidationException(ValidationException):
    pass
