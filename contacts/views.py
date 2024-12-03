from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from home.models import CompanyEmail
from .forms import RequestForm
from .services import send_email


class SaveRequestView(View): 
    def post(self, request): 
        print('Пост запрос')
        form: RequestForm = RequestForm(request.POST) 
        if form.is_valid(): 
            new_request = form.save() 
            
            recipient = CompanyEmail.get_instance().email
            subject = f'Заявка от {new_request.phone}'
            content = (
                f'Номер телефона: {new_request.phone}'
                f'\nИмя: {new_request.name}'
            )

            print(form.data)
            print(recipient)
            print(subject)
            print(content)
            
            send_email(
                recipient=recipient, 
                subject=subject, 
                content=content 
            )

            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'})