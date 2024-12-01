from django.shortcuts import render
from django.views import View 
from .forms import FilterForm
from .models import (
    Product, 
    Category, 
    Brand, 
    ProductPhoto,
)


class CatalogView(View): 
    template_name = 'products/catalog.html'

    def get(self, request): 
        form = FilterForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data

            products = Product.objects.all()
            
            selected_category = cd.get('category')
            if selected_category: 
                products = products.filter(category=selected_category)

            selected_sorting = cd.get('sorting')
            if selected_sorting: 
                match selected_sorting: 
                    case FilterForm.SortingChoices.NEWEST: 
                        products = products.order_by('created_at')
                    case FilterForm.SortingChoices.PRICE_ASC: 
                        products = products.order_by('price')
                    case FilterForm.SortingChoices.PRICE_ASC: 
                        products = products.order_by('-price') 

        context = {
            'form': form,
            'products': products,
        }
        return render(request, self.template_name, context)
