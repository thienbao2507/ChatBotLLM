import re
from newspaper import Article
import requests
from bs4 import BeautifulSoup

# Kiểm tra câu hỏi có liên quan tới sản phẩm không
def is_product_query(text):
    keywords = ["điện thoại", "mua", "giá", "iphone", "samsung", "android", "máy", "hàng", "giảm"]
    return any(kw in text.lower() for kw in keywords)

# Kiểm tra câu hỏi có liên quan đến tin tức thời sự không
def is_news_query(text):
    keywords = ["sự kiện", "tin tức", "mới nhất", "thời sự", "nóng"]
    return any(kw in text.lower() for kw in keywords)

# Trích xuất URL từ câu hỏi (nếu có)
def extract_url(text):
    match = re.search(r"https?://\\S+", text)
    return match.group(0) if match else None

# Tóm tắt bài báo từ URL
def summarize_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return "❌ Không thể trích xuất nội dung bài báo."

# Lấy tin tức mới nhất từ VnExpress RSS
def get_latest_news():
    try:
        url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll("item")[:3]
        return "\\n\\n".join(f"{i+1}. {item.title.text}" for i, item in enumerate(items))
    except Exception as e:
        return f"Không lấy được tin tức: {e}"
