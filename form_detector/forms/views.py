import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import FormTemplate


@csrf_exempt
def get_form(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body.decode('utf-8'))
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
