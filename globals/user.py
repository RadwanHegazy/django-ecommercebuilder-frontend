from .request_manager import Action
from frontend.settings import MAIN_URL

def userTemp (request) : 

    context = {}
    user = request.COOKIES.get('user',None)
    
    if user is not None :
        headers = {'Authorization':f"Bearer {user}"}
        action = Action(
            url = MAIN_URL + '/user/profile/',
            headers=headers
        )
        action.get()
        if action.is_valid : 
            context['c_user'] = action.json_data()
    context['main_url'] = MAIN_URL
            
    return context