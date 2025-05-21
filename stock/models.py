# from email.policy import default
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from pkg_resources import require

from api_gestion_stock.models import BaseUUIDModel


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model to handle user creation and superuser creation.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email, username, and password.
        
        Args:
            email (str): The email address of the user.
            username (str): The username of the user.
            password (str, optional): The password of the user.
            extra_fields (dict, optional): Extra fields to be added to the user.

        Returns:
            User: A new user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email, username, and password.
        
        Args:
            email (str): The email address of the superuser.
            username (str): The username of the superuser.
            password (str, optional): The password of the superuser.
            extra_fields (dict, optional): Extra fields to be added to the superuser.

        Returns:
            User: A new superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model to handle user authentication and additional fields such as phone, reset token, etc.

    Attributes:
        id (UUIDField): Unique identifier for the user.
        id_employee (id_employee field): Unique employee_id corresponding for the user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_employee = models.UUIDField(editable=False, unique=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]

    objects = CustomUserManager()

    def __str__(self):
        """
        String representation of the User instance, returns the username.
        
        Returns:
            str: The username of the user.
        """
        return self.username

    def save(self, *args, **kwargs):
        """
        Saves the user instance
        """
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date_joined']

class Supplier(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) 

class ArticleFamily(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True) 

class Article(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    family = models.OneToOneField(ArticleFamily, on_delete=models.CASCADE, related_name='articles')
    is_active = models.BooleanField(default=True) 

class Stock(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initial_stock = models.IntegerField(default=0)
    stock_variation = models.IntegerField(default=0)
    final_stock = models.IntegerField(default=0)
    article = models.UUIDField(default=None, blank=True, unique=True)
    is_active = models.BooleanField(default=True) 


class Service(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) 

class EntryVoucher(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField()
    description = models.TextField()
    reference_number = models.CharField(max_length=50, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    created_by = models.UUIDField(editable=False)
    updated_by = models.UUIDField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier = models.UUIDField(default=None, blank=True)
    article = models.UUIDField(default=None, blank=True)
    is_active = models.BooleanField(default=True)


class ExitRequest(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)
    article = models.UUIDField(default=None, blank=True)
    quantity = models.IntegerField()
    description = models.TextField()
    request_code = models.CharField(max_length=50, unique=True, null=True)
    is_active = models.BooleanField(default=True) 
    applicant = models.UUIDField(null=True, blank=True)

class ExitVoucher(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=50, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    created_by = models.UUIDField(editable=False)
    updated_by = models.UUIDField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exit_request = models.ForeignKey(ExitRequest, on_delete=models.CASCADE, related_name='exit_requests', null=True)
    employee = models.UUIDField(default=None, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True) 
    applicant = models.UUIDField(null=True, blank=True)

class ReturnRequest(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)
    article = models.UUIDField(default=None, blank=True)
    employee = models.UUIDField(default=None, blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True) 
    applicant = models.UUIDField(null=True, blank=True)

class ReturnVoucher(BaseUUIDModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=50, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    created_by = models.UUIDField(editable=False)
    updated_by = models.UUIDField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    employee = models.UUIDField(default=None, blank=True)
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name='return_requests', null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True) 
    applicant = models.UUIDField(null=True, blank=True)
