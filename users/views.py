from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from globals.decorators import login_required
from globals.request_manager import Action
from frontend.settings import MAIN_URL
from django.contrib.messages import error

class ProfileView(TemplateView) : 
    template_name = 'profile.html'

    @login_required
    def get(self, request, **kwargs) : 
        return render(request, self.template_name)

class LoginView (TemplateView): 
    template_name = 'login.html'

    def post(self, request) : 
        action = Action(url=MAIN_URL + "/user/auth/login/",data={
            **request.POST
        })

        action.post()
        if action.is_valid:
            user = action.json_data()['access_token']
            response = redirect('profile')
            response.set_cookie('user', user)
            return response
        
        error(request,'invalid crediantils')
        return redirect('login')

class RegisterView (TemplateView) : 
    template_name = 'register.html'

    def post (self, request) : 
        action = Action(MAIN_URL + '/user/auth/register/', data={
            **request.POST
        })

        action.post()
        
        if action.is_valid :
            user = action.json_data()['access_token']
            response = redirect('profile')
            response.set_cookie('user', user)
            return response
        
        error(request, action.json_data()['message'][0])
        return redirect('register')

class LogoutView (View) : 
    
    def get (self, request) : 
        response = redirect('login')
        response.delete_cookie('user')
        return response
    

class CreateProductView(TemplateView) : 
    template_name = 'create-product.html'

    @login_required
    def post(self, request, **kwargs) : 
        action = Action(MAIN_URL + '/product/create/',data={**request.POST}, headers=kwargs['headers'])
        action.files = {'image' : request.FILES['image']}
        action.post()
        if action.is_valid:
            return redirect('profile')
        return redirect('create_product')
