import re
from datetime import datetime

from tinydb import TinyDB
import phonenumbers

from .exceptions import (
    ValidationException, EmailValidationException,
    PhoneValidationException, DateValidationException
)

db = TinyDB('db.json')


class FormTemplate:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def save(self):
        # if self.validate_fields(self.fields):
        db.insert({'name': self.name, 'fields': self.fields})
        print("✅ Data saved successfully!")

    @staticmethod
    def find_matching_template(form_data):
        for template in db.all():
            # print(template)
            template_fields = template.get('fields', {})
            # print(template_fields)
            if all(form_data.get(key) == template_fields.get(key) for key in template_fields):
                print(template)
                return template
        return None

    # def validate_fields(self, data):
    #     validators = {
    #         'email': self.is_valid_email(),
    #         'phone': self.is_valid_phone(),
    #         'date': self.is_valid_date(),
    #     }

    #     for key, validator_func in validators.items():
    #         try:
    #             if key in data and not validator_func():
    #                 raise ValidationException(f"❌ Validation failed for {key}")
    #         except EmailValidationException as e:
    #             print(f"❌ Email Validation error: {e}")
    #             return False
    #         except PhoneValidationException as e:
    #             print(f"❌ Phone Validation error: {e}")
    #             return False
    #         except DateValidationException as e:
    #             print(f"❌ Date Validation error: {e}")
    #             return False
    #         except ValidationException as e:
    #             print(f"❌ Validation error: {e}")
    #             return False

    #     return True

    def is_valid_date(value):
        try:
            # print(value)
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except Exception:
            try:
                datetime.strptime(value, '%Y.%m.%d')
                return True
            except Exception:
                return False

    def is_valid_phone(value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                return False
        except Exception:
            return False
        return True

    def is_valid_email(value):
        try:
            email_pattern = re.compile(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            )
            if not bool(email_pattern.match(value)):
                return False
        except Exception:
            return False
        return True
