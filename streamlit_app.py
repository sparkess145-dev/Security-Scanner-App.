
%%writefile streamlit_app.py
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

        output =
