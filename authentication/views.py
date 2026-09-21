from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

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

# Create your views here.
