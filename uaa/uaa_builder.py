from .models import UsersProfiles
from .uaa_dto import  UserProfileObject


class UserAccountBuilder:
    
    @staticmethod
    def get_user_profile_data(id):
        try:
            user_profile=UsersProfiles.objects.filter(user_unique_id=id).first()
            print("Im the user now",user_profile)
            return UserProfileObject(
                id = user_profile.primary_key,
                user_unique_id = user_profile.user_unique_id,
                user_first_name = user_profile.user.first_name,
                user_last_name = user_profile.user.last_name,
                user_email = user_profile.user.email,
                user_phone = user_profile.user_phone,
                user_username=user_profile.user.username,
            )
        except Exception as e:
            print("I failed")
            return UserProfileObject()
