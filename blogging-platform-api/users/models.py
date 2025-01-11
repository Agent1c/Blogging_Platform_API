# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.db import models
# from django.utils import timezone

# class CustomUserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("You have not provided a valid e-mail address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=255, blank=True, default='')
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     # last_login = models.DateTimeField(null=True, blank=True)  # Optional: if you want to track last login
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'

#     def get_full_name(self):
#         return self.name

#     def get_short_name(self):
#         return self.name or self.email.split('@')[0]
    
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,  Group, Permission

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255, null=False)
    username = models.CharField(unique=True, max_length=30)
    # name = models.CharField(max_length=255, blank=True, default='')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change this to something unique
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    # class Meta:
    #     verbose_name = 'user'
    #     verbose_name_plural = 'users'

    # def get_full_name(self):
    #     return self.name

    # def get_short_name(self):
    #     return self.name or self.email.split('@')[0]