import json
from langchain_core.tools import tool
from core.database import DatabaseManager

@tool
def retrieve_places(category: str, keyword: str = "") -> str:
    """
    Truy xuất danh sách các địa điểm từ cơ sở dữ liệu.
    
    Args:
        category (str): Phân loại địa điểm cần tìm ('hotel', 'attraction', hoặc 'restaurant').
        keyword (str, optional): Từ khóa tìm kiếm (ví dụ: 'giá rẻ', 'trung tâm', 'biển'). Mặc định là chuỗi rỗng.
        
    Returns:
        str: Chuỗi JSON chứa danh sách các địa điểm tìm được, gồm tên, mô tả, giá và đánh giá (nếu có).
    """
    # Gọi DatabaseManager để tìm kiếm
    results = DatabaseManager.search_places(category=category, keyword=keyword)
    
    if not results:
        return f"Không tìm thấy địa điểm nào phù hợp với danh mục '{category}' và từ khóa '{keyword}'."
        
    # Trả về kết quả dưới dạng JSON string để LLM dễ xử lý
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def calculate_budget(hotel_price_per_night: float, nights: int, ticket_costs: float, estimated_food_daily: float) -> str:
    """
    Tính toán tổng chi phí ước tính cho chuyến đi (Budgeting Tool không dùng LLM).
    
    Args:
        hotel_price_per_night (float): Giá phòng khách sạn mỗi đêm.
        nights (int): Số đêm lưu trú.
        ticket_costs (float): Tổng chi phí vé tham quan.
        estimated_food_daily (float): Chi phí ăn uống ước tính mỗi ngày.
        
    Returns:
        str: Kết quả tổng chi phí dưới định dạng chuỗi.
    """
    total_hotel = hotel_price_per_night * nights
    total_food = estimated_food_daily * (nights + 1) # Giả sử số ngày = số đêm + 1
    
    total_cost = total_hotel + ticket_costs + total_food
    
    # Định dạng kết quả
    result = (
        f"Chi tiết dự toán:\n"
        f"- Chi phí khách sạn ({nights} đêm x {hotel_price_per_night:,} VNĐ): {total_hotel:,} VNĐ\n"
        f"- Chi phí vé tham quan: {ticket_costs:,} VNĐ\n"
        f"- Chi phí ăn uống ({nights + 1} ngày x {estimated_food_daily:,} VNĐ/ngày): {total_food:,} VNĐ\n"
        f"---------------------------\n"
        f"=> TỔNG CHI PHÍ ƯỚC TÍNH: {total_cost:,} VNĐ"
    )
    return result
