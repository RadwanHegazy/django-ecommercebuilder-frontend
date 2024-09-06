from django.shortcuts import render
from django.views import View
from globals.decorators import tenant_config
from django.http import Http404

class IndexView (View) : 

    @tenant_config
    def get(self, request, has_tenant, **kwargs) : 
        if not has_tenant : 
            raise Http404(request)
        
        context = {
            **kwargs
        }
        print(context)
        return render(request, 'home.html', context)
