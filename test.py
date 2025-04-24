from pymongo import MongoClient

# Thay đổi nếu dùng MongoDB Atlas
client = MongoClient("mongodb://localhost:27017")

try:
    # Lấy danh sách database
    db_names = client.list_database_names()
    print("✅ Đã kết nối thành công!")
    print("📂 Các database hiện có:", db_names)

    # Truy cập database & collection
    db = client["chatbot"]
    products = db["products"]

    # Lấy 1 document đầu tiên
    product = products.find_one()
    if product:
        print("📄 Một sản phẩm đầu tiên:", product)
    else:
        print("⚠️ Collection 'products' chưa có dữ liệu.")
except Exception as e:
    print("❌ Kết nối thất bại:", e)
