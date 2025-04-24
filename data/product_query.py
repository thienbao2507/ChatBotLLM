from data.mongo_client import products

def find_products_by_keyword(keyword):
    regex = {"$regex": keyword, "$options": "i"}  # không phân biệt hoa thường
    results = products.find({
        "$or": [
            {"name": regex},
            {"brand": regex},
            {"tags": regex}
        ]
    })

    response = ""
    for p in results:
        price = f"{p['price']:,}đ"
        discount_price = int(p['price'] * (1 - p['discount'] / 100))
        response += f"\n📱 {p['name']} ({p['brand']})\n"
        response += f"💰 Giá: {price} (-{p['discount']}%) → {discount_price:,}đ\n"
        response += f"ℹ️ Mô tả: {p['description']}\n---\n"

    return response if response else "❌ Không tìm thấy sản phẩm phù hợp."
