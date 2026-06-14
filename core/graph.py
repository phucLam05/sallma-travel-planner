from langgraph.graph import StateGraph, START, END
from core.state import TravelState
from agents.workflow_agent import workflow_node
from agents.itinerary_agent import itinerary_node
from agents.accommodation_agent import accommodation_node
from core.logger import get_logger

logger = get_logger("Graph")

def route_intent(state: TravelState):
    """
    Hàm định tuyến (Conditional Edge) để quyết định bước tiếp theo dựa trên intent.
    """
    intent = state.get("intent", "create")
    if intent == "create":
        logger.info("Routing: Intent là CREATE -> Itinerary Agent")
        return "itinerary"
    elif intent == "refine":
        logger.info("Routing: Intent là REFINE -> Cập nhật lại lịch trình hoặc khách sạn")
        # Trong MVP này, chúng ta cho chạy lại từ Itinerary để sửa đổi
        return "itinerary"
    else:
        logger.warning("Routing: Không rõ intent, mặc định -> Itinerary Agent")
        return "itinerary"

def build_graph():
    """
    Xây dựng luồng xử lý bằng LangGraph.
    """
    logger.info("Đang khởi tạo StateGraph...")
    builder = StateGraph(TravelState)

    # Đăng ký các Node (các Agent)
    builder.add_node("workflow", workflow_node)
    builder.add_node("itinerary", itinerary_node)
    builder.add_node("accommodation", accommodation_node)

    # Đăng ký các Edge (luồng chuyển)
    builder.add_edge(START, "workflow")
    
    # Định tuyến có điều kiện từ Workflow -> Itinerary hoặc luồng khác
    builder.add_conditional_edges("workflow", route_intent, {
        "itinerary": "itinerary"
    })
    
    # Tiếp tục luồng tuyến tính: Itinerary -> Accommodation -> END
    builder.add_edge("itinerary", "accommodation")
    builder.add_edge("accommodation", END)

    # Biên dịch đồ thị
    graph = builder.compile()
    logger.info("Đã compile thành công StateGraph.")
    return graph
