from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import TravelState
from core.logger import get_logger
from tools.travel_tools import retrieve_places, calculate_budget
import re

logger = get_logger("AccommodationAgent")

def accommodation_node(state: TravelState):
    """
    Agent tìm kiếm khách sạn và tính toán chi phí tổng.
    Bắt buộc gọi tool `retrieve_places` (tìm khách sạn) và `calculate_budget`.
    """
    logger.info("--- ACCOMMODATION AGENT ĐANG CHẠY ---")
    
    user_input = state.get("latest_user_input", "")
    travel_dates = state.get("travel_dates", "không rõ")
    
    # Ước tính số đêm từ chuỗi travel_dates (rất cơ bản cho PoC)
    nights = 2 # Mặc định
    match = re.search(r'(\d+)\s*đêm', travel_dates, re.IGNORECASE)
    if match:
        nights = int(match.group(1))
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2
    )
    llm_with_tools = llm.bind_tools([retrieve_places, calculate_budget])
    
    system_prompt = f"""
    Bạn là chuyên gia về lưu trú và ngân sách (Accommodation Agent).
    Số đêm lưu trú dự kiến: {nights} đêm.
    Yêu cầu của người dùng: {user_input}
    
    Nhiệm vụ của bạn:
    1. BẮT BUỘC gọi tool `retrieve_places` với category='hotel' để tìm khách sạn phù hợp.
    2. Sau khi chọn được khách sạn, BẮT BUỘC gọi tool `calculate_budget` để tính tổng chi phí dự kiến.
       - Tham số cho calculate_budget: 
         + hotel_price_per_night: lấy từ thông tin khách sạn.
         + nights: {nights}
         + ticket_costs: ước tính khoảng 500000 (nếu không rõ).
         + estimated_food_daily: ước tính khoảng 300000.
    
    KHÔNG ĐƯỢC TỰ TÍNH TOÁN BẰNG TAY. Phải dùng tool `calculate_budget`.
    Trình bày kết quả rõ ràng cho người dùng (bao gồm thông tin khách sạn và bảng chi phí).
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    logger.debug("Gọi LLM để tìm phòng và tính toán...")
    response = llm_with_tools.invoke(messages)
    
    while response.tool_calls:
        for tool_call in response.tool_calls:
            logger.info(f"Accommodation Agent gọi Tool: {tool_call['name']} với args: {tool_call['args']}")
            
            tool_result = ""
            if tool_call['name'] == 'retrieve_places':
                tool_result = retrieve_places.invoke(tool_call['args'])
            elif tool_call['name'] == 'calculate_budget':
                tool_result = calculate_budget.invoke(tool_call['args'])
                
            logger.debug(f"Kết quả từ Tool: {tool_result}")
            
            from langchain_core.messages import ToolMessage
            messages.append(response)
            messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call['id']))
            
        response = llm_with_tools.invoke(messages)
        
    content = response.content
    if isinstance(content, list):
        final_output = "".join(
            block["text"] if isinstance(block, dict) and "text" in block else (block if isinstance(block, str) else "") 
            for block in content
        )
    else:
        final_output = str(content)
    state["accommodation_details"] = final_output
    
    logger.info("Accommodation Agent hoàn thành.")
    return state
