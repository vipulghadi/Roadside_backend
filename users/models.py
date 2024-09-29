
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models, transaction
import uuid



class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given phone_number must be set')
        try:
            with transaction.atomic():
                user = self.model(phone_number=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise 

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_roles=(
        ('admin','admin'),
        ('superadmin','superadmin'),
        ('user','user'),
        ('vendor','vendor')
        
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role=models.CharField(max_length=25,choices=user_roles,default="user")
    username= models.CharField(null=True,blank=True, unique=True,max_length=20)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_deleted= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_google_signin= models.BooleanField(default=False)
    is_phoneno_verified=models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
 
    class Meta:
        ordering = ['-created_at']
        
class ManagementConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Management Configs'

    def update_token(token, key):
        try:
            inst = ManagementConfig.objects.get(key = key)
        except ManagementConfig.DoesNotExist:
            return None
        inst.value = token
        inst.save()
        return inst
    
    def get_instance_by_key(key):
        try:
            inst = ManagementConfig.objects.get(key = key)
            return inst
        except ManagementConfig.DoesNotExist:
            return None