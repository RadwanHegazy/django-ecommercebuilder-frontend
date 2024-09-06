from django.shortcuts import redirect
from .request_manager import Action
from frontend.settings import MAIN_URL
from django.http import HttpRequest

def login_required (function) : 

    def wrapper (self, request, **kwargs) : 

        user = request.COOKIES.get('user',None)

        if user is None :
            return redirect('login')
        
        action = Action(
            url = MAIN_URL + '/user/profile/',
            headers = {'Authorization':f"Bearer {user}"}
        )

        action.get()
        
        if not action.is_valid : 
            kwargs['headers'] = None
            return redirect('login')
        else:
            kwargs['headers'] = {'Authorization':f"Bearer {user}"}
            kwargs['user'] = action.json_data()
        
        func = function(self,request,**kwargs)

        return func
    
    return wrapper


def tenant_config(func) : 
    def handler(self, request, **kwargs) : 
        host = request.get_host()
        kwargs['has_tenant'] = len(host.split('.')) > 1
        if kwargs['has_tenant'] : 
            kwargs['tenant'] = {
                'name' : host.split('.')[0]
            }

        if kwargs['has_tenant'] : 
            action = Action(
                MAIN_URL + f'/product/get/{kwargs['tenant']['name']}/',
            )
            action.get()

            if action.is_valid :
                kwargs['products'] = action.json_data()
            else:
                kwargs['has_tenant'] = False

        f = func(self, request, **kwargs)
        return f
    return handler