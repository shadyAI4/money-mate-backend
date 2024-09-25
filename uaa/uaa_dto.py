import graphene

from .models import UsersProfiles
from response.Response import ResponseObject


class UserInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    user_username = graphene.String()
    user_phone = graphene.String()


class UserRegistrationInputObject(graphene.InputObjectType):
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    user_username = graphene.String()
    user_phone = graphene.String()
    password = graphene.String()
    confirm_password = graphene.String()
    
class UserObject(graphene.ObjectType):
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    user_username=graphene.String()

class UserObjectProfile(graphene.ObjectType):
    id = graphene.String()
    user_unique_id = graphene.String()
    user_phone = graphene.String()
    user_createddate = graphene.String()
    user=graphene.Field(UserObject)

class UserProfileObject(graphene.ObjectType):
    id = graphene.String()
    user_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    user_phone = graphene.String()
    user_username=graphene.String()

class ProfileResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)



class UserFilteringInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()


class ChangePasswordInputObject(graphene.InputObjectType):
    current_password = graphene.String()
    password_1 = graphene.String()
    password_2 = graphene.String()

class ForgotPasswordInputObject(graphene.InputObjectType):
    token = graphene.String(required=True)
    password_1 = graphene.String()
    password_2 = graphene.String()



