from .models import UsersProfiles
from .BearerTokenAuthentication import BearerTokenAuthentication
import uuid


class UserUtils:
    def __profile__(request):
        print("This is the request",request)
        user_data = UserUtils.get_user(request)
        print("My user data", user_data['user_unique_id'])
        return user_data['user_unique_id']

    def get_user(user = None, request = None): 
        if user is None:
            print("true is none")
            is_authenticated, user = BearerTokenAuthentication.authenticate(None,request)
        print("Another user ")
        print(user)
            
        profile=UsersProfiles.objects.filter(user=user).first()
        print("this is profle",profile)
        user_data={
            'user_unique_id':str(profile.user_unique_id),
            'first_name':profile.user.first_name,
            'last_name':profile.user.last_name,
            'username':profile.user.username,
            'email':profile.user.email,
            "user_phone":profile.user_phone
        }

        
        return user_data
    
    def get_forgot_password_token():
        token =  str(uuid.uuid4())
        return token
    
    
