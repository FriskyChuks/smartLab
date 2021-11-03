from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Group
)

GENDER = (
		('male', 'Male'),
		('female', 'Female'),
	)

class UserManager(BaseUserManager):
    def create_user(self, username, first_name=None, last_name=None, email=None, password=None, is_staff=False, is_admin=False, is_active=True, is_patient=False):
        if not first_name:
            raise ValueError("User must have firstname!")
        if not last_name:
            raise ValueError("User must have lastname!")
        if not username:
            raise ValueError("User must have a username!")
        if not password:
            raise ValueError("Users must have password!")

        user_obj = self.model(
            username = username,
            email =self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.is_a_patient = is_patient
        user_obj.save(using=self._db)
        return user_obj


    def create_staff(self, username, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(
            username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True
        )
        return user


    def create_superuser(self, username, first_name=None, last_name=None, password=None):
        user = self.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user



class User(AbstractBaseUser):
    image           = models.ImageField(null=True, blank=True, upload_to="users/")
    first_name		= models.CharField(max_length=225)
    last_name		= models.CharField(max_length=225)
    other_names		= models.CharField(max_length=225, blank=True, null=True)
    email 			= models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username		= models.CharField(max_length=225, unique=True)
    phone1          = models.CharField(max_length=11)
    gender          = models.CharField(max_length=10, choices=GENDER)
    active 			= models.BooleanField(default=True)
    staff 			= models.BooleanField(default=False)
    is_a_patient	= models.BooleanField(default=False)
    admin			= models.BooleanField(default=False)
    group 			= models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    timestamp 		= models.DateTimeField(auto_now_add=True, auto_now=False)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)
    
    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
