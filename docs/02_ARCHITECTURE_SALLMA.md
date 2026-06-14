# Kiến trúc Hệ thống (Operational Layer)

* *Shared Memory (Data for Memory for Persistence)*: Được định nghĩa bằng TypedDict của LangGraph (TravelState). Lưu trữ toàn bộ ngữ cảnh bao gồm yêu cầu người dùng, ngày đi, lịch trình tạm thời, thông tin khách sạn và tổng chi phí.

* *Intent/Workflow Management Agent*: Agent cổng vào, chịu trách nhiệm đọc tin nhắn của người dùng và xác định mục đích là tạo mới lịch trình (create) hay chỉnh sửa lịch trình hiện tại (refine).  

* *Itinerary Agent (Specialized Agent 1)*: Chuyên trách lập lịch trình điểm đến. Bắt buộc không được ảo giác (hallucination) mà phải gọi công cụ RAG để truy xuất địa điểm có thật từ cơ sở dữ liệu.

* *Accommodation Agent (Specialized Agent 2)*: Chuyên trách tìm khách sạn dựa trên điểm đến và số ngày lưu trú. Bắt buộc gọi công cụ RAG để lấy giá phòng thật và gọi Tool tính toán chi phí.

* *Place Retrieval Tool (RAG Tool)*: Công cụ dùng để kéo dữ liệu từ cơ sở dữ liệu.

* *Budgeting Tool (Non-LLM Tool)*: Công cụ tính toán chi phí bằng thuật toán toán học truyền thống, đảm bảo độ chính xác tuyệt đối.