from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError(_('User must have an email address'))
        
        if not username:
            raise ValueError(_('User must have a username'))
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        # Create a user profile for the new user
        UserProfile.objects.create(user=user)
        
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    username = models.CharField(max_length=100, unique=True, verbose_name=_('Username'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=100, verbose_name=_('Phone Number'))
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
    last_login = models.DateTimeField(auto_now_add=True, verbose_name=_('Last Login'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is Staff'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is Active'))
    is_superadmin = models.BooleanField(default=False, verbose_name=_('Is Superadmin'))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.email
    
    # permission
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    address_line_1 = models.CharField(blank=True, max_length=100, verbose_name=_('Address Line 1'))
    address_line_2 = models.CharField(blank=True, max_length=100, verbose_name=_('Address Line 2'))
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', verbose_name=_('Profile Picture'))
    city = models.CharField(blank=True, max_length=60, verbose_name=_('City'))
    state = models.CharField(blank=True, max_length=60, verbose_name=_('State'))
    country = models.CharField(blank=True, max_length=60, verbose_name=_('Country'))
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'
