# 12 Triết Lý Cốt Lõi Xây Dựng Skill Đa Ngành (Từ Đơn Giản Đến Phức Tạp)

## Mục 1. Nguyên Lý Nền Tảng Về Ngữ Cảnh & Bộ Nhớ AI (Triết lý 1 – 5)

### 1. Ngữ cảnh là tài sản chung (`Context Window Economy`)
> *"The context window is a public good. Only add context the model doesn't already have."* — OpenAI & Anthropic

- Mỗi đơn vị dữ liệu (*token*) nhồi vào `SKILL.md` = 1 đơn vị bị lấy mất khỏi khả năng suy luận của AI. Skill càng phình to vô ích, AI càng xử lý kém.
- **Quy tắc:** Chỉ viết những quy tắc chuyên biệt mà AI **không thể tự suy ra**. Kiến thức phổ thông AI đã biết sẵn → Xóa bỏ. Kiến thức chuyên sâu của dự án → Cất vào `references/` và chỉ nạp đúng phần cần dùng ở từng bước.

### 2. Tiết lộ dần 3 Tầng (`3-Level Progressive Disclosure`)
```text
Tầng 1: PHẦN MỞ ĐẦU YAML (name + description) → Luôn nằm trong bộ nhớ chờ (~50-100 từ)
Tầng 2: THÂN SKILL.md (Bộ điều hướng)         → Chỉ nạp khi skill được kích hoạt (≤ 150 dòng)
Tầng 3: TÀI NGUYÊN ĐÍNH KÈM (references/...)  → Chỉ nạp từng mục theo lệnh đọc ở từng bước
```
- AI chỉ nạp tầng sâu khi thật sự bước vào giai đoạn cần kiến thức đó. Không bao giờ bắt AI đọc cả cuốn bách khoa toàn thư chỉ để làm Bước 1.

### 3. Giải thích lý do Nhân – Quả (`Explain the Why`)
- Thay vì dùng chữ in hoa kèm dấu chấm than (`BẮT BUỘC!!! TUYỆT ĐỐI KHÔNG!!!`), hãy giải thích ngắn gọn **nguyên nhân – hậu quả** (*"Làm X vì nếu không sẽ gây ra lỗi Y ở bước sau"*).
- Khi AI hiểu **tại sao** có quy tắc đó, nó sẽ tự biết cách xử lý thông minh khi gặp các tình huống biên ngoài dự kiến.

### 4. Đặt mức độ tự do khớp với độ rủi ro (`Calibrated Degrees of Freedom`)
| Mức tự do | Khi nào áp dụng (Đa ngành) | Cách thiết kế trong Skill |
| :--- | :--- | :--- |
| **Thấp** *(Khóa cứng bằng khuôn mẫu & code)* | Sai 1 thông số là hỏng toàn bộ hệ thống (VD: Xuất file kỹ thuật JSON/XML, tính toán tài chính, kiểm toán dữ liệu). | Ép dùng `templates/` cố định + chạy `scripts/` kiểm tra tự động. |
| **Trung bình** *(Có khung chuẩn + nhánh lựa chọn)* | Có quy trình chuẩn nhưng cần tùy biến theo từng loại đối tượng (VD: Phân tích đối thủ, lập kế hoạch dự án, soạn thảo tài liệu). | Dùng Cây quyết định (`Decision Tree`) + bảng quy tắc `Nếu X → Thì Y`. |
| **Cao** *(Định hướng bằng nguyên lý & rào chắn)* | Bài toán sáng tạo mở, nhiều phương án đều đúng (VD: Tìm ý tưởng mới, thiết kế concept, đề xuất chiến lược). | Dùng quy trình Phân kỳ → Hội tụ + Danh sách Cấm mặc định (`Banned Defaults`). |

### 5. Mô tả (`description`) = Bộ lọc kích hoạt duy nhất
- Trường `description` trong YAML ở đầu `SKILL.md` là nơi duy nhất hệ thống đọc để quyết định có gọi skill này hay không.
- Bắt buộc ghi rõ 3 thông tin: **Làm gì (`WHAT`)** + **Khi nào dùng (`WHEN`)** + **Từ khóa kích hoạt (`Trigger: /tên-lệnh`)**.

---

## Mục 2. Kiến Trúc Vận Hành & Tách Bạch Trách Nhiệm (Triết lý 6 – 9)

### 6. Phân Biệt Chế Độ Vận Hành: Skill Độc Lập (`Standalone`) vs. Skill Dây Chuyền (`Pipeline`)
Trước khi thiết kế bất kỳ skill nào, phải xác định rõ nó đứng một mình hay nằm trong một chuỗi nhiều skill nối tiếp:
- **Nếu là Skill Độc Lập (`Standalone Skill`):** Nhận đầu vào trực tiếp từ câu lệnh hoặc tài liệu người dùng đưa vào. Đặt **Điểm dừng cứng (`Hard Gates`)** tại các bước chốt phương án quan trọng (từ 1 đến 3 cổng tùy độ phức tạp) để người dùng duyệt trước khi đi sâu.
- **Nếu là Skill Dây Chuyền (`Pipeline Skill` — Học từ `Remotion` & `HeyGen`):** Không bao giờ hỏi lại người dùng những thông tin đã có sẵn ở bước trước. Đặt **Bảng Kiểm Tra Trạng Thái Ổ Cứng (`State-Driven Entry Table`)** ngay đầu `SKILL.md`: Nếu đã có file đầu ra của giai đoạn trước → đọc thẳng file đó và chạy ngay; đồng thời khóa chặt định dạng file đầu ra để giai đoạn kế tiếp đọc không bị lỗi.

### 7. Phân Tách Tuyệt Đối 3 Loại File (`Strict 3-Tier Separation of Concerns` — Edsger Dijkstra)
Lỗi lớn nhất khiến các skill bị rối loạn là trộn lẫn nhiệm vụ giữa các file. Bắt buộc tuân thủ ranh giới bất khả xâm phạm sau:
1. **`SKILL.md` = BỘ ĐIỀU HƯỚNG THUẦN TÚY (`Pure Router & Orchestrator`):** Chỉ chứa Kiểm tra đầu vào, các Bước thực thi, Lệnh đọc phẫu thuật (`File + Mục + Dòng + Lý do`), Checklist Cổng chất lượng và Điểm dừng cứng (`Hard Gates`). **CẤM** viết lý thuyết chuyên môn dài dòng và **CẤM** chép khung đầu ra vào `SKILL.md`.
2. **`references/*.md` = SÁCH HƯỚNG DẪN CHUYÊN MÔN (`Pure Knowledge Manual`):** Chỉ chứa công thức, bảng quy tắc, tiêu chí chấm điểm chia theo Đầu mục (`## Mục 1`, `## Mục 2`) có ranh giới dòng rõ ràng. **CẤM** điều phối quy trình (`Bước 1, Bước 2`) và **CẤM** chứa đường dẫn `file:///` trỏ ra ngoài thư mục skill.
3. **`templates/*.md` = KHUNG DỮ LIỆU ĐẦU RA SẠCH (`Pure Output Schema`):** Chỉ chứa cấu trúc trường dữ liệu đầu ra và các ô điền ngắn gọn `[Điền ...]`. **CẤM** nhét lời dạy bảo, giải thích lý thuyết hay câu nhắc việc vào `templates/` (để file kết quả sinh ra sạch 100%, sẵn sàng bàn giao).

### 8. Điều Hướng Đọc Phẫu Thuật Theo Mục & Khoảng Dòng (`4-Part Surgical Read Pointers`)
- Nếu `SKILL.md` chỉ ghi chung chung *"→ Đọc `references/file-a.md`"*, AI sẽ nạp toàn bộ các file tham chiếu cùng lúc gây tràn bộ nhớ (*Token Limit*) và loãng sự chú ý (*Lost-in-the-Middle*), dẫn đến làm việc và kiểm tra qua loa.
- **Quy tắc bắt buộc:** Mọi lệnh đọc trong `SKILL.md` phải ghi đủ **4 thành phần**:
  1. **Khi nào đọc (`When`):** Đọc ở Bước nào / Nhánh nào.
  2. **Đọc ở đâu (`Where`):** Tên file + **Từ `Mục X` đến `Mục Y` (`StartLine: AA` → `EndLine: BB`)**.
  3. **Giới hạn loại trừ (`Exclusion`):** Ghi rõ những mục/file **CHƯA ĐƯỢC ĐỌC** ở bước đó.
  4. **Tại sao đọc (`Why`):** Đọc để lấy công thức/bảng dữ liệu gì phục vụ hành động nào.

### 9. Giao Việc Toán Học Cho Code (`Software 1.0`), Giao Việc Suy Luận Cho AI (`Software 2.0` — Andrej Karpathy)
> *"Never ask an LLM to do arithmetic, count lengths, parse 100 files, or lint JSON by eye when a Python script can do it with 100% precision."*

- Mô hình ngôn ngữ (LLM) rất giỏi phân tích chiến lược, sáng tạo nội dung, suy luận ngữ nghĩa; nhưng rất hay sai khi đếm ký tự, cộng trừ số liệu lớn, quét hàng loạt file hoặc kiểm tra cú pháp định dạng.
- Bất kỳ tác vụ nào cần **quét dữ liệu đầu vào lớn (`Scanner`)**, **tính toán/biên dịch kỹ thuật (`Engine`)**, hoặc **kiểm tra tiêu chuẩn định lượng (`Validator`)** đều phải được viết thành **Script chạy tự động trong `scripts/`**.

---

## Mục 3. Chống Bệnh Hình Thức — Làm Đặc Ruột & Chọn Đúng Cấp Độ (Triết lý 10 – 12)

### 10. Không Đồng Phục Hóa — Chọn Đúng Cấp Độ Phức Tạp (`Cấp 1 → 4`) & Hình Mẫu Chức Năng (`Hình mẫu 1 → 6`)
- Cấm dùng một cấu trúc thư mục rập khuôn cho mọi bài toán.
- Bài toán nhỏ (< 100 dòng quy tắc) chỉ làm **Cấp độ 1** (1 file `SKILL.md` duy nhất). Bài toán chuẩn làm **Cấp độ 2**. Bài toán đa nhánh đối tượng làm **Cấp độ 3** (`references/core/` + `references/types/`). Bài toán xử lý dữ liệu lớn/kỹ thuật nặng làm **Cấp độ 4** (có hệ thống `scripts/` 3 tầng `scanners/engines/validators` và `config/`).

### 11. Diệt Trừ Tính Từ Mơ Hồ & Khóa Danh Sách Cấm Mặc Định (`Zero-Adjective & Banned Defaults` — HeyGen)
- Những tính từ cảm tính (*"viết chuyên nghiệp, phân tích sâu sắc, tối ưu tốt, trình bày đẹp"*) là nguyên nhân số 1 khiến sản phẩm của AI trở nên rập khuôn, công nghiệp và vô hồn.
- **Quy tắc bắt buộc khi viết nội dung chuyên môn (`Ruột`):**
  1. Quy đổi mọi tính từ cảm tính thành **Con số định lượng, Công thức tính hoặc Điều kiện kiểm chứng được** (VD: thay *"viết tiêu đề ngắn gọn"* bằng *"từ 50–80 ký tự, chia 2 vế ngăn cách bởi dấu hai chấm hoặc gạch ngang"*).
  2. Luôn lập mục **`DANH SÁCH CẤM MẶC ĐỊNH (BANNED DEFAULTS)`** (Tư duy ngược Charlie Munger) để chặn đứng các thói quen lười biếng, sáo rỗng mặc định của AI trong lĩnh vực đó.

### 12. Bản Chất Quan Trọng Hơn Hiện Tượng (`Substance Over Cargo-Cult Form`)
- Tạo ra nhiều thư mục (`core/`, `types/`, `scripts/`, `config/`) chỉ là **Hiện tượng (Cái Vỏ)**.
- **Bản chất (Cái Ruột)** quyết định skill chạy tốt hay không nằm ở 2 chỗ:
  1. **Mật độ tri thức trong `references/`:** Phải là bảng quy tắc `Nếu X → Thì Y`, công thức định lượng, và cặp ví dụ `✅ Đúng / ❌ Sai` thực tế — tuyệt đối không phải những đoạn văn xuôi giáo điều chung chung.
  2. **Cơ chế phối hợp thực sự:** `SKILL.md` phải điều hướng nạp đúng nhánh tài liệu cần thiết (không nạp tràn lan), và `scripts/` phải thực sự chạy kiểm toán/xử lý dữ liệu bằng toán học chứ không phải file làm cảnh.
