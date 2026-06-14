import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import TravelState
from core.logger import get_logger

logger = get_logger("WorkflowAgent")

def workflow_node(state: TravelState):
    """
    Agent đầu tiên tiếp nhận yêu cầu.
    Nhiệm vụ: Phân tích intent (create/refine) và trích xuất ngày đi (travel_dates).
    """
    logger.info("--- WORKFLOW AGENT ĐANG CHẠY ---")
    
    user_input = state.get("latest_user_input", "")
    if not user_input:
        logger.warning("Không có đầu vào từ người dùng.")
        return state

    # Cấu hình LLM Gemini 3.5 Flash
    # Yêu cầu phải có biến môi trường GOOGLE_API_KEY hoặc GEMINI_API_KEY
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.0
    )
    
    # Prompt chặt chẽ để buộc LLM trả về đúng định dạng
    system_prompt = """
    Bạn là một trợ lý điều phối quy trình du lịch (Workflow Router).
    Nhiệm vụ của bạn là đọc yêu cầu của người dùng và trả về đúng 2 thông tin phân cách bởi dấu |:
    1. Intent: 'create' (nếu người dùng muốn tạo lịch trình mới) hoặc 'refine' (nếu người dùng muốn sửa đổi lịch trình hiện tại, ví dụ: đổi khách sạn, thêm nhà hàng).
    2. Travel Dates: Số ngày đi (ví dụ: '3 ngày 2 đêm', '2 ngày', 'không rõ'). Nếu intent là refine mà không nhắc đến ngày thì giữ nguyên là 'unchanged'.
    
    Ví dụ 1:
    User: Lên lịch trình đi Đà Nẵng 3 ngày 2 đêm
    Output: create | 3 ngày 2 đêm
    
    Ví dụ 2:
    User: Đổi cho tôi khách sạn rẻ hơn
    Output: refine | unchanged
    
    KHÔNG ĐƯỢC GIẢI THÍCH THÊM. CHỈ TRẢ VỀ CHUỖI THEO ĐÚNG ĐỊNH DẠNG TRÊN.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    response = llm.invoke(messages)
    content = response.content
    if isinstance(content, list):
        result_text = "".join(
            block["text"] if isinstance(block, dict) and "text" in block else (block if isinstance(block, str) else "") 
            for block in content
        ).strip()
    else:
        result_text = str(content).strip()
    
    logger.debug(f"Workflow Agent LLM Output: {result_text}")
    
    try:
        intent, travel_dates = [part.strip() for part in result_text.split("|")]
        state["intent"] = intent.lower()
        if travel_dates != "unchanged":
            state["travel_dates"] = travel_dates
    except Exception as e:
        logger.error(f"Lỗi parse kết quả từ Workflow Agent: {e}")
        state["intent"] = "create" # Mặc định
        
    logger.info(f"Kết quả phân tích: Intent={state.get('intent')}, Dates={state.get('travel_dates')}")
    return state
