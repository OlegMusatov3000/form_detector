"""
A simple module for handling form templates and validating form data.

This module provides a FormTemplate class with methods for saving form data to
a TinyDB database,
generating field types based on form data, and finding matching templates in
the database.

It also includes utility methods for checking the validity of dates,
phone numbers, and email addresses.

Dependencies:
- tinydb: A lightweight database for Python.
- phonenumbers: A Python library for parsing and validating international
phone numbers.

Usage:
1. Create an instance of FormTemplate with a name and fields.
2. Save the form template using the save() method.
3. Generate field types based on form data using the generate_field_types
method.
4. Find a matching template in the database with the find_matching_template
method.
5. Utilize the is_valid_date, is_valid_phone, and is_valid_email methods
for data validation.
"""
import re
from datetime import datetime

import phonenumbers
from tinydb import TinyDB

db = TinyDB('db.json')


class FormTemplate:
    def __init__(self, name, fields):
        """
        Initializes a FormTemplate object with a name and fields.

        Args:
            name (str): The name of the form template.
            fields (dict): A dictionary representing the fields of the form
            template.
        """
        self.name = name
        self.fields = fields

    def save(self):
        """
        Saves the form template data to the database.
        """
        db.insert({'name': self.name, 'fields': self.fields})

    @staticmethod
    def generate_field_types_from_data(form_data):
        """
        Generates field types based on the provided form data.

        Args:
            form_data (dict): A dictionary representing the form data.

        Returns:
            dict: A dictionary mapping field names to their respective types.
        """
        field_types = {}
        for field_name, field_value in form_data.items():
            if FormTemplate.is_valid_date(field_value):
                field_types[field_name] = 'date'
            elif FormTemplate.is_valid_phone(field_value):
                field_types[field_name] = 'phone'
            elif FormTemplate.is_valid_email(field_value):
                field_types[field_name] = 'email'
            else:
                field_types[field_name] = 'text'
        return field_types

    @staticmethod
    def find_matching_template(form_data):
        """
        Finds a matching template in the database based on the provided form
        data.

        Args:
            form_data (dict): A dictionary representing the form data.

        Returns:
            dict or None: The matching template if found, otherwise None.
        """
        for template in db.all():
            template_fields = template.get('fields', {})
            if all(
                form_data.get(key) == template_fields.get(key) for key in (
                    template_fields
                )
            ):
                print(template)
                return template
        return None

    @staticmethod
    def is_valid_date(value):
        """
        Checks if the provided value is a valid date.

        Args:
            value (str): The value to be checked.

        Returns:
            bool: True if the value is a valid date, False otherwise.
        """
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except Exception:
            try:
                datetime.strptime(value, '%Y.%m.%d')
                return True
            except Exception:
                print(f'Значение {value} не является датой')
                return False

    @staticmethod
    def is_valid_phone(value):
        """
        Checks if the provided value is a valid phone number.

        Args:
            value (str): The value to be checked.

        Returns:
            bool: True if the value is a valid phone number, False otherwise.
        """
        try:
            parsed_number = phonenumbers.parse(value, 'RU')
            if not phonenumbers.is_valid_number(parsed_number):
                return False
        except Exception:
            print(f'Значение {value} не является номером телефона')
            return False
        return True

    @staticmethod
    def is_valid_email(value):
        """
        Checks if the provided value is a valid email address.

        Args:
            value (str): The value to be checked.

        Returns:
            bool: True if the value is a valid email address, False otherwise.
        """
        try:
            email_pattern = re.compile(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            )
            if not bool(email_pattern.match(value)):
                return False
        except Exception:
            print(f'Значение {value} не является электронной почтой')
        return True
