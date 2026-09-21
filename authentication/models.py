from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    """
    User profile to define roles and permissions (Admin, Manager, Standard User, Client)
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Standard User'),
        ('client', 'Client'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="User")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name="Role")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phone Number")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# ==========================================




