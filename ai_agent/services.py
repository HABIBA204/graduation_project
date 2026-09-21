import os
from google import genai
from google.genai import types
from .tools import check_low_stock_products, get_inventory_summary
from .prompts import AGENT_SYSTEM_INSTRUCTION

def run_inventory_agent(user_message: str) -> str:
    """
    المنطق هنا: هذا هو الملف المسؤول عن التواصل مع Google GenAI API،
    وتمرير الأدوات (Tools) للنموذج لكي يقرر متى يستخدمها.
    """
    # 1. تهيئة عميل جوجل جيميناي باستخدام مفتاح الـ API
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # 2. تحديد الأدوات المتاحة للـ Agent
    my_tools = [check_low_stock_products, get_inventory_summary]
    
    # 3. إرسال الطلب للنموذج مع التعليمات (System Instruction) والأدوات
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # أو النموذج المناسب
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=AGENT_SYSTEM_INSTRUCTION,
            tools=my_tools,  # هنا المربط: نعطي الـ AI الصلاحية لاستدعاء أدوات ملف tools.py
            temperature=0.2, # درجة حرارة منخفضة ليكون دقيقاً في اتخاذ القرارات
        )
    )
    
    return response.text