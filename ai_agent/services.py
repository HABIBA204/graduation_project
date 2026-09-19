import os
from google import genai
from google.genai import types
from django.conf import settings
from .models import Product, PurchaseOrder, PurchaseOrderItem

# تهيئة عميل جوجل جيمي باستخدام المكتبة الرسمية الحديثة
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def check_inventory_and_create_orders():
    """
    دالة يقوم الـ Agent باستدعائها أو تنفيذها لفحص المنتجات التي قاربت على النفاد
    وإنشاء مسودة أمر شراء تلقائياً للموردين.
    """
    # 1. المنطق: استخراج المنتجات التي تخطت حد الأمان (الكمية أقل من أو تساوي الحد الأدنى)
    low_stock_products = [
        p for p in Product.objects.all() 
        if p.stock_quantity <= p.low_stock_threshold
    ]

    if not low_stock_products:
        return "المخزون بحالة ممتازة، لا توجد منتجات تتطلب إعادة طلب حالياً."

    created_orders_summary = []

    # 2. تجميع المنتجات حسب المورد لتنظيم أوامر الشراء بصورة منطقية
    supplier_orders = {}
    for product in low_stock_products:
        supplier = product.supplier
        if supplier not in supplier_orders:
            supplier_orders[supplier] = []
        supplier_orders[supplier].append(product)

    # 3. إنشاء أوامر الشراء كمسودات (Drafts) في قاعدة البيانات
    for supplier, products in supplier_orders.items():
        # إنشاء رأس أمر الشراء بحالة معلقة أو مسودة
        purchase_order = PurchaseOrder.objects.create(
            supplier=supplier,
            status='Pending'  # الحالة المعلقة أو المسودة
        )

        for product in products:
            # الكمية المقترح طلبها تعوض العجز (مثلاً: ضعف الحد الأدنى أو كمية ثابتة للتغطية)
            suggested_quantity = (product.low_stock_threshold * 2) - product.stock_quantity
            
            PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                product=product,
                quantity=max(suggested_quantity, 5) # ضمان طلب حد أدنى مناسب
            )
        
        created_orders_summary.append(f"تم إنشاء أمر شراء رقم #{purchase_order.id} للمورد {supplier.name}")

    return "\n".join(created_orders_summary)


def ask_inventory_agent(user_prompt):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            tools=[check_inventory_and_create_orders], # إعطاء الدالة كأداة للنموذج
            system_instruction="أنت مساعد ذكي لإدارة المخزون والمبيعات، مهمتك تحليل حالة المنتجات ومساعدة المسؤول في اتخاذ القرارات وإدارة المخزون بدقة.",
            temperature=0.3,
        )
    )
    return response.text