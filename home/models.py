from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings 
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):  
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    
    identydoc = models.FileField(upload_to='user_docs/', blank=True, null=True)  
    DOB = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


from django.db import models



class Essay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    grammar_errors = models.PositiveIntegerField(default=0)
    spelling_errors = models.PositiveIntegerField(default=0)
    total_errors = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0)
    pdf_file = models.FileField(upload_to="essays/pdfs/", blank=True, null=True)
    
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    

   

@receiver(post_delete, sender=Essay)
def delete_pdf_file(sender, instance, **kwargs):
    if instance.pdf_file and os.path.isfile(instance.pdf_file.path):
        os.remove(instance.pdf_file.path)






