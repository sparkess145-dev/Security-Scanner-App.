import streamlit as st
import requests
import sys

# ---------------------------------------------
# 1. كود فحص الأمان
# ---------------------------------------------
REQUIRED_HEADERS = [
    'Strict-Transport-Security', 'Content-Security-Policy',
    'X-Content-Type-Options', 'X-Frame-Options',
    'Referrer-Policy', 'Permissions-Policy'
]

def scan_security_headers_gui(url):
    """يفحص رؤوس الأمان ويعيد النتائج كنص منسق."""
    if not url.startswith(('http://', 'https://')):
        return "❌ خطأ: يجب إدخال رابط يبدأ بـ http:// أو https://"

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        output = "## ✅ تم إيجاد الرؤوس التالية:\n"
        
        for header, value in sorted(headers.items()):
            output += f"* **{header}**: `{value}`\n"
        
        output += "\n---\n"
        output += "## ⚠️ تقييم الأمان (الرؤوس المفقودة):\n"
        
        missing_count = 0
        
        for required_header in REQUIRED_HEADERS:
            if required_header not in headers:
                output += f"**[⚠️ خطر!]** الرأس **{required_header}** مفقود. (مخاطر أمنية عالية)\n"
                missing_count += 1
            else:
                value = headers[required_header]
                if required_header == 'X-Frame-Options' and 'DENY' not in value.upper() and 'SAMEORIGIN' not in value.upper():
                    output += f"**[❗ تحذير]** قيمة X-Frame-Options ضعيفة: `{value}`. يجب أن تكون DENY أو SAMEORIGIN.\n"
        
        if missing_count == 0:
            output += "**[👍 ممتاز]** جميع رؤوس الأمان الحرجة موجودة.\n"
        
        return output

    except requests.exceptions.Timeout:
        return "❌ خطأ: انتهت مهلة الطلب. الموقع بطيء جدًا أو غير مستجيب."
    except requests.exceptions.RequestException as e:
        return f"❌ خطأ في الاتصال: {e}"
    except Exception as e:
        return f"❌ خطأ غير متوقع: {e}"


# ---------------------------------------------
# 2. واجهة Streamlit الرسومية
# ---------------------------------------------
st.set_page_config(page_title="Security Header Scanner", layout="wide")
st.title('🛡️ Security Header Scanner (فاحص رؤوس الأمان)')
st.markdown('أدخل عنوان URL للتحقق من وجود رؤوس أمان HTTP الحرجة مثل HSTS و CSP.')

url_input = st.text_input('أدخل رابط الموقع (يجب أن يبدأ بـ http:// أو https://)', 'https://google.com')

if st.button('إبدأ الفحص', type="primary"):
    if url_input:
        st.info(f"جاري فحص: {url_input}...")
        results = scan_security_headers_gui(url_input)
        
        st.markdown("---")
        st.markdown("### 📋 تقرير الفحص")
        st.markdown(results)
    else:
        st.error("الرجاء إدخال رابط لبدء الفحص.")
