from typing import List, Dict, Any

# Mock data phong phú về Đà Nẵng để kiểm thử
MOCK_DATABASE = [
    # Khách sạn
    {
        "id": "h1",
        "name": "Mường Thanh Luxury Đà Nẵng",
        "category": "hotel",
        "description": "Khách sạn 5 sao sát biển Mỹ Khê, view đẹp, hồ bơi vô cực.",
        "price_per_night": 2000000,
        "location": "Biển Mỹ Khê",
        "rating": 4.8
    },
    {
        "id": "h2",
        "name": "Furama Resort Danang",
        "category": "hotel",
        "description": "Khu nghỉ dưỡng đẳng cấp, sang trọng bậc nhất, phù hợp nghỉ dưỡng gia đình.",
        "price_per_night": 4500000,
        "location": "Biển Mỹ Khê",
        "rating": 4.9
    },
    {
        "id": "h3",
        "name": "Naman Retreat",
        "category": "hotel",
        "description": "Kiến trúc tre độc đáo, không gian yên tĩnh, hòa mình vào thiên nhiên.",
        "price_per_night": 3500000,
        "location": "Đường Trường Sa",
        "rating": 4.8
    },
    {
        "id": "h4",
        "name": "Avora Hotel",
        "category": "hotel",
        "description": "Khách sạn 3 sao, ngay trung tâm sông Hàn, tiện di chuyển.",
        "price_per_night": 600000,
        "location": "Sông Hàn",
        "rating": 4.3
    },
    {
        "id": "h5",
        "name": "Minh Toan Galaxy Hotel",
        "category": "hotel",
        "description": "Khách sạn 4 sao, tiện nghi, giá cả phải chăng, ngay trung tâm thành phố.",
        "price_per_night": 900000,
        "location": "Trung tâm",
        "rating": 4.5
    },

    # Điểm tham quan
    {
        "id": "a1",
        "name": "Bà Nà Hills",
        "category": "attraction",
        "description": "Khu du lịch trên núi với Cầu Vàng nổi tiếng, công viên giải trí Fantasy Park.",
        "ticket_price": 900000,
        "location": "Hòa Vang",
        "duration": "1 ngày"
    },
    {
        "id": "a2",
        "name": "Bán đảo Sơn Trà & Chùa Linh Ứng",
        "category": "attraction",
        "description": "Ngắm cảnh biển, tượng Phật Bà Quan Âm lớn nhất Việt Nam.",
        "ticket_price": 0,
        "location": "Sơn Trà",
        "duration": "Nửa ngày"
    },
    {
        "id": "a3",
        "name": "Ngũ Hành Sơn",
        "category": "attraction",
        "description": "Hệ thống 5 ngọn núi đá vôi, hang động, chùa chiền linh thiêng.",
        "ticket_price": 40000,
        "location": "Ngũ Hành Sơn",
        "duration": "Nửa ngày"
    },
    {
        "id": "a4",
        "name": "Phố cổ Hội An (gần Đà Nẵng)",
        "category": "attraction",
        "description": "Di sản văn hóa thế giới, cách Đà Nẵng 30km, thả đèn hoa đăng.",
        "ticket_price": 120000,
        "location": "Quảng Nam",
        "duration": "Chiều - Tối"
    },
    {
        "id": "a5",
        "name": "Công viên Châu Á (Asia Park)",
        "category": "attraction",
        "description": "Công viên giải trí với vòng quay Mặt Trời Sun Wheel lớn.",
        "ticket_price": 200000,
        "location": "Trung tâm",
        "duration": "Buổi tối"
    },

    # Nhà hàng & Ẩm thực
    {
        "id": "r1",
        "name": "Hải sản Năm Đảnh",
        "category": "restaurant",
        "description": "Hải sản tươi ngon, giá bình dân, luôn đông khách.",
        "avg_price": 200000,
        "location": "Sơn Trà"
    },
    {
        "id": "r2",
        "name": "Bánh tráng cuốn thịt heo Trần",
        "category": "restaurant",
        "description": "Đặc sản Đà Nẵng nổi tiếng, không gian rộng rãi.",
        "avg_price": 150000,
        "location": "Trung tâm"
    },
    {
        "id": "r3",
        "name": "Mì Quảng Bà Mua",
        "category": "restaurant",
        "description": "Quán mì Quảng lâu đời, đậm đà hương vị miền Trung.",
        "avg_price": 50000,
        "location": "Hải Châu"
    },
    {
        "id": "r4",
        "name": "Bún chả cá Ông Tạ",
        "category": "restaurant",
        "description": "Bún chả cá nước ngọt thanh, chả cá dai ngon.",
        "avg_price": 40000,
        "location": "Hải Châu"
    },
    {
        "id": "r5",
        "name": "Chè sầu Liên",
        "category": "restaurant",
        "description": "Món tráng miệng đặc trưng Đà Nẵng, béo ngậy vị sầu riêng.",
        "avg_price": 30000,
        "location": "Nhiều cơ sở"
    }
]

class DatabaseManager:
    """
    Class để mock các truy vấn vào Database.
    Ở Phase 1, nó sẽ lọc danh sách MOCK_DATABASE.
    """
    
    @staticmethod
    def search_places(category: str = None, keyword: str = None) -> List[Dict[str, Any]]:
        """
        Tìm kiếm địa điểm dựa trên danh mục (hotel, attraction, restaurant) và từ khóa.
        """
        results = MOCK_DATABASE
        
        # Lọc theo category
        if category:
            results = [item for item in results if item["category"].lower() == category.lower()]
            
        # Lọc theo keyword (tìm trong name hoặc description)
        if keyword:
            keyword = keyword.lower()
            results = [item for item in results if keyword in item["name"].lower() or keyword in item["description"].lower()]
            
        return results

    @staticmethod
    def get_place_by_id(place_id: str) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết một địa điểm qua ID.
        """
        for item in MOCK_DATABASE:
            if item["id"] == place_id:
                return item
        return None
