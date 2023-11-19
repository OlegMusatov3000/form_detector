"""
This script is designed to execute 3 test requests with specified parameters
to a given URL. The purpose is to test the functionality of the target
endpoint with different sets of parameters.

Usage:
    python manage.py make_test_requests

The script uses the Django BaseCommand class to create a custom management
command. It performs three POST requests to the specified URL (MAIN_URL) with
the predefined test parameters (TEST_PARAMS_1, TEST_PARAMS_2, TEST_PARAMS_3).
The results of each test are printed to the console.
"""

import requests
from django.core.management.base import BaseCommand
from form_detector_backend.settings import (
    TEST_PARAMS_1, TEST_PARAMS_2, TEST_PARAMS_3, MAIN_URL
)


class Command(BaseCommand):
    help = f'''Команда выполняет 3 тестовых запроса с параметрами:
    {TEST_PARAMS_1}, {TEST_PARAMS_2}, {TEST_PARAMS_3} к url: {MAIN_URL}
    '''

    def handle(self, *args, **kwargs):
        '''
        Executes the main functionality of the script. Iterates through the
        list of test parameters, builds the URL with parameters, performs a
        POST request, and prints the response.
        '''
        test_params_list = [TEST_PARAMS_1, TEST_PARAMS_2, TEST_PARAMS_3]

        for i, test_params in enumerate(test_params_list, start=1):
            url_with_params = self.build_url_with_params(test_params)
            response = self.perform_post_request(url_with_params)
            self.stdout.write(
                self.style.SUCCESS(f'Test {i}: {response.json()}')
            )

    def build_url_with_params(self, params):
        '''
        Builds the URL with the given parameters. Converts the parameters into
        a query string and appends it to the main URL.
        '''
        return (
            f'{MAIN_URL}?'
            f'{"&".join([f"{key}={value}" for key, value in params.items()])}'
        )

    def perform_post_request(self, url):
        '''
        Performs a POST request to the specified URL using the requests
        library and returns the response.
        '''
        response = requests.post(url)
        return response
