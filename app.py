from openai import OpenAI
from dotenv import load_dotenv
from mongo_module import find_products_by_keyword
from chat_engine import is_news_query, extract_url, get_latest_news, summarize_article
from gradioInterface import build_gradio_ui
import os
import fitz

customer_mode = {"enabled": False}
pdf_context = {"content": ""}

def toggle_customer_mode(toggle):
    customer_mode["enabled"] = toggle
    return f"Tư vấn khách hàng: {'BẬT' if toggle else 'TẮT'}"

def upload_pdf(file):
    text = ""
    try:
        doc = fitz.open(file.name)
        for page in doc:
            text += page.get_text()
        pdf_context["content"] = text
        return "✅ Đã tải và đọc nội dung PDF thành công!"
    except Exception as e:
        return f"❌ Lỗi đọc PDF: {e}"

# Load API Key
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def find_products_by_keyword(keyword):
    sample_products = [
        {
            "name": "iPhone 15 Pro Max",
            "brand": "Apple",
            "price": 32990000,
            "discount": 10,
            "description": "Flagship mạnh mẽ từ Apple"
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "brand": "Samsung",
            "price": 28990000,
            "discount": 12,
            "description": "Điện thoại cao cấp, camera tốt"
        }
    ]

    result = ""
    for product in sample_products:
        if keyword.lower() in product["name"].lower() or keyword.lower() in product["brand"].lower():
            discounted_price = int(product["price"] * (1 - product["discount"]/100))
            result += f"\n📱 {product['name']} ({product['brand']})\n"
            result += f"💰 Giá: {product['price']:,}đ (-{product['discount']}%) → {discounted_price:,}đ\n"
            result += f"ℹ️ Mô tả: {product['description']}\n---\n"

    return result if result else "❌ Không tìm thấy sản phẩm phù hợp."

def chat_with_gemini(message, history):
    if customer_mode["enabled"]:
        return find_products_by_keyword(message)

    if is_news_query(message):
        raw_news = get_latest_news()
        prompt = f"Hãy tóm tắt và phân tích các sự kiện sau:\n\n{raw_news}"
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    url = extract_url(message)
    if url:
        text = summarize_article(url)
        if text.startswith("❌"): return text
        prompt = f"Tóm tắt bài báo sau:\n\n{text}"
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    prompt = pdf_context["content"] and f"Dựa vào tài liệu sau, trả lời:\n\n{pdf_context['content']}\n\nCâu hỏi: {message}" or message
    messages = [{"role": "system", "content": "Bạn là trợ lý AI thân thiện."}]
    for user, bot in history:
        messages.extend([
            {"role": "user", "content": user},
            {"role": "assistant", "content": bot}
        ])
    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(model="gemini-2.0-flash", messages=messages, stream=True)
    reply = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            reply += chunk.choices[0].delta.content
    return reply

# Khởi chạy app
app = build_gradio_ui(chat_with_gemini, upload_pdf, toggle_customer_mode)
app.launch()
