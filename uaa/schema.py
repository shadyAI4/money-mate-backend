from datetime import timezone
import graphene
from graphene import ObjectType
from django.contrib.auth.models import User, AbstractUser

from .models import UsersProfiles
from .uaa_builder import UserAccountBuilder
from response.Response import ResponseObject
from .uaa_dto import UserObjectProfile, UserFilteringInputObject, ProfileResponseObject
from django.db.models import Q
from django.core.paginator import Paginator
from .UserUtils import UserUtils


class Query(ObjectType): 
    print("it reach heere")
    get_users = graphene.Field(ProfileResponseObject,filtering=UserFilteringInputObject())
    get_user_profile = graphene.Field(ProfileResponseObject)
    data= graphene.List(UserObjectProfile)
    

    def resolve_get_user_profile(self, info,**kwargs):
        print(info.context.user)
        print("Here it work")
        user_unique_id = UserUtils.__profile__(info.context.user)
        print("But here it not work")
        profile=UsersProfiles.objects.filter(user_unique_id=user_unique_id).first()
        
        if profile is None:
            return self(response=ResponseObject.get_response(id="20"))
        user_object=UserAccountBuilder.get_user_profile_data(profile.user_unique_id)
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"),data=user_object)
    
    def resolve_get_all_users(self,info,*args, **kwargs):
        users = UsersProfiles.objects.all()
        print(users)
        return self(response = ResponseObject.get_response(id="21"),data = users)
        

    





