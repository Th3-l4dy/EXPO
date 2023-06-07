from datetime import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, password=None, role=None, username=None, skills=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            username=username,
            skills=skills,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, role="Admin", username=None, skills=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, first_name, last_name, password, role, username, skills,**extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        SUPERVISOR = "SUPERVISOR", "Supervisor"

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=None)
    skills = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "role"]

    objects = UserManager()

    def str(self):
        return self.email



class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.STUDENT)

class Student(User):
    class Meta:
        proxy = True

    objects = StudentManager()

    def save(self, *args, **kwargs):
        self.role = User.Role.STUDENT
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.STUDENT:
        Students.objects.create(user=instance)

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class SupervisorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role="Supervisor")


class Supervisor(User):
    class Meta:
        proxy = True

    objects = SupervisorManager()

    def save(self, *args, **kwargs):
        self.role = "Supervisor"
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.SUPERVISOR:
        Supervisors.objects.create(user=instance)

class Supervisors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
  

  

class Projects(models.Model):
    class Year(models.TextChoices): 
        YEAR_2 = '2CPI', '2CPI'
        YEAR_3 = '1CS', '1CS'
        YEAR_4 = '2CS', '2CS'
        YEAR_5 = '3CS', '3CS'
    class Category(models.TextChoices):
        ARDUINO = 'Arduino', 'Arduino'
        DESKTOP = 'Desktop App', 'Desktop App'
        APP = 'App', 'App' 
        WEBSITE = 'Web-app', 'Web-app'
        

     
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.CharField(max_length=4, choices=Year.choices, default=None)
    category = models.CharField(max_length=20, choices=Category.choices, default=None)
    created = models.ManyToManyField(User, related_name='projects_created', limit_choices_to={'role': 'STUDENT'}, blank=True)
    created_by = models.TextField(blank=True)
    supervised_by = models.TextField(blank=True)
    used_techs = models.TextField(blank=True)
    logo = models.ImageField(upload_to='project_logos/', blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='project_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='project_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    def __str__(self):
        return self.title

class Ideas(models.Model):
    title = models.CharField(max_length=100,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def str(self):
        return self.title