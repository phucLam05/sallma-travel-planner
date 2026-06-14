import streamlit as st
from dotenv import load_dotenv
import os

# Nạp biến môi trường từ .env
load_dotenv()

from core.graph import build_graph
from core.state import TravelState

st.set_page_config(page_title="SALLMA Travel Planner", layout="wide")

# Hàm khởi tạo LangGraph
@st.cache_resource
def get_travel_graph():
    return build_graph()

graph = get_travel_graph()

# Tiêu đề ứng dụng
st.title("✈️ SALLMA Travel Planner (Phase 1)")
st.markdown("Hệ thống lên kế hoạch du lịch sử dụng kiến trúc Multi-Agent (LangGraph & Gemini).")

# Khởi tạo state trong Streamlit
if "travel_state" not in st.session_state:
    st.session_state.travel_state = TravelState(
        chat_history=[],
        latest_user_input="",
        intent="",
        travel_dates="",
        itinerary_plan="",
        accommodation_details="",
        total_cost=0.0
    )

# Chia layout thành 2 cột chính
col_chat, col_result = st.columns([1, 2])

with col_chat:
    st.header("Trò chuyện & Yêu cầu")
    
    # Hiển thị lịch sử hội thoại (rất cơ bản)
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.travel_state.get("chat_history", []):
            role = msg.get("role", "User")
            st.markdown(f"**{role}**: {msg.get('content')}")
            
    # Ô nhập liệu
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Nhập yêu cầu (VD: Lên lịch trình Đà Nẵng 3 ngày 2 đêm, đổi khách sạn...)")
        submit_button = st.form_submit_button("Gửi")

with col_result:
    st.header("Kết quả Lịch trình")
    
    # Các tab hiển thị kết quả
    tab1, tab2 = st.tabs(["Lịch trình Tham quan", "Khách sạn & Chi phí"])
    
    with tab1:
        st.markdown(st.session_state.travel_state.get("itinerary_plan", "Chưa có lịch trình nào được tạo."))
        
    with tab2:
        st.markdown(st.session_state.travel_state.get("accommodation_details", "Chưa có thông tin khách sạn."))


# Xử lý khi người dùng ấn nút Gửi
if submit_button and user_input:
    # Cập nhật state
    st.session_state.travel_state["latest_user_input"] = user_input
    
    # Thêm tin nhắn user vào lịch sử
    current_history = st.session_state.travel_state.get("chat_history", [])
    current_history.append({"role": "User", "content": user_input})
    st.session_state.travel_state["chat_history"] = current_history
    
    with st.spinner("Hệ thống đang xử lý qua các Agent..."):
        # Chạy LangGraph
        try:
            # Truyền state hiện tại vào graph
            final_state = graph.invoke(st.session_state.travel_state)
            
            # Cập nhật state mới vào session_state
            st.session_state.travel_state = final_state
            
            # Thêm tin nhắn hệ thống báo thành công
            st.session_state.travel_state["chat_history"].append({
                "role": "System", 
                "content": f"Đã cập nhật yêu cầu. Intent nhận diện: {final_state.get('intent')}. Số ngày: {final_state.get('travel_dates')}"
            })
            
            # Rerun để cập nhật UI
            st.rerun()
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")
