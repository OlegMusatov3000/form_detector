from forms.models import FormTemplate


def populate_database():
    template_data = {
        'name': 'MyForm',
        'fields': {
            'email': 'd@a.w',
            'phone': '+78005553535',
            'date': '11.08.1997',
            'text': 'dsvcsd'
        }
    }

    # Создаем экземпляр FormTemplate и сохраняем его
    form_template = FormTemplate(**template_data)
    form_template.save()


if __name__ == '__main__':
    populate_database()
