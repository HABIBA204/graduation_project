from stock.models import Product, Supplier, PurchaseOrder, PurchaseOrderItem
from django.db import transaction
from django.db.models import F

def check_low_stock_products() -> str:
    """
    أداة وظيفية لفحص المنتجات التي وصل مخزونها إلى حد النفاذ (أو أقل من الحد الأدنى)،
    وتقسيمها تلقائياً حسب المورد المسؤول عنها لتجهيز مسودات أوامر الشراء.
    """
    # 1. المنطق: استعلام قاعدة البيانات لجلب المنتجات التي الكمية فيها أقل أو تساوي الحد الأدنى
    low_stock_items = Product.objects.filter(stock_quantity__lte=F('low_stock_threshold'))
    
    if not low_stock_items.exists():
        return "المخزون في وضع آمن تماماً، ولا توجد أي منتجات بحاجة لإعادة طلب حالياً."

    # 2. المنطق: تجميع المنتجات الناقصة حسب كل مورد لتنظيم أوامر الشراء
    supplier_orders = {}
    for product in low_stock_items:
        supplier = product.supplier
        if not supplier:
            continue # تخطي المنتجات التي ليس لها مورد مسجل لتجنب الأخطاء
        
        if supplier not in supplier_orders:
            supplier_orders[supplier] = []
        supplier_orders[supplier].append(product)

    report = []
    
    # استخدام transaction لضمان سلامة البيانات (إما أن يتم حفظ كل الأوامر أو لا يتم شيء لو حدث خطأ)
    with transaction.atomic():
        for supplier, products in supplier_orders.items():
            # 3. المنطق: إنشاء رأس أمر الشراء بحالة 'draft' (مسودة) للمورد
            purchase_order = PurchaseOrder.objects.create(
                supplier=supplier,
                status='draft',
                notes="تم إنشاء هذا الأمر تلقائياً بواسطة نظام الـ AI Agent بسبب انخفاض المخزون."
            )
            
            items_summary = []
            for product in products:
                # حساب كمية ذكية مقترحة للطلب (ضعف الحد الأدنى مطروحاً منه المخزون الحالي، بحد أدنى 5 قطع)
                suggested_qty = max((product.low_stock_threshold * 2) - product.stock_quantity, 5)
                
                # إنشاء تفاصيل بند أمر الشراء
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    product=product,
                    quantity=suggested_qty,
                    unit_price=product.cost_price  # سعر التكلفة الافتراضي للمنتج
                )
                items_summary.append(f"- {product.name}: تم طلب عدد {suggested_qty} قطعة")
            
            report.append(f"تم بنجاح إنشاء مسودة أمر شراء رقم #{purchase_order.id} للمورد: {supplier.name}\n" + "\n".join(items_summary))

    return "\n\n".join(report)


def get_inventory_summary() -> str:
    """
    أداة استعلام عامة تتيح للـ AI Agent جلب ملخص شامل لحالة المخزون الكلي 
    (إجمالي عدد المنتجات، المنتجات المتاحة، والمنتجات النافذة) للإجابة على أسئلة المدير.
    """
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lte=F('low_stock_threshold')).count()
    out_of_stock_count = Product.objects.filter(stock_quantity=0).count()
    
    summary = (
        f"تقرير حالة المخزون الحالي:\n"
        f"- إجمالي أنواع المنتجات في النظام: {total_products}\n"
        f"- المنتجات التي تحت حد الأمان (تحتاج انتباه): {low_stock_count}\n"
        f"- المنتجات النافذة تماماً (رصيدها صفر): {out_of_stock_count}"
    )
    return summary