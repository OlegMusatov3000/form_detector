"""
This module defines Django views related to handling form data.

Functions:
    - get_form(request): A view function for processing form data. It supports
    POST requests with JSON-formatted data.
        It extracts form data from the request, generates field types using
        the FormTemplate model, and finds a matching
        template. If a match is found, it returns the template name; otherwise,
        it returns the processed form data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing either the template name
            or processed form data.

        Raises:
            JsonResponse: If there is an error in decoding JSON or any other
            unexpected exception, an error response
            with relevant information is returned.

        Note:
            This view is decorated with '@csrf_exempt' to bypass CSRF
            protection for demonstration purposes. In a production environment,
            proper CSRF protection should be applied.
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import FormTemplate


@csrf_exempt
def get_form(request):
    if request.method == 'POST':
        try:
            form_data = request.GET.dict()
            form_data = FormTemplate.generate_field_types_from_data(form_data)
            matching_template = FormTemplate.find_matching_template(form_data)
            if matching_template:
                return JsonResponse(
                    {'template_name': matching_template.get('name')}
                )
            else:
                return JsonResponse(form_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
