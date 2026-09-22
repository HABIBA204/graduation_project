from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    """
    منطق التحقق الديناميكي: 
    يستقبل قائمة بالأدوار المصرح لها (مثل ['admin', 'manager']) ويتحقق 
    ما إذا كان دور المستخدم الحالي يقع ضمن هذه القائمة أم لا.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. التأكد أن المستخدم مسجل الدخول ولديه بروفايل مرتبط
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                # 2. التحقق مما إذا كان دور المستخدم موجوداً ضمن الأدوار المصرح لها
                if request.user.profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            
            # إذا فشل الشرط، يتم منع الوصول وإرسال خطأ الصلاحيات
            raise PermissionDenied("عذراً، لا تملك الصلاحية اللازمة للقيام بهذا الإجراء.")
        return _wrapped_view
    return decorator