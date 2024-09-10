from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid


class PersonManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        person = self.model(username=username,
                            email=self.normalize_email(email),
                            **extra_fields)
        person.set_password(password)
        person.save(using=self._db)

        return person

    def create_superuser(self, username, email, password=None, **extra_fields):
        person = self.create_user(username, email, password)
        person.is_staff = True
        person.is_superuser = True
        person.save(using=self.db)

        return person


class Person(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
