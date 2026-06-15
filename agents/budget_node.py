from core.state import TravelState
from core.logger import get_logger

logger = get_logger("BudgetNode")

def budget_node(state: TravelState):
    """
    Node tính toán cuối cùng. KHÔNG DÙNG LLM.
    Chỉ đơn thuần đọc data JSON từ Itinerary và Accommodation để tính ra tổng chi phí.
    """
    logger.info("--- BUDGET NODE ĐANG CHẠY ---")
    
    itinerary_plan = state.get("itinerary_plan", {})
    accommodation_details = state.get("accommodation_details", {})
    
    # 1. Chi phí khách sạn
    hotel_price = accommodation_details.get("price_per_night", 0)
    hotel_price_per_night = accommodation_details.get("price_per_night", 0)
    nights = accommodation_details.get("nights", 2)
    hotel_total_cost = hotel_price_per_night * nights
    
    # 2. Chi phí vé tham quan & nhà hàng (Tính trực tiếp từ giá của từng activity)
    # Tính tổng tiền từ hoạt động
    activities_cost = 0
    for day in itinerary_plan.get("days", []):
        for act in day.get("activities", []):
            activities_cost += act.get("price", 0)
            
    total_cost = hotel_total_cost + activities_cost
    
    budget_details = {
        "hotel_cost_per_night": hotel_price_per_night,
        "nights": nights,
        "hotel_total_cost": hotel_total_cost,
        "activities_cost": activities_cost,
        "total_cost": total_cost,
        "currency": "VND"
    }
    
    logger.info(f"Tổng chi phí dự tính: {total_cost:,} VND")
    return {"budget_details": budget_details}
