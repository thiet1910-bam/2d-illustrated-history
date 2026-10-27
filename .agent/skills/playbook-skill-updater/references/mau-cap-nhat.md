# 8 Mẫu Thực Chiến Khi CẬP NHẬT & NÂNG CẤP CẤP ĐỘ Skill (`M1 → M8`)

## Mục 1. Cây Quyết Định Chọn Mẫu Cập Nhật (`M1 → M8`)

```text
Bản chất vấn đề cần nâng cấp là gì?
├─ Nhóm A: Tối ưu Nội dung & Quy trình trong cùng Cấp độ
│  ├─ File tham chiếu quá dài (> 200 dòng, ôm nhiều bước) ────────► M1. Tách File Theo Bước Quy Trình
│  ├─ Nhiều file chứa nội dung trùng lặp nhau (> 30%) ───────────► M2. Gộp & Khử Trùng Lặp File
│  ├─ Thiếu công thức/bảng quy tắc chuyên môn cho 1 bước ─────────► M3. Thêm Tham Chiếu Mới ("Ruột Đặc")
│  ├─ Quy trình thiếu bước, thiếu Cổng duyệt hoặc thiếu Số dòng ──► M4. Chuẩn Hóa Quy Trình & Lệnh Đọc Phẫu Thuật
│  └─ File đầu ra bị lẫn lời hướng dẫn hoặc thiếu trường dữ liệu ─► M5. Làm Sạch Khuôn Mẫu Đầu Ra (`Pure Output Schema`)
│
└─ Nhóm B: Nâng Cấp Kiến Trúc & Chữa Bệnh "Rỗng Ruột / Đếm Sai" (Cấp Độ Cao)
   ├─ Bài toán phình to (đa nhánh đối tượng hoặc xử lý file lớn) ─► M6. Nâng Cấp Cấp Độ Phức Tạp (`Cấp 1 → 2 → 3 → 4`)
   ├─ AI hay đếm sai ký tự/thời lượng hoặc kiểm tra bằng mắt sót ─► M7. Chuyển Giao Việc Toán Học Sang Code (`Code-over-Prompt`)
   └─ `references/` viết văn xuôi sáo rỗng, nhiều tính từ mơ hồ ──► M8. Phẫu Thuật Làm Đặc Ruột (`High-Density Refactoring`)
```

---

## Mục 2. Nhóm A — 5 Mẫu Tối Ưu Nội Dung & Tách Bạch 3 Tầng (`M1 → M5`)

### M1. Tách File Dài → Nhiều File Ngắn Theo Bước Quy Trình (Kèm Rào Chắn Chống Tách Vụn)
- **Khi nào dùng:** File trong `references/` vượt ngưỡng **`> 80 – 100 dòng` bảng đặc** (hoặc $> 150$ dòng văn bản) VÀ chứa kiến thức của **2–3 bước chạy khác nhau** (hoặc 2 nhánh đối tượng độc lập) khiến AI đọc bị tràn bộ nhớ.
- **⛔ Khi nào CẤM dùng (Chống phân mảnh & Đẻ thêm việc):** Nếu file hiện tại còn ngắn ($\le 80$ dòng) và các mục bên trong vẫn phục vụ chung 1 Bước (ví dụ: Bước 1 vừa cắt âm thanh vừa chia cụm), **TUYỆT ĐỐI KHÔNG tách thành 2 file vật lý**. Thay vào đó, hãy chia thành `## Mục 1`, `## Mục 2` ngay trong file đó và dùng lệnh đọc `StartLine–EndLine` trong `SKILL.md`.
- **Cách thực thi khi đủ điều kiện tách:** Tách theo **Bước quy trình** (`01-buoc-mot.md`, `02-buoc-hai.md`), đánh số lại `## Mục 1`, `## Mục 2`, cập nhật tọa độ dòng `StartLine–EndLine` trong `SKILL.md`, và chạy ngay `validate_skill_structure.py` để đảm bảo **0 File Mồ Côi (`Orphan File = 0`)**.

### M2. Gộp & Khử Trùng Lặp File
- **Khi nào dùng:** Có $\ge 2$ file chứa quy tắc trùng nhau, gây nguy cơ sửa 1 nơi quên 1 nơi.
- **Cách thực thi:** Gom về 1 nguồn chân lý duy nhất (*Single Source of Truth*), xóa bản thừa và cập nhật lại đường dẫn trỏ trong `SKILL.md`.

### M3. Thêm Tham Chiếu Mới (Đạt Chuẩn "Ruột Đặc")
- **Khi nào dùng:** Skill thiếu kiến thức chuyên sâu cho một bước cụ thể.
- **Cách thực thi:** Tạo file mới trong `references/`, trình bày bằng **Bảng quyết định + Con số định lượng + Cặp ví dụ `✅ Đúng / ❌ Sai`**, sau đó gắn lệnh đọc 4 thành phần (`StartLine–EndLine`) vào đúng bước đó trong `SKILL.md`.

### M4. Chuẩn Hóa Quy Trình & Gắn Lệnh Đọc Phẫu Thuật (`StartLine–EndLine`)
- **Khi nào dùng:** `SKILL.md` đang viết lệnh đọc chung chung (`→ Đọc references/file.md`), thiếu Bước 0 kiểm tra đầu vào, hoặc thiếu Điểm dừng cứng (`Hard Gate`).
- **Cách thực thi:** Đếm số dòng thực tế của từng `## Mục` trong `references/`, cập nhật lệnh đọc 4 thành phần vào từng bước của `SKILL.md`, bổ sung Checklist cổng chất lượng trước Điểm dừng cứng.

### M5. Làm Sạch Khuôn Mẫu Đầu Ra (`Pure Output Schema Purification`)
- **Khi nào dùng:** File trong `templates/` bị nhét lẫn lời dạy bảo (*"Hãy viết..."*, *"Lưu ý..."*, `← CỐ ĐỊNH`) làm bẩn file kết quả bàn giao.
- **Cách thực thi:** Cắt toàn bộ lời hướng dẫn trong `templates/` chuyển sang `references/`; giữ `templates/` chỉ còn 100% khung trường dữ liệu sạch và ô điền `[Điền ...]`.

---

## Mục 3. Nhóm B — 3 Mẫu Nâng Cấp Kiến Trúc Bậc Cao (`M6 → M8`)

### M6. Nâng Cấp Cấp Độ Phức Tạp Của Skill (`Architectural Tier Upgrade: Cấp 1 → 2 → 3 → 4`)
| Lộ trình nâng cấp | Dấu hiệu cần nâng cấp | Cách thực thi bản chất (Không làm hình thức) |
| :--- | :--- | :--- |
| **Từ Cấp 1 $\rightarrow$ Cấp 2** | `SKILL.md` vượt quá 120–150 dòng hoặc cần khuôn mẫu đầu ra cố định. | Giữ `SKILL.md` làm Bộ điều hướng; tách phần kiến thức chuyên môn sang `references/`, tách khung đầu ra sang `templates/`. |
| **Từ Cấp 2 $\rightarrow$ Cấp 3 (Đa nhánh)** | Skill phải xử lý $\ge 3$ loại đối tượng/ngành hàng/chế độ khác nhau (mỗi loại có quy tắc riêng $> 50$ dòng). | Chia `references/` thành **`references/core/`** (chứa 60% quy tắc bất biến chung) và **`references/types/`** (mỗi loại 1 file). Trong `SKILL.md` Bước 1, thiết lập **Định tuyến "Đọc 1 Bỏ 9"** (chỉ đọc `core/` + đúng 1 file `types/` khớp loại). |
| **Từ Cấp 2/3 $\rightarrow$ Cấp 4 (Lai Code Engine)** | Phải xử lý hàng chục/trăm file dữ liệu, tính toán phức tạp, gọi CLI/API hoặc xuất file kỹ thuật. | Tạo `config/` (chứa tham số `.json`) + `scripts/` chia 3 tầng: `scanners/` (quét đầu vào xuất `manifest.json`) $\rightarrow$ `LLM` (lập kế hoạch) $\rightarrow$ `engines/` (biên dịch) $\rightarrow$ `validators/` (kiểm toán tự động / Vision QA). |

### M7. Chuyển Giao Việc Tính Toán Từ AI Sang Code (`Code-over-Prompt Migration`)
- **Khi nào dùng:** Phát hiện AI liên tục đếm sai ký tự, tính nhầm thời lượng/số liệu, hoặc bỏ sót tiêu chí kiểm tra khi tự duyệt bằng mắt.
- **Cách thực thi:** Viết script Python trong `scripts/validate_*.py` (hoặc `scripts/engines/`) để máy tính thực hiện 100% phép đếm/kiểm tra định lượng, và đặt lệnh chạy bắt buộc (`Code Gate`) ngay trước Cổng duyệt của `SKILL.md`.

### M8. Phẫu Thuật Chữa Bệnh "Rỗng Ruột" (`High-Density Content Refactoring`)
- **Khi nào dùng:** Các file trong `references/` viết toàn lời khuyên văn xuôi sáo rỗng, nhiều tính từ cảm tính (*"hấp dẫn, chuyên nghiệp, mượt mà, tối ưu"*).
- **Cách thực thi:**
  1. Quét toàn bộ tính từ cảm tính → thay bằng **Khoảng số học, Công thức hoặc Ngưỡng đo lường cụ thể** (`Zero-Adjective Rule`).
  2. Chuyển các đoạn văn giải thích dài thành **Bảng quyết định `| Điều kiện (Nếu X) | Hành động bắt buộc (Thì Y) | Ngưỡng chuẩn | Lỗi cấm |`**.
  3. Bổ sung **Danh sách Cấm mặc định (`Banned Defaults`)** và ít nhất **1 cặp ví dụ `✅ Đúng / ❌ Sai`** cho mỗi quy tắc chính.


---

## Mục 4. Ví Dụ Giải Phẫu Thực Tế: Phẫu Thuật Skill Từ "Vỏ Hình Thức / Rỗng Ruột" Thành "Đúng Bản Chất"

### 4.1. Tình Huống Thực Tế
- **Vấn đề người dùng báo:** *"Tôi có 1 skill viết kịch bản/tài liệu bán hàng cho 4 dòng sản phẩm khác nhau, nhưng mỗi lần chạy AI viết rất chung chung, hay nhầm quy tắc của sản phẩm A sang sản phẩm B, đếm sai độ dài chữ và file kết quả xuất ra cứ bị dính mấy câu ghi chú hướng dẫn."*

### 4.2. Đối Chứng Cách Sửa: `❌ Chữa Triệu Chứng / Hình Thức` vs. `✅ Phẫu Thuật Đúng Bản Chất`

| Hạng mục lỗi | ❌ Cách sửa SAI (Chỉ chữa triệu chứng bề mặt) | ✅ Cách sửa ĐÚNG BẢN CHẤT (Tổ hợp Mẫu `M4 + M5 + M6 + M7 + M8`) |
| :--- | :--- | :--- |
| **1. AI viết chung chung, sáo rỗng** | Thêm câu *"BẮT BUỘC PHẢI VIẾT SÂU SẮC, CHUYÊN NGHIỆP HƠN!!!"* vào `SKILL.md`. | **Áp dụng Mẫu M8 (Làm đặc ruột):** Mở `references/`, xóa các tính từ cảm tính; thay bằng **Bảng quyết định `Nếu khách hàng thuộc nhóm X → Dùng cấu trúc câu Y (từ 45–60 từ)`** kèm cặp ví dụ `✅ Đúng / ❌ Sai`. |
| **2. Nhầm quy tắc giữa 4 dòng sản phẩm** | Vẫn giữ chung 1 file tham chiếu dài 400 dòng nhưng thêm dòng nhắc *"Chú ý đừng nhầm lẫn giữa các sản phẩm"*. | **Áp dụng Mẫu M6 (Nâng lên Cấp độ 3 Đa nhánh):** Tách phần quy tắc chung vào `references/core/luat-chung.md` và tách 4 sản phẩm thành 4 file riêng trong `references/types/`. Tại Bước 1 của `SKILL.md`, đặt lệnh **Định tuyến "Đọc 1 Bỏ 3"** kèm tọa độ dòng `StartLine–EndLine` (`M4`). |
| **3. File đầu ra bị dính câu hướng dẫn** | Dặn AI trong prompt: *"Khi xuất kết quả nhớ xóa các câu hướng dẫn đi nhé"*. | **Áp dụng Mẫu M5 (Làm sạch Khuôn mẫu):** Cắt toàn bộ lời hướng dẫn trong `templates/` chuyển sang `references/`; giữ `templates/` là khung dữ liệu sạch 100%. |
| **4. AI đếm sai độ dài ký tự/từ** | Nhắc AI *"Hãy đếm kỹ số ký tự trước khi trả lời"*. | **Áp dụng Mẫu M7 (`Code-over-Prompt`):** Viết script `scripts/validate_output.py` tự động đếm ký tự và kiểm tra từ cấm bằng toán học trước Cổng duyệt. |
