import json
from django.http import JsonResponse
from django.core.validators import MinValueValidator
from django.views.decorators.csrf import csrf_exempt
from .models import FormTemplate


@csrf_exempt
def get_form(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body.decode('utf-8'))
            print(form_data)
            matching_template = FormTemplate.find_matching_template(form_data)
            if matching_template:
                return JsonResponse({'template_name': matching_template.name})
            else:
                return JsonResponse(generate_field_types(form_data))
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def generate_field_types(form_data):
    field_types = {}
    for field_name, field_value in form_data.items():
        if FormTemplate.validate_date(field_value):
            field_types[field_name] = 'date'
        elif FormTemplate.validate_phone(field_value):
            field_types[field_name] = 'phone'
        elif FormTemplate.validate_email(field_value):
            field_types[field_name] = 'email'
        else:
            field_types[field_name] = 'text'
    return field_types
