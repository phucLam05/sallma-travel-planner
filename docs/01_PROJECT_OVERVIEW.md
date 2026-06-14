# AI Travel Planner - Dự án áp dụng kiến trúc SALLMA
* *Mục tiêu dự án*: Chuyển đổi hệ thống lên kế hoạch du lịch từ kiến trúc Backend-Orchestrated tuyến tính sang kiến trúc Multi-Agent-Orchestrated (SALLMA).

* *Triết lý SALLMA áp dụng*: Giải quyết bài toán thiếu bộ nhớ liên tục và ảo giác của mô hình ngôn ngữ lớn (LLM) bằng cách chia nhỏ tác vụ cho các Agent chuyên biệt.

* *Điểm khác biệt*: Hệ thống không sử dụng các luồng if/else cứng nhắc để quản lý trạng thái cập nhật (ví dụ: đổi ngày đi). Các Agent sẽ giao tiếp gián tiếp qua một Bộ nhớ chung (Shared State).

* *Giới hạn tính năng (MVP)*: Hệ thống chỉ tập trung vào việc tạo lịch trình, tìm kiếm khách sạn, tính toán chi phí tổng thể và xử lý các yêu cầu thay đổi (Refine) từ người dùng.

* *Công nghệ lõi*: Sử dụng Python, LangGraph để quản lý luồng, Streamlit cho giao diện UI và mô hình Gemini 2.5 Flash để suy luận.