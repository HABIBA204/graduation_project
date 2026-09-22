from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout



def register_view(request):
    
    """
    منطق معالجة تسجيل مستخدم جديد في النظام
    """
    if request.method == 'POST':
        # استقبال البيانات المرسلة من المتصفح عبر الـ POST
        form = UserRegistrationForm(request.POST)
        
        # التأكد من صحة البيانات ومطابقتها للشروط الأمنية
        if form.is_valid():
            # حفظ المستخدم والبروفايل الخاص به في قاعدة البيانات
            form.save()
            
            # استخراج اسم المستخدم لعرض رسالة ترحيبية مخصصة
            username = form.cleaned_data.get('username')
            messages.success(request, f'تم إنشاء الحساب بنجاح يا {username}! يمكنك تسجيل الدخول الآن.')
            
            # توجيه المستخدم إلى صفحة تسجيل الدخول بعد النجاح
            return redirect('login')  # (سنتأكد من ربط مسار الـ login لاحقاً)
    else:
        # لو الطلب GET، اعرض للمستخدم نموذج تسجيل فارغ نظيف
        form = UserRegistrationForm()
    
    # تمرير الفورم لملف الـ HTML لعرضه للمستخدم
    return render(request, 'authentication/register.html', {'form': form})



def login_view(request):
    """
    Handle user login logic: authenticate credentials and establish a session.
    """
    if request.method == 'POST':
        # Bind the POST data to Django's built-in AuthenticationForm
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Extract authenticated user object from the cleaned form
            user = form.get_user()
            
            # Establish the user session
            login(request, user)
            
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Redirect to the main dashboard or home page after successful login
            return redirect('home')  # ( تأكدي من ربط مسار الـ home عندك )
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        # Display an empty login form for GET requests
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {'form': form})



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    منطق تسجيل الخروج: إنهاء جلسة المستخدم الحالية وتوجيهه لصفحة تسجيل الدخول
    """
    logout(request) # دالة دجانجو لتدمير الـ Session الحالية
    return redirect('login') # التوجيه الآمن لصفحة تسجيل الدخول




