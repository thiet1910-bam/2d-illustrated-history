# Ma Trận Phân Luồng File & Quy Tắc Tổ Chức Thư Mục (Cấp 1 → Cấp 4)

## Mục 1. Hệ Thống Thư Mục Chuẩn & Luật Phân Tách Tuyệt Đối (`Strict Separation of Concerns`)

### 1.1. Bảng Nhiệm Vụ Độc Quyền Của Từng Loại File (Chống Chồng Chéo)

| Thư mục / File | Xuất hiện ở Cấp độ | AI làm gì với file? | Nhiệm vụ DUY NHẤT được phép | ❌ CẤM TUYỆT ĐỐI (Chống chồng chéo nhiệm vụ) |
| :--- | :-: | :--- | :--- | :--- |
| **`SKILL.md`** | Cấp 1, 2, 3, 4 | **ĐIỀU HƯỚNG** quy trình | Định tuyến đầu vào, chỉ huy từng Bước, chỉ rõ **Đọc file nào + Mục nào + Dòng nào (`StartLine–EndLine`) + Tại sao đọc**, đặt Checklist & Điểm dừng cứng (`Gate`). *(Riêng Cấp 1 chứa luôn quy tắc ngắn < 100 dòng)*. | ❌ CẤM giảng giải lý thuyết dài dòng (ở Cấp 2–4); CẤM chép khung đầu ra vào `SKILL.md`. |
| **`references/`** *(Phẳng)* | Cấp 2, 4 | **ĐỌC** theo từng bước | Chứa 100% kiến thức chuyên môn, công thức định lượng, bảng quy tắc `Nếu X → Thì Y`, tiêu chí chấm điểm chia theo Đầu mục (`## Mục 1`, `## Mục 2`). | ❌ CẤM điều phối quy trình (`Bước 1, Bước 2`); CẤM chứa đường dẫn `file:///` trỏ ra ngoài skill; CẤM viết văn xuôi sáo rỗng. |
| **`references/core/`** + **`references/types/`** | Cấp 3 *(Đa nhánh)* | **ĐỌC** chọn lọc (`core/` + 1 file `types/`) | `core/` chứa **Luật Bất Biến** (áp dụng cho mọi nhánh). `types/` chứa **Luật Biến Thiên** (mỗi file = 1 loại đối tượng/ngành hàng/chế độ riêng biệt). | ❌ CẤM lặp lại nội dung của `core/` vào trong `types/`; CẤM ra lệnh đọc toàn bộ thư mục `types/` cùng lúc. |
| **`config/`** | Cấp 3, 4 *(Tùy chọn)* | **ĐỌC / NẠP** tham số | Chứa các file cấu hình tĩnh (`.json`, `.yaml`) lưu ngưỡng số học, danh sách từ khóa, thông số môi trường để dễ thay đổi mà không cần sửa code hay prompt. | ❌ CẤM viết hướng dẫn bằng lời văn vào `config/`. |
| **`templates/`** | Cấp 2, 3, 4 | **LÀM THEO** khi xuất kết quả | Chỉ chứa **Khung dữ liệu đầu ra thuần túy (`Pure Output Schema`)** và các ô trống `[Điền ...]`. | ❌ CẤM nhét lời hướng dẫn cách làm, lý thuyết, ghi chú nhắc việc hay nhãn `← CỐ ĐỊNH / ← THAY ĐỔI` vào trong `templates/`. |
| **`scripts/`** *(1 file hoặc chia 3 nhóm `scanners/`, `engines/`, `validators/`)* | Cấp 2, 3, 4 | **CHẠY** bằng dòng lệnh | Chứa code chạy thật (`Python/Bash/JS`):<br>• `scanners/`: Quét dữ liệu thô lớn → xuất `manifest.json`.<br>• `engines/`: Tính toán nặng / biên dịch sản phẩm.<br>• `validators/`: Kiểm toán định lượng tự động (`Code Gate`). | ❌ CẤM đặt mã giả (pseudo-code) không chạy được vào `scripts/`; CẤM viết script chỉ in dòng chữ hình thức mà không kiểm tra thật. |
| **`assets/`** & **`examples/`** | Tùy chọn | **NHÚNG** hoặc **ĐỌC MẪU** | `assets/`: Phông chữ, ảnh, logo nhúng vào sản phẩm.<br>`examples/`: Cặp ví dụ Đầu vào → Đầu ra hoàn chỉnh mẫu. | ❌ CẤM trộn lẫn với kiến thức quy tắc trong `references/`. |

---

## Mục 2. Chuẩn Cú Pháp Lệnh Đọc Phẫu Thuật & Cây Quyết Định Phân Luồng

### 2.1. Chuẩn Cú Pháp Lệnh Đọc Phẫu Thuật 4 Thành Phần (`4-Part Surgical Read Pointer`)
Trong `SKILL.md` (từ Cấp độ 2 trở lên), mọi lệnh trỏ sang `references/` ở từng Bước bắt buộc phải ghi rõ **Khi nào đọc + File/Mục/Khoảng Dòng (`StartLine–EndLine`) + Giới hạn loại trừ + Tại sao đọc**:

```markdown
- **📖 Lệnh đọc tài liệu Bước X:**
  - **Khi nào đọc:** Ngay khi bắt đầu Bước X (thuộc Luồng/Nhánh Y).
  - **Đọc ở đâu:** `references/ten-file.md` — **Từ `Mục 1` đến `Mục 2` (`StartLine: 1` → `EndLine: 68`)**. *(Giới hạn loại trừ: Không đọc Mục 3 và chưa đọc các file khác ở bước này)*.
  - **Tại sao đọc:** Để lấy [tên bảng quy tắc / công thức định lượng cụ thể] phục vụ cho [hành động cụ thể của Bước X].
```

### 2.2. Cây Quyết Định Phân Luồng File Khi Thiết Kế Skill (Hỏi 4 Câu)
```text
Câu 1: Hệ thống làm gì với file này?
├─ CHẠY bằng lệnh máy tính để quét dữ liệu, tính toán hoặc kiểm toán ──► Đặt vào scripts/
├─ ĐỌC tham số cấu hình tĩnh (.json/.yaml) để truyền vào script/prompt ──► Đặt vào config/
├─ LÀM THEO khung định dạng để điền dữ liệu kết quả bàn giao ──────────► Đặt vào templates/
├─ NHÚNG trực tiếp vào sản phẩm (ảnh, font, biểu mẫu tĩnh) ────────────► Đặt vào assets/
└─ ĐỌC để nắm công thức, quy tắc chuyên môn ───────────────────────────► Sang Câu 2

Câu 2: Tổng lượng quy tắc chuyên môn của toàn bộ Skill dài bao nhiêu?
├─ Ngắn (< 100 dòng) và chỉ có 1 nhiệm vụ đơn giản ──► Viết thẳng vào SKILL.md (Cấp độ 1)
└─ Dài (≥ 100 dòng) hoặc có nhiều bước ──────────────► Sang Câu 3

Câu 3: Các quy tắc này áp dụng chung cho mọi trường hợp hay chia theo từng loại đối tượng?
├─ Áp dụng tuần tự theo từng Bước (Mọi trường hợp đều đi qua) ──► Tách file theo Bước trong references/ (Cấp độ 2)
└─ Có ≥ 3 loại đối tượng/chế độ khác nhau (Mỗi lần chạy chỉ dùng 1 loại):
   ├─ Phần quy tắc chung cho mọi loại ──► Đặt vào references/core/ (Cấp độ 3)
   └─ Phần quy tắc riêng của từng loại ──► Tách từng file vào references/types/ (Cấp độ 3)
```

### 2.3. Bảng Phân Luồng Nhanh Theo Đuôi File
| Đuôi file | Bản chất nội dung | Đặt ở thư mục | Hành động của AI |
| :--- | :--- | :--- | :--- |
| `.md` | Bộ điều hướng bước chạy, lệnh đọc dòng, cổng chất lượng | `SKILL.md` | ĐỌC đầu tiên khi kích hoạt |
| `.md` | Công thức chuyên môn, bảng quyết định, tiêu chí chấm điểm | `references/` (hoặc `core/`, `types/`) | ĐỌC theo khoảng dòng ở Bước X |
| `.md`, `.json`, `.html` | Khung dữ liệu đầu ra sạch (có ô điền `[Điền ...]`) | `templates/` | LÀM THEO khi sinh file kết quả |
| `.json`, `.yaml` | Tham số ngưỡng, cấu hình tách rời khỏi code/prompt | `config/` | ĐỌC / Truyền vào `scripts/` |
| `.py`, `.sh`, `.js` | Code quét dữ liệu (`scanner`), biên dịch (`engine`), kiểm toán (`validator`) | `scripts/` | CHẠY bằng lệnh terminal |
| `.png`, `.ttf`, `.pdf` | Tài nguyên tĩnh đính kèm vào sản phẩm đầu ra | `assets/` | DÙNG / Sao chép |

---

## Mục 3. Quy Tắc Tách/Gộp File Tham Chiếu, Chống Phân Mảnh & Chống Ảo Giác Dữ Liệu

### 3.1. Nguyên Tắc Tách File Tham Chiếu & Cờ Đỏ Chống Tách Vụn (`Anti-Fragmentation & Orphan Prevention`)
1. **Ở Cấp độ 2 (Quy trình tuần tự):** Tách file theo **BƯỚC QUY TRÌNH** (`01-buoc-mot.md`, `02-buoc-hai.md`), không tách vụn theo khái niệm nhỏ lẻ. Nhờ đó ở Bước 1, AI chỉ cần mở file `01`, không phải nhảy qua lại 5 file khác nhau.
2. **Ở Cấp độ 3 & 4 (Quy trình phân nhánh / Hybrid Engine):** Tách theo **BẤT BIẾN (`references/core/`)** và **BIẾN THIÊN (`references/types/`)**.
3. **Thang 3 Cấp Xử Lý Khi File Tham Chiếu Dài Lên (Tránh đẻ thêm việc & Tránh tạo File Mồ Côi):**
   - **Cấp 1 (Khi file $\le 80$ dòng):** Giữ nguyên trong **1 file duy nhất**, nén văn xuôi thành **Bảng quyết định `Nếu X → Thì Y`** và chia thành các Đầu mục (`## Mục 1`, `## Mục 2`).
   - **Cấp 2 (Khi 1 file phục vụ 2 tiểu bước hoặc dài `50 – 80 dòng`):** **KHÔNG tách thành 2 file vật lý**, mà dùng **Lệnh đọc phẫu thuật theo Khoảng Dòng (`StartLine–EndLine`)** trong `SKILL.md` (ví dụ: Bước 1A đọc `Mục 1: dòng 1–20`, Bước 1B đọc `Mục 2: dòng 21–45`). Cách này vừa tiết kiệm Token cho AI, vừa không đẻ thêm file mới cho con người.
   - **Cấp 3 (Chỉ tách thành 2 file vật lý KHI VÀ CHỈ KHI):** File vượt ngưỡng **`> 80 – 100 dòng` bảng đặc** VÀ hai phần bên trong thuộc **2 bước chạy độc lập hoặc 2 nhánh loại trừ nhau (`Đọc 1 Bỏ 9`)**. Ngay sau khi tách file, bắt buộc chạy `validate_skill_structure.py` để đảm bảo **0 File Mồ Côi (`Orphan File = 0`)**.
4. **3 Câu Hỏi Kiểm Tra Ranh Giới File:**
   - *AI cần kiến thức này ở Bước nào?* → Nếu cùng 1 Bước và tổng độ dài $\le 80$ dòng, bắt buộc gộp chung vào 1 file của Bước đó (chia theo `## Mục 1`, `## Mục 2`).
   - *Nội dung này có bị viết lặp lại ở 2 file không?* → Nếu có, xóa bản trùng, chỉ giữ ở 1 nơi duy nhất.
   - *Trong file `references/` có câu nào ra lệnh "Bước 1 làm X, Bước 2 làm Y" không?* → Nếu có, chuyển quy trình đó về `SKILL.md`, giữ `references/` thuần túy là bảng công thức.

### 3.2. Cơ Chế Kiểm Chứng Kép & Nhãn Nguồn (Khi Skill Xử Lý Dữ Liệu Thật)
Khi tạo các Skill phân tích dữ liệu, nghiên cứu thị trường, tài chính hoặc kiểm toán (yêu cầu độ trung thực 100%, không bịa đặt số liệu):
1. **Hệ thống Nhãn Nguồn Bắt Buộc:**
   - `[📊 Tên file/nguồn dữ liệu]`: Số liệu trích xuất trực tiếp từ dữ liệu đầu vào (xác minh được).
   - `[📌 Nguồn bên ngoài]`: Dẫn chứng từ tài liệu/website thực tế có thật.
   - `[⚠️ Giả thuyết cần xác minh]`: Nhận định do AI suy luận khi chưa đủ dữ liệu, cần người dùng kiểm tra.
   - `[✅ Người dùng chốt]`: Quyết định hoặc thông số do chính người dùng cung cấp/phê duyệt.
2. **Kiểm Toán Chéo Bằng Script (`Code Gate`):** Nếu đầu ra có bảng số liệu, độ dài ký tự hoặc cấu trúc bắt buộc, luôn ưu tiên dùng `scripts/validate_*.py` kiểm tra tự động trước khi trình người dùng duyệt.
