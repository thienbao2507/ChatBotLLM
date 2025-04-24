from pymongo import MongoClient

# Kết nối MongoDB local (hoặc thay URI nếu bạn dùng MongoDB Atlas)
client = MongoClient("mongodb://localhost:27017")

# Truy cập database và collection
db = client["chatbot"]
products = db["products"]
