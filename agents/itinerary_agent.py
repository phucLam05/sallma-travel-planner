from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import TravelState
from core.logger import get_logger
from tools.travel_tools import retrieve_places

logger = get_logger("ItineraryAgent")

def itinerary_node(state: TravelState):
    """
    Agent chịu trách nhiệm lên lịch trình dựa trên các địa điểm thực tế từ Database.
    Bắt buộc phải gọi Tool `retrieve_places`.
    """
    logger.info("--- ITINERARY AGENT ĐANG CHẠY ---")
    
    user_input = state.get("latest_user_input", "")
    travel_dates = state.get("travel_dates", "không rõ")
    
    # Khởi tạo LLM và bind tool
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2
    )
    llm_with_tools = llm.bind_tools([retrieve_places])
    
    system_prompt = f"""
    Bạn là một chuyên gia lên kế hoạch du lịch (Itinerary Agent).
    Bạn ĐƯỢC YÊU CẦU BẮT BUỘC phải sử dụng công cụ `retrieve_places` để tìm kiếm các 'attraction' (điểm tham quan) và 'restaurant' (nhà hàng) trước khi lập lịch trình.
    KHÔNG ĐƯỢC tự bịa ra địa điểm (hallucinate).
    
    Yêu cầu của người dùng: {user_input}
    Thời gian đi: {travel_dates}
    
    Hãy lên một lịch trình thật chi tiết theo từng ngày, sử dụng đúng thông tin từ tool trả về.
    Nếu người dùng đang yêu cầu chỉnh sửa (refine) lịch trình cũ, hãy tập trung sửa đúng phần họ yêu cầu (ví dụ: đổi nhà hàng).
    
    Lịch trình hiện tại (nếu có): {state.get('itinerary_plan', 'Chưa có')}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    logger.debug("Gọi LLM để lập lịch trình...")
    # Chạy LLM, có thể LLM sẽ trả về yêu cầu gọi tool
    response = llm_with_tools.invoke(messages)
    
    # Xử lý luồng gọi Tool
    while response.tool_calls:
        for tool_call in response.tool_calls:
            logger.info(f"Itinerary Agent gọi Tool: {tool_call['name']} với args: {tool_call['args']}")
            
            if tool_call['name'] == 'retrieve_places':
                tool_result = retrieve_places.invoke(tool_call['args'])
                logger.debug(f"Kết quả từ Tool: {tool_result}")
                
                # Thêm tool result vào lịch sử hội thoại của LLM
                from langchain_core.messages import ToolMessage
                messages.append(response) # Append lại tin nhắn yêu cầu gọi tool
                messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call['id']))
        
        # Gọi lại LLM với kết quả từ tool
        response = llm_with_tools.invoke(messages)
    
    content = response.content
    if isinstance(content, list):
        final_plan = "".join(
            block["text"] if isinstance(block, dict) and "text" in block else (block if isinstance(block, str) else "") 
            for block in content
        )
    else:
        final_plan = str(content)
    state["itinerary_plan"] = final_plan
    
    logger.info("Itinerary Agent hoàn thành lập lịch trình.")
    return state
