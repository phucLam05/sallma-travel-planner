# SALLMA Travel Planner (Phase 1)

Dự án lên kế hoạch du lịch sử dụng kiến trúc **SALLMA (Single Agent, Large Language Model Architecture - hoặc Multi-Agent tùy ngữ cảnh)**, xây dựng với **LangGraph**, **Streamlit** và **Gemini**.

## Tính năng (Phase 1 - PoC)
- Giao diện chat tương tác với Streamlit.
- Kiến trúc Multi-Agent bằng LangGraph:
  - **Workflow Agent**: Phân tích yêu cầu người dùng (Tạo mới hoặc Chỉnh sửa).
  - **Itinerary Agent**: Lên lịch trình tham quan, ăn uống.
  - **Accommodation Agent**: Tìm khách sạn, tính toán chi phí.
- Tích hợp công cụ (Tool calling) giả lập RAG từ cơ sở dữ liệu ảo về Đà Nẵng.

## Cài đặt và Chạy thử nghiệm

1. **Clone repository:**
   ```bash
   git clone <URL_REPO_CUA_BAN>
   cd travel_planner
   ```

2. **Cài đặt môi trường:**
   Tạo môi trường ảo (khuyến nghị) và cài đặt các gói phụ thuộc:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Cấu hình API Key:**
   Tạo file `.env` tại thư mục gốc và thêm khóa API Gemini của bạn:
   ```env
   GEMINI_API_KEY="Điền API key của bạn vào đây"
   ```

4. **Khởi chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```

## Cấu trúc thư mục

```
travel_planner/
├── app.py                      # Giao diện Streamlit chính
├── core/
│   ├── database.py             # Database Manager & Mock Data
│   ├── graph.py                # Cấu hình luồng chạy LangGraph
│   ├── logger.py               # Thiết lập ghi log hệ thống
│   └── state.py                # Định nghĩa shared State cho LangGraph
├── agents/
│   ├── workflow_agent.py       # Agent phân tích intent
│   ├── itinerary_agent.py      # Agent lên lịch trình
│   └── accommodation_agent.py  # Agent khách sạn và chi phí
├── tools/
│   └── travel_tools.py         # Công cụ (Tool calling)
├── docs/                       # Tài liệu thiết kế kiến trúc
├── .env                        # Biến môi trường (không commit)
├── .gitignore                  # Bỏ qua các file không cần thiết
└── requirements.txt            # Danh sách thư viện phụ thuộc
```

## Giấy phép
Dự án được phân phối dưới giấy phép MIT.
