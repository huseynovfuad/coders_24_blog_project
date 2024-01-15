from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField()
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "mobile"]

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "User"
        verbose_name_plural = "User"


    def __str__(self):
        if self.email:
            return self.email
        return str(self.mobile)