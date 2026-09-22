# ai_agent/views.py
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import run_inventory_agent
from authentication.decorators import role_required
from stock.models import PurchaseOrder

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


@role_required(['manager', 'admin'])
def approve_purchase_order(request, order_id):
    # هنا الكود اللي بيحول حالة أمر الشراء من Pending لـ Confirmed أو مرسل للمورد
    order = PurchaseOrder.objects.get(id=order_id)
    order.status = 'Approved'
    order.save()
    return redirect('purchase_orders_list')

# Create your views here.
