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
Kết quả dưới đây được lấy trực tiếp từ full benchmark gần nhất:
- JSON: [benchmark_single_rag_20260627_091510.json](benchmarks/results/benchmark_single_rag_20260627_091510.json)
- Markdown: [benchmark_single_rag_20260627_091510.md](benchmarks/results/benchmark_single_rag_20260627_091510.md)
- Academic write-up: [BENCHMARK_ANALYSIS.md](docs/BENCHMARK_ANALYSIS.md)

Thiết lập chạy:
- `30` create prompts
- `2` multi-turn sessions, mỗi session `10` turns
- latency suite với `5` concurrent simulated rooms
- text model: `gemini-3.1-flash-lite`

### Tóm tắt so sánh

| Criterion | Single-Agent (RAG) | Multi-Agent | How the number is produced |
|---|---:|---:|---|
| Correctness | `98.55%` verified rate | `100.00%` verified rate | Kết quả này là **macro-average trên 30 cases**. Single-agent (RAG) có `228` địa điểm verified trên `231` địa điểm sinh ra tổng cộng; multi-agent có `435/435`. Tuy nhiên số công bố `98.55%` và `100.00%` được tính theo `mean(case_verified_rate)` chứ không phải gộp toàn bộ địa điểm rồi chia một lần. |
| Hallucination | `1.45%` | `0.00%` | Cũng là **macro-average trên 30 cases** với công thức `hallucination_rate = 1 - verified_rate`. Tính theo tổng raw counts thì single-agent (RAG) có `3/231` địa điểm không verify được, còn multi-agent là `0/435`. |
| Budget accuracy | `204,000 VND` average delta | `0 VND` average delta | Benchmark tính `budget_delta = abs(claimed_total_cost - recomputed_total_cost)` cho từng case, rồi lấy trung bình trên `30` cases. Tổng sai số raw của single-agent (RAG) là `6,120,000 VND`, chia `30` ra `204,000 VND`; multi-agent có tổng sai số `0 VND`. |
| Consistency (create cases) | `0.23` violations/case | `4.6` violations/case | Bộ kiểm tra consistency đếm các lỗi như `nights_mismatch`, `time_order`, `missing_coordinates`, `duplicate_activity`, `route_distance`. Single-agent (RAG) có tổng `7` violations trên `30` create cases nên trung bình `0.23`; multi-agent có `138/30 = 4.6`. |
| State retention | `100%` pass rate | `100%` pass rate | Có `2` session, mỗi session có `5` checks, nên tổng là `10/10` checks passed cho cả hai hệ. Công thức là `state_retention_pass_rate = passed_checks / total_checks`. |
| Consistency (10-turn sessions) | `1.0` violations/session | `7.0` violations/session | Sau khi hoàn tất `2` session nhiều lượt, benchmark chạy lại consistency checker trên state cuối cùng. Single-agent (RAG) có tổng `2` violations trên `2` session nên ra `1.0`; multi-agent có `14/2 = 7.0`. |
| Latency - Create | `44.285s` | `95.627s` | Đây là trung bình của `10` samples trong latency suite dưới `5` concurrent simulated rooms. Tổng thời gian cộng dồn xấp xỉ là `442.85s` cho single-agent (RAG) và `956.27s` cho multi-agent. |
| Latency - Refine | `43.882s` | `54.740s` | Trung bình của `10` samples. Tổng thời gian cộng dồn xấp xỉ là `438.82s` cho single-agent (RAG) và `547.40s` cho multi-agent. |
| Latency - Budget | `20.079s` | `0.000s` | Trung bình của `10` samples. Tổng thời gian cộng dồn xấp xỉ là `200.79s` cho single-agent (RAG); multi-agent dùng `Budget Node` Python thuần nên gần như `0s` trên mọi sample. |
| User-perceived usefulness (proxy) | `4.76/5` | `3.65/5` | Đây là **automated proxy**, không phải questionnaire thật. Single-agent (RAG) có tổng điểm raw `142.8` trên `30` cases nên trung bình `4.76`; multi-agent có `109.5/30 = 3.65`. |

### Diễn giải theo 6 tiêu chí đánh giá

1. **Correctness**
   Benchmark đã phủ tiêu chí này trực tiếp. Con số `98.55%` và `100.00%` là **trung bình theo từng case** của tỷ lệ địa điểm được đối chiếu thành công với knowledge base thật trong database. Raw counts tương ứng là `228/231` địa điểm cho single-agent (RAG) và `435/435` cho multi-agent. Nhờ có RAG, Single-Agent đã cải thiện vượt bậc tỷ lệ chính xác từ mức dưới `45%` ở phiên bản không có RAG lên đến `98.55%`, tiệm cận mức hoàn hảo `100%` của Multi-Agent.

2. **Budget accuracy**
   Benchmark đã phủ trực tiếp. Single-agent (RAG) có tổng sai số `6,120,000 VND` trên `30` cases nên lệch trung bình `204,000 VND` (đã giảm đáng kể so với mức lệch hơn `500,000 VND` khi không có RAG), còn multi-agent lệch `0 VND` vì tổng chi phí cuối được tính bởi `Budget Node` deterministic thay vì để LLM tự cộng.

3. **Consistency**
   Benchmark đã phủ bằng một bộ luật kiểm tra tự động. Bộ đo hiện tại xem contradiction là các lỗi cấu trúc và logic giữa itinerary, route, hotel và budget metadata. Ở create benchmark, raw totals là `7` violations cho single-agent (RAG) và `138` cho multi-agent. Lý do Multi-Agent bị nhiều lỗi hơn là do hệ thống Multi-Agent tạo ra các lịch trình phức tạp và đầy đủ thông tin địa điểm chi tiết hơn, dẫn đến tăng xác suất dính các lỗi phạt tự động (ví dụ: khoảng cách giữa các điểm vui chơi quá 35km).

4. **State retention**
   Benchmark đã phủ bằng `2` hội thoại nhiều lượt, mỗi hội thoại `10` turns. Cả hai hệ đều đạt `10/10` checks passed, tương đương `100%` pass rate trong bộ kiểm tra giữ trạng thái.

5. **Latency**
   Benchmark đã phủ trực tiếp bằng latency suite chạy đồng thời `5` group rooms mô phỏng, tách riêng `Create`, `Refine`, `Budget`. Mỗi workflow có `10` samples. Khi tích hợp thêm RAG, Single-Agent (RAG) phải tốn thêm thời gian gọi cơ sở dữ liệu nên thời gian phản hồi tăng lên mức `44.285s` (Create) và `43.882s` (Refine). Tuy nhiên, nó vẫn nhanh hơn đáng kể so với Multi-Agent (`95.627s` cho Create) do không phải chạy qua chuỗi LangGraph tuần tự.

6. **User-perceived usefulness**
   Benchmark mới chỉ phủ một phần. Giá trị `4.76/5` và `3.65/5` hiện là **proxy tự động**, chưa phải khảo sát Likert thật từ người dùng. Việc Single-Agent (RAG) có điểm proxy cao hơn là do hệ thống này có ít lỗi consistency hơn trong các bài kiểm tra tự động.

### Kết luận ngắn

Benchmark cho thấy khi cả hai hệ thống đều sử dụng RAG:
- Cả **Single-Agent (RAG)** và **Multi-Agent** đều đạt độ chính xác địa danh cực kỳ cao (tiệm cận và đạt `100%`). Việc ảo giác địa danh gần như đã được giải quyết triệt để nhờ cơ chế RAG.
- **Multi-Agent** vẫn vượt trội tuyệt đối về tính chính xác của hóa đơn (`Budget accuracy` đạt sai số `0 VND` nhờ Budget Node deterministic).
- **Single-Agent (RAG)** có lợi thế rất lớn về mặt tốc độ phản hồi (nhanh hơn khoảng gấp đôi so với Multi-Agent) và cấu trúc đơn giản hơn, đồng thời ghi nhận ít lỗi consistency tự động hơn.

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
└── requirements.txt            # Danh sách thư viện phụ thuộc
```

## Giấy phép
Dự án được phân phối dưới giấy phép MIT.
