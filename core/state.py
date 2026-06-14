from typing import TypedDict, List, Dict, Any, Annotated
import operator

class TravelState(TypedDict):
    """
    Trạng thái lưu trữ (Shared Memory) cho LangGraph.
    Dùng để truyền thông tin giữa các Agent thay vì gọi trực tiếp.
    """
    # Lịch sử chat giữa người dùng và hệ thống
    chat_history: Annotated[List[Dict[str, str]], operator.add]
    
    # Câu hỏi/yêu cầu mới nhất từ người dùng
    latest_user_input: str
    
    # Mục đích của người dùng: 'create' (tạo mới lịch trình) hoặc 'refine' (chỉnh sửa lịch trình)
    intent: str
    
    # Các ngày đi du lịch, ví dụ: "3 ngày 2 đêm" hoặc "từ ngày 10 đến ngày 12"
    travel_dates: str
    
    # Lịch trình chi tiết (được Itinerary Agent tạo ra)
    itinerary_plan: str
    
    # Chi tiết về khách sạn/chỗ ở (được Accommodation Agent tạo ra)
    accommodation_details: str
    
    # Tổng chi phí chuyến đi (tính bằng Tool)
    total_cost: float
