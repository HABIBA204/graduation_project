from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # تعريف الأدوار المتاحة في النظام بناءً على متطلبات الـ RBAC
    ROLE_CHOICES = (
        ('owner', 'Owner (المالك)'),
        ('employee', 'Employee (الموظف)'),
    )

    # ربط الجدول بجدول المستخدمين الأساسي في دجانجو علاقة One-to-One
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # حقل الدور لتحديد صلاحيات المستخدم
    role = models.CharField(max_lenth=20, choices=ROLE_CHOICES, default='employee')
    
    # حقول إضافية اختيارية مفيدة للموظف والمالك (مثل رقم الهاتق أو الفرع)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Create your models here.
