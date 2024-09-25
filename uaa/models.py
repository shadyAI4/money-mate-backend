from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
from django.utils import timezone


class UsersProfiles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='profile_user', on_delete=models.CASCADE, blank=True)
    user_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    user_phone = models.CharField(default='', max_length=9000, blank=True)
    user_createddate = models.DateField(auto_now_add=True)



    class Meta:
        db_table = 'pesa_user_profiles'
        ordering = ['-primary_key']
        verbose_name_plural = "USER PROFILES"

    def __str__(self):
        return "{}-{}".format(self.user.username, self.user.first_name)




class ForgotPasswordRequestUsers(models.Model):
    primary_key = models.AutoField(primary_key=True)
    request_user = models.ForeignKey(User, related_name='request_profile', on_delete=models.CASCADE)
    request_token = models.CharField(max_length=300, editable=False, default=None)
    request_is_used = models.BooleanField(default=False)
    request_is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'pesa_users_forgot_password_request'
        ordering = ['-primary_key']
        verbose_name_plural = "FORGOT PASSWORD REQUESTS"

    def __str__(self):
        return "{} - {}".format(self.request_user, self.request_token)
    