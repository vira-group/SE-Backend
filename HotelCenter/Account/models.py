from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self,adminpannel=False ,*args, **kwargs):
        
            email=kwargs.get('email')
            password=kwargs.get('password')
            
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email)
            )

            user.set_password(password)
            user.role=kwargs.get('role','C')
            user.phone_number=kwargs.get('phone_number',"")
            user.save(using=self._db)
            
            if user.role == "M":
                    manager=Manager(user=user,name=f"Manager{user.pk}")
                    manager.save()
            elif user.role=="C":
                    customer=Customer(user=user,first_name=f"cutomer{user.pk}",last_name=f"customer_last_name")
                    customer.save()
            else :
                    raise ValueError("Value is invalid!")
            
            
            return user
        
    def super_user(self,eamil,password):
            
            email=eamil
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email)
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
            

    def create_superuser(self, email, password=None):
    
        user = self.super_user(
            email,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    
    
    
    role_manager='M'
    role_customer='C'
    role_unknown='U'
    
    ROLE_CHOICES=[
        (role_manager,'Manager'),
        (role_customer,'Customer'),
        (role_unknown,'Unkown'),
    ]
    
    valid_number=[RegexValidator(regex='^(\+98|0)?9\d{9}$')]
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects = UserManager()
    phone_number = models.CharField(_('phone number'),max_length=11,validators=valid_number,blank=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    role=models.CharField(max_length=1,choices=ROLE_CHOICES,default=role_unknown)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    
    
class Customer(models.Model):

        male_gender ="M"
        female_gender ="F"
        other_gender ="O"
    
        sexuality_choises = [
            ("M","Male",),
            ("F","Female",),
            ("O","Other",)
        ]
        user=models.OneToOneField(User,on_delete=models.CASCADE)     
        valid_id=[RegexValidator(regex='^[0-9]{10}')]
        first_name=models.CharField(max_length=55)
        last_name=models.CharField(max_length=55)
        national_code = models.CharField(max_length=10,validators=valid_id,blank=True)
        gender = models.CharField(max_length=1,choices=sexuality_choises,default=male_gender)
        
        
        
        def __str__(self):
            return f"{self.last_name}"+" "+f"{self.first_name}"


class Manager(models.Model):
    
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)     
    name=models.CharField(max_length=55)
    
    def __str__(self):
            return self.name
    



