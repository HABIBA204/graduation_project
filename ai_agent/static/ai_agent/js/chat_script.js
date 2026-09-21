// 1. استخراج رمز الحماية الأمني من صفحة الـ HTML
function getCSRFToken() {
    return document.getElementById('csrf_token').value;
}

// 2. الدالة المسؤولة عن إرسال الرسالة واستقبال رد الـ AI دون إعادة تحميل الصفحة
async function sendMessage() {
    const inputField = document.getElementById('userInput');
    const messageText = inputField.value.trim();
    if (!messageText) return;

    const chatBox = document.getElementById('chatBox');

    // أ. عرض رسالة المستخدم فوراً في شاشة المحادثة
    chatBox.innerHTML += `<div class="message user-message">${messageText}</div>`;
    inputField.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // ب. إرسال الطلب للخلفية عبر Fetch API
        const response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            },
            body: new URLSearchParams({ 'message': messageText })
        });

        const data = await response.json();

        if (data.status === 'success') {
            // ج. عرض رد الـ AI القادم من السيرفر
            chatBox.innerHTML += `<div class="message ai-message" style="direction: rtl;">${data.response}</div>`;
        } else {
            chatBox.innerHTML += `<div class="message ai-message" style="color:red; direction: rtl;">حدث خطأ: ${data.message}</div>`;
        }

    } catch (error) {
        console.error('Connection Error:', error);
        chatBox.innerHTML += `<div class="message ai-message" style="color:red; direction: rtl;">فشل الاتصال بالسيرفر.</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// 3. تفعيل زر Enter من لوحة المفاتيح للإرسال السريع
document.addEventListener('DOMContentLoaded', () => {
    const inputElement = document.getElementById('userInput');
    if (inputElement) {
        inputElement.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});