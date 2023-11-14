# main_file.py
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
        if self.validate_fields(self.fields):
            db.insert({'name': self.name, 'fields': self.fields})
            print("✅ Data saved successfully!")

    @staticmethod
    def find_matching_template(form_data):
        for template in db.all():
            template_fields = template.get('fields', {})
            if all(form_data.get(key) == template_fields.get(key) for key in template_fields):
                return template
        return None

    def validate_fields(self, data):
        validators = {
            'email': self.is_valid_email,
            'phone': self.is_valid_phone,
            'date': self.is_valid_date,
        }

        for key, validator_func in validators.items():
            try:
                if key in data and not validator_func():
                    raise ValidationException(f"❌ Validation failed for {key}")
            except EmailValidationException as e:
                print(f"❌ Email Validation error: {e}")
                return False
            except PhoneValidationException as e:
                print(f"❌ Phone Validation error: {e}")
                return False
            except DateValidationException as e:
                print(f"❌ Date Validation error: {e}")
                return False
            except ValidationException as e:
                print(f"❌ Validation error: {e}")
                return False

        return True

    def is_valid_email(self):
        email_pattern = re.compile(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        )
        if not bool(email_pattern.match(self.fields.get('email'))):
            raise EmailValidationException("❌ Invalid email format")
        return True

    def is_valid_phone(self):
        try:
            parsed_number = phonenumbers.parse(self.fields.get('phone'), None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise PhoneValidationException("❌ Invalid phone number")
            return True
        except phonenumbers.NumberParseException as e:
            print(e)
            raise PhoneValidationException("❌ Error parsing phone number")

    def is_valid_date(self):
        try:
            datetime.strptime(self.fields.get('date'), '%d.%m.%Y')
            return True
        except ValueError:
            try:
                datetime.strptime(self.fields.get('date'), '%Y.%m.%d')
                return True
            except ValueError:
                raise DateValidationException("❌ Invalid date format")
