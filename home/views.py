from django.shortcuts import render
from django.views import View 
from contacts.forms import RequestForm


class HomeView(View): 
    template_name = 'home/home.html' 

    def get(self, request): 
        form = RequestForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
