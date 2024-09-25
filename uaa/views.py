import datetime
import graphene
from graphene_federation import build_schema
# from nircmis_uaaa_utils.EmailUtils import EmailNotifications

from .uaa_dto import  ForgotPasswordInputObject, UserInputObject, UserProfileObject, ChangePasswordInputObject, UserRegistrationInputObject
from response.Response import ResponseObject

from django.contrib.auth.models import User
from .models import ForgotPasswordRequestUsers, UsersProfiles

from .uaa_builder import UserAccountBuilder
from .UserUtils import UserUtils


class RegisterUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserRegistrationInputObject(required=True)
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self,root, info, input):
        if input.password != input.confirm_password:
            self(response=ResponseObject.get_response(id="30"))
        if input.password == input.confirm_password:
            user = User.objects.create(
                first_name=input.user_first_name,
                last_name=input.user_last_name,
                username=input.user_username,
                email=input.user_email,
                
                password = input.password,
            )


            user_profile = UsersProfiles.objects.create(
                user=user,
                user_phone =input.user_phone,
            )
            return self(response=ResponseObject.get_response(id="2"))

class UpdateUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)

    @classmethod
    # @has_mutation_access(permissions=['can_manage_settings'])
    def mutate(self, root, info,  input):
        profile = UsersProfiles.objects.filter(profile_unique_id=input.user_unique_id).first()

        if profile is None:
            return self(response=ResponseObject.get_response(id="1"), data=None)

        profile.user_phone = input.user_phone
        profile.save()

        profile.user.first_name = input.user_first_name
        profile.user.last_name = input.user_last_name
        profile.user.email = input.user_email
        profile.user.save()
        
        response_body = UserAccountBuilder.get_user_profile_data(id=profile.profile_unique_id)

        return self(response=ResponseObject.get_response(id="2"), data=response_body)
  
class Mutation(graphene.ObjectType):
    register_user_mutation = RegisterUsersMutation.Field()
    update_users_mutation = UpdateUsersMutation.Field()
    

    

schema = build_schema(Mutation, types=[])

