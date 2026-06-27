# SALLMA Travel Planner

Dự án lên kế hoạch du lịch sử dụng kiến trúc **SALLMA (State-Aware Large Language Model Architecture)**, xây dựng với **LangGraph**, **Streamlit** và **Google Gemini**.

## Tính năng
- **Giao diện 1 cửa (Single-page UI)**: Tích hợp Chatbot, Lịch trình, Dự toán Chi phí và Bản đồ hiển thị song song.
- **Bản đồ Tuyến đường (PyDeck)**: Tự động trích xuất tọa độ từ dữ liệu JSON và vẽ đường nối (PathLayer) lộ trình di chuyển theo từng ngày.
- **Kiến trúc SALLMA bằng LangGraph**:
  - **Workflow Agent**: Phân tích ý định người dùng (Intent) dựa trên toàn bộ lịch sử hội thoại (Shared Memory).
  - **Research Agent**: RAG Agent chuyên kết nối với PostgreSQL `pgvector` để truy xuất địa điểm có thật (Hybrid Search). Hỗ trợ tìm kiếm thông minh bổ sung khi Refine.
  - **Planner Agent**: Agent lập kế hoạch thông minh, tự động tính toán số ngày lưu trú, điều chỉnh lịch trình, bắt buộc phải chọn đủ 3 bữa ăn/ngày, và không ảo giác.
  - **Budget Node**: Node toán học (Non-LLM) tính tổng chi phí chính xác tuyệt đối.
- **Database (PostgreSQL + pgvector)**: Lưu trữ dữ liệu thực và Vector Embeddings (Google `gemini-embedding-2`).

## 📊 Benchmark Results
Kết quả dưới đây được lấy trực tiếp từ các đợt benchmark gần nhất để so sánh giữa 3 kiến trúc:
1. **Single-Agent (No RAG)**: Bản gốc chạy trên tri thức tĩnh của LLM (không có Database grounding).
   - [benchmark_full_20260617_063715.json](benchmarks/results/benchmark_full_20260617_063715.json)
2. **Single-Agent (RAG)**: Bản Single-Agent được tích hợp công cụ `retrieve_places` để truy xuất DB.
   - [benchmark_single_rag_20260627_091510.json](benchmarks/results/benchmark_single_rag_20260627_091510.json)
3. **Multi-Agent (LangGraph)**: Hệ thống SALLMA chia các Agent Workflow, Research, Planner và Budget Node.
   - [benchmark_single_rag_20260627_091510.json](benchmarks/results/benchmark_single_rag_20260627_091510.json) (Phần Multi-Agent)

Báo cáo phân tích học thuật chi tiết: [BENCHMARK_ANALYSIS.md](docs/BENCHMARK_ANALYSIS.md)

Thiết lập chung:
- `30` create prompts
- `2` multi-turn sessions, mỗi session `10` turns
- latency suite với `5` concurrent simulated rooms
- text model: `gemini-3.1-flash-lite`

### Tóm tắt so sánh

| Tiêu chí | Single-Agent (No RAG) | Single-Agent (RAG) | Multi-Agent | Cách số liệu được tính toán |
|---|---:|---:|---:|---|
| **Correctness** (Đo độ xác thực địa danh) | `43.73%` | `98.55%` | `100.00%` | **Macro-average trên 30 cases**. Số địa danh thô khớp DB thực tế: No RAG: `109/249`, RAG: `228/231`, Multi-Agent: `435/435`. |
| **Hallucination** (Tỷ lệ địa danh ảo giác) | `56.27%` | `1.45%` | `0.00%` | Tính bằng `1 - verified_rate`. Số địa danh ảo giác thô: No RAG: `140/249`, RAG: `3/231`, Multi-Agent: `0/435`. |
| **Budget accuracy** (Lệch ngân sách trung bình) | `531,333 VND` | `204,000 VND` | `0 VND` | Trung bình của `budget_delta` trên 30 cases. Tổng sai số thô: No RAG: `15.94M VND`, RAG: `6.12M VND`, Multi-Agent: `0 VND` (do dùng Budget Node logic). |
| **Consistency** (Lỗi logic trong Create) | `0.20` lỗi/case | `0.23` lỗi/case | `4.60` lỗi/case | Bộ kiểm tra tự động đếm các lỗi logic cấu trúc (ví dụ: ngày/đêm không khớp, trùng địa điểm, di chuyển quá xa). Multi-Agent bị phạt nhiều hơn do sinh kế hoạch đầy đủ, chi tiết hơn. |
| **State retention** (Giữ trạng thái hội thoại) | `100%` pass | `100%` pass | `100%` pass | Pass rate trên 10 bài kiểm tra ở 2 session hội thoại 10 lượt. |
| **Consistency** (Lỗi logic trong 10-turn) | `0.5` lỗi/session | `1.0` lỗi/session | `7.0` lỗi/session | Bộ kiểm tra chạy trên trạng thái cuối cùng của 2 session nhiều lượt. |
| **Latency - Create** (Thời gian tạo) | `19.81s` | `44.29s` | `95.63s` | Trung bình `10` mẫu trong suite tải đồng thời. Tổng thời gian: No RAG: `198s`, RAG: `443s`, Multi-Agent: `956s`. |
| **Latency - Refine** (Thời gian chỉnh sửa) | `18.63s` | `43.88s` | `54.74s` | Trung bình `10` mẫu. Tổng thời gian: No RAG: `186s`, RAG: `439s`, Multi-Agent: `547s`. |
| **Latency - Budget** (Thời gian dự toán) | `19.57s` | `20.08s` | `0.00s` | Trung bình `10` mẫu. Multi-Agent dùng Python thuần nên gần như `0s`. |
| **Usefulness proxy** (Điểm hữu ích ước lượng) | `4.17/5` | `4.76/5` | `3.65/5` | Điểm tự động dựa trên độ chính xác và tính nhất quán (chưa phải khảo sát người dùng thực). |

### Diễn giải theo 6 tiêu chí đánh giá

1. **Correctness & Hallucination**
   * **No RAG**: Single-Agent không có cơ sở dữ liệu làm mốc tham chiếu sẽ ảo giác liên tục, đặt các địa danh không có thật lên tới `56.27%`.
   * **RAG**: Khi được tích hợp RAG, Single-Agent cải thiện ngoạn mục độ chính xác lên `98.55%` (228/231 địa điểm chuẩn).
   * **Multi-Agent**: Đạt độ chính xác tuyệt đối `100%` nhờ sự kiểm soát gắt gao của Research Agent trong LangGraph, cam kết không bịa địa danh.

2. **Budget accuracy**
   * **No RAG** bị lệch nhiều nhất do LLM làm toán nhầm lẫn.
   * **RAG** giúp Single-Agent lấy được giá phòng và giá vé chuẩn từ DB nên sai số giảm hơn 2.5 lần xuống `204,000 VND`.
   * **Multi-Agent** đạt sai số `0 VND` nhờ chuyển hẳn nhiệm vụ tính toán ngân sách từ LLM sang chương trình Python thuần túy (`Budget Node`).

3. **Consistency**
   * Cả hai bản Single-Agent (có và không có RAG) đều có số lỗi rất ít (`0.2` - `0.23` lỗi/case) do chúng có xu hướng tạo ra lịch trình ngắn gọn, ít hoạt động phụ.
   * Multi-Agent bị phạt nhiều lỗi hơn (`4.6` lỗi/case) do LangGraph sinh ra lịch trình dày đặc, chi tiết (4-6 hoạt động đầy đủ mỗi ngày theo đúng chuẩn), dẫn đến khả năng xuất hiện các lỗi cấu trúc tự động (ví dụ: khoảng cách từ hoạt động tới khách sạn >35km) tăng cao.

4. **Latency**
   * **No RAG** nhanh nhất do không tốn thời gian truy vấn DB hay định tuyến.
   * **RAG** làm Single-Agent chậm đi gấp đôi (tăng lên ~44s) vì phải thực hiện các vòng lặp gọi tool truy xuất Postgres.
   * **Multi-Agent** chậm nhất (~95s cho Create) vì chạy qua chuỗi LangGraph gồm 3 Agent LLM tuần tự cùng nhiều lượt gọi tool DB.

### Kết luận tổng quan

* **Single-Agent (No RAG)**: Chạy nhanh nhất nhưng không thể dùng trong thực tế do tỷ lệ ảo giác địa danh quá lớn (56.27%) và tính toán sai ngân sách.
* **Single-Agent (RAG)**: Là sự dung hòa xuất sắc giữa hiệu năng và độ chính xác. Nhờ RAG, hệ thống loại bỏ ảo giác, giữ được tốc độ phản hồi nhanh hơn gấp đôi so với Multi-Agent mà vẫn đảm bảo độ tin cậy của thông tin đạt 98.55%.
* **Multi-Agent**: Đạt độ hoàn thiện cao nhất về mặt nội dung (100% địa danh chính xác, 0 VND sai lệch ngân sách) nhưng đánh đổi bằng tài nguyên và độ trễ phản hồi (latency) rất cao.

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
   Tạo file `.env` tại thư mục gốc và thêm token của bạn (Database và LLM):
   ```env
   GOOGLE_API_KEY="Key Gemini của bạn (dùng cho Text Generation va Vector Embeddings)"
   SALLMA_TEXT_MODEL="gemini-3.1-flash-lite"
   DB_HOST="localhost"
   DB_PORT="5432"
   DB_NAME="travel_db"
   DB_USER="postgres"
   DB_PASSWORD="yourpassword"
   ```

4. **Khởi tạo dữ liệu:**
   Chạy script Seed để nạp dữ liệu mẫu vào PostgreSQL:
   ```bash
   python seed_db.py
   ```

5. **Khởi chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```

## Cấu trúc thư mục

```
travel_planner/
├── app.py                      # Giao diện Streamlit chính (PyDeck Map, Chat, Status Stream)
├── core/
│   ├── database.py             # Database Manager & Vector Search
│   ├── graph.py                # Cấu hình luồng chạy LangGraph
│   ├── logger.py               # Thiết lập ghi log hệ thống
│   └── state.py                # Định nghĩa Shared State (Memory) cho LangGraph
├── agents/
│   ├── workflow_agent.py       # Agent phân loại Intent từ History
│   ├── research_agent.py       # Agent RAG truy xuất dữ liệu từ Postgres
│   ├── planner_agent.py        # Agent lập kế hoạch và tối ưu Route
│   └── budget_node.py          # Hàm tính toán chi phí (Non-LLM)
├── tools/
│   └── travel_tools.py         # Khai báo Tool calling
├── docs/                       # Tài liệu thiết kế kiến trúc
├── .env                        # Biến môi trường (không commit)
├── .gitignore                  # Bỏ qua các file không cần thiết
├── requirements.txt            # Danh sách thư viện phụ thuộc
```

## Giấy phép
Dự án được phân phối dưới giấy phép MIT.
