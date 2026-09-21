
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    # بنضيف حقول إضافية مش موجودة في نموذج دجانجو الافتراضي بس محتاجينها في البيزنس بتاعنا
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True, label="User Role")
    phone = forms.CharField(max_length=15, required=False, label="Phone Number")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(func_self, commit=True):
        # ليه بنعمل override للدالة save؟
        # لأننا مش عايزين نسجل الـ User وبس، احنا عايزين كمان نحفظ الـ role والـ phone في جدول الـ UserProfile المرتبط بيه!
        user = super().save(commit=False)
        user.email = func_self.cleaned_data['email']
        
        if commit:
            user.save()
            # هنا بنعدل الـ UserProfile اللي اتعمل أوتوماتيك بالـ Signal ونحط فيه الـ role والـ phone
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = func_self.cleaned_data['role']
            profile.phone = func_self.cleaned_data.get('phone', '')
            profile.save()
            
        return user