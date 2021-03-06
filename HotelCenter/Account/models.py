from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from birthday import BirthdayField, BirthdayManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    avatar = models.ImageField(null=True, blank=True, default=None, upload_to='users')
    firstName = models.CharField(max_length=30, null=True, blank=True, default=None)
    lastName = models.CharField(max_length=30, null=True, blank=True, default=None)

    username = models.CharField(max_length=30, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    birthday = BirthdayField(null=True, blank=True)
    objectsBirthday = BirthdayManager()

    gender = models.CharField(max_length=20, null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    national_code = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    balance = models.PositiveIntegerField(default=0, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




