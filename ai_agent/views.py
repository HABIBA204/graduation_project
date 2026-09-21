# ai_agent/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import run_inventory_agent

@login_required  # ضمان الأمان وأن المستخدم مسجل دخوله (RBAC)
def agent_chat_view(request):
    if request.method == "POST":
        # 1. استقبال النص المكتوب من واجهة المستخدم (Frontend)
        user_message = request.POST.get("message", "").strip()
        
        if not user_message:
            return JsonResponse({"error": "الرجاء إدخال طلب صحيح."}, status=400)
        
        try:
            # 2. تمرير الطلب لعقل الـ Agent وإرجاع النتيجة
            agent_response = run_inventory_agent(user_message)
            
            # 3. إرجاع النتيجة بصيغة JSON لكي يعرضها المتصفح بسلاسة
            return JsonResponse({"status": "success", "response": agent_response})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # لو الطلب GET، بنعرض صفحة الدردشة أو لوحة التحكم الخاصة بالـ Agent
    return render(request, "ai_agent/chat_dashboard.html")
# Create your views here.
