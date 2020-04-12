from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, is_staff=False, is_superuser=False):
        if not email or not password:
            raise ValueError("User must have an email address and a password")
        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)  # we change the password the same way
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self.db)
        return user_obj

    def create_superuser(self, email, password, first_name="name", last_name="surname"):
        user_obj = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True
        )
        return user_obj


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, null=False, unique=True)
    first_name = models.CharField(max_length=255, null=False, default="name")
    last_name = models.CharField(max_length=255, null=False, default="surname")
    telephone = models.CharField(max_length=15, null=True)
    is_job_seeker = models.BooleanField(null=False, default=True)
    is_employee = models.BooleanField(null=False, default=False)
    description = models.TextField(null=True)

    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff, but not superuser, # for django auth app
    is_superuser = models.BooleanField(default=False)  # superuser, admin
    date_joined = models.DateTimeField(auto_now_add=True, null=True)  # date of creation account, automatic

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # ex ['first_name'] #py manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):  # for django auth app
        return True

    @staticmethod
    def has_module_perms(app_label):  # for django auth app
        return True

    # examples:


#   def get_first_name(self):
#       return self.first_name

#   def get_last_name(self):
#       return self.last_name

#   @property
#   def is_superuser_(self):
#       return self.is_superuser


class Country(models.Model):
    name = models.CharField(
        max_length=30,
        null=False
    )

    def __str__(self):
        return self.name


class City(models.Model):
    id_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(
        max_length=30,
        null=False
    )

    def __str__(self):
        return self.name


class JobOffer(models.Model):
    name = models.CharField(
        max_length=30,
        null=False
    )
    id_employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    company = models.CharField(
        max_length=30,
        null=True
    )

    id_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True
    )

    full_time = models.BooleanField(
        null=False,
        default=True
    )

    remote = models.BooleanField(
        null=False,
        default=False
    )

    description = models.TextField(
        null=True
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    id_job_offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        null=False
    )

    id_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    date_published = models.DateTimeField(
        null=False,
        auto_now_add=True  # data zostanie zapisana automatycznie podczas tworzenia obiektu
    )

    text = models.TextField(
        null=False
    )

    is_blocked = models.BooleanField(
        null=False,
        default=False
    )

    def __str__(self):
        return self.text
