# Lộ trình phát triển hệ thống

* *Phase 1 - Proof of Concept (Mock Database & UI)*: Xây dựng bộ khung LangGraph hoàn chỉnh. Sử dụng dữ liệu giả lập (Mock list of dictionaries) thay cho cơ sở dữ liệu thật để kiểm thử luồng đồng bộ giữa các Agent. Triển khai giao diện Streamlit cơ bản và hệ thống Logging để theo dõi Chain of Thought.

* *Phase 2 - RAG & Real Database Integration*: Thay thế Mock Database bằng PostgreSQL/pgvector. Cập nhật RAG Tool để thực hiện Hybrid Search (Vector Search + SQL Filter). Đảm bảo LLM chỉ dùng dữ liệu từ cơ sở dữ liệu.

* *Phase 3 - Deployment & Containerization*: Đóng gói mỗi Agent và Database thành các Docker container độc lập để chứng minh tính cô lập và khả năng chịu lỗi của kiến trúc SALLMA.  