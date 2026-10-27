# Quy Trình Đầy Đủ — Cho Nhiệm Vụ NẶNG & Nâng Cấp Cấp Độ (`Pha U1 → U2 → U3`)

## Mục 1. Pha U1 — Đọc Giải Phẫu & Phản Biện Đa Góc Độ (Tư Duy Guru)

- **📖 Lệnh đọc tài liệu Pha U1:**
  - **Khi nào đọc:** Ngay khi nhiệm vụ được phân loại là **NẶNG** sau Pha U0.
  - **Đọc ở đâu:**
    1. `references/khung-phan-bien.md` — **Từ `§1` đến `§5` (`StartLine: 1` → `EndLine: 162`)**.
    2. `references/mau-cap-nhat.md` — **Từ `Mục 1` đến `Mục 4` (`StartLine: 1` → `EndLine: 81`)**.
  - **Tại sao đọc:** Áp dụng Khung phản biện 6 góc và chọn đúng mẫu nâng cấp (`M1 → M8`, bao gồm nâng cấp Cấp độ 1→2→3→4, chuyển giao việc tính toán sang Code, và làm đặc ruột `references/`).
- **Các bước thực hiện Pha U1:**
  1. **Đọc & Ghi nhận cấu trúc gốc:** Đọc toàn bộ `SKILL.md`, `references/`, `templates/`, `scripts/`, `config/` của skill cần sửa.
  2. **Soi chiếu 6 góc + Kiểm toán Vỏ & Ruột:**
     - *Về Vỏ cấu trúc:* Cấp độ hiện tại (1/2/3/4) đã khớp với độ phức tạp bài toán chưa? Đã tách bạch 3 tầng (`SKILL.md` / `references/` / `templates/`) và gắn số dòng `StartLine–EndLine` chưa?
     - *Về Ruột bản chất:* Trong `references/` đã là Bảng quyết định + Con số định lượng + Ví dụ `✅/❌` chưa, hay vẫn là văn xuôi sáo rỗng? Có việc tính toán/đếm nào cần chuyển sang `scripts/` không?
  3. **Phản biện gợi ý của người dùng (Tư duy Munger · Dalio · Musk):** Phân biệt rõ triệu chứng vs. nguyên nhân gốc; nói thẳng các lỗ hổng 🔴 Nghiêm trọng / 🟡 Quan trọng / 🟢 Nhỏ.

**⏸️ CỔNG DUYỆT U1 (DỪNG CỨNG):** Trình bày Bảng cấu trúc hiện tại + Bảng phản biện 6 góc & Đề xuất mẫu nâng cấp (`M1–M8`).
Kết thúc bằng: *"Nếu bạn đồng ý → nói: **'Duyệt Pha U1, chuyển Pha U2'**. Nếu cần điều chỉnh → chỉ rõ điểm cần sửa."*

---

## Mục 2. Pha U2 — Lập Kế Hoạch Chi Tiết & Chia Nhiệm Vụ Con (`Sub-tasks`)

- **📖 Lệnh đọc tài liệu Pha U2:**
  - **Khi nào đọc:** Ngay khi người dùng duyệt Pha U1.
  - **Đọc ở đâu:**
    1. `references/phan-luong-file.md` — **Từ `Mục 1` đến `Mục 2` (`StartLine: 1` → `EndLine: 27`)**.
    2. `templates/roadmap-nhiem-vu-nang.md` — **Từ `§1` đến `§5` (`StartLine: 1` → `EndLine: 112`)**.
  - **Tại sao đọc:** Phân bổ đúng vị trí file cần sửa/tạo mới và chia thành các nhiệm vụ con độc lập (`2A, 2B, 2C...`) có thứ tự phụ thuộc hợp lý.
- **Các bước thực hiện Pha U2:**
  1. Lập bảng kế hoạch tổng thể: `| # | File | Thay đổi cụ thể | Lý do (Bản chất) | Rủi ro tác dụng phụ |`.
  2. Chia thành các **Nhiệm vụ con (`2A, 2B, 2C...`)**: Ví dụ `2A` (Chưng cất/nâng cấp ruột `references/`), `2B` (Làm sạch `templates/` & viết `scripts/`), `2C` (Đo dòng & cập nhật bộ điều hướng `SKILL.md` + chạy kiểm toán).

**⏸️ CỔNG DUYỆT U2 (DỪNG CỨNG):** Trình bày Kế hoạch tổng thể + Bảng lộ trình nhiệm vụ con.
Kết thúc bằng: *"Nếu bạn đồng ý → nói: **'Duyệt Pha U2, chuyển Pha U3'**. Nếu cần điều chỉnh → chỉ rõ điểm cần sửa."*

---

## Mục 3. Pha U3 — Thực Thi Từng Nhiệm Vụ Con & Kiểm Toán Tự Động Bằng Script

- **📖 Lệnh đọc tài liệu Pha U3:**
  - **Khi nào đọc:** Ngay khi bắt đầu thực thi Pha U3.
  - **Đọc ở đâu:**
    1. `references/quy-tac-viet.md` — **Từ `§1` đến `§11` (`StartLine: 1` → `EndLine: 182`)**.
    2. `references/mau-sai.md` — **Toàn bộ file (`StartLine: 1` → `EndLine: 45`)**.
    3. `templates/bang-kiem-tra.md` — **Toàn bộ file (`StartLine: 1` → `EndLine: 24`)**.
  - **Tại sao đọc:** Tuân thủ nghiêm ngặt quy tắc sửa chọn lọc, chống tác dụng phụ và rà soát toàn bộ tiêu chuẩn trước khi bàn giao.
- **Các bước thực hiện Pha U3:**
  1. **Thực thi từng nhiệm vụ con (`2A → 2B → 2C`):** Làm xong nhiệm vụ con nào → tự kiểm tra → trình báo cáo nhiệm vụ con đó và **DỪNG LẠI** chờ người dùng duyệt trước khi sang nhiệm vụ con tiếp theo.
  2. **Kiểm tra chéo & Đo lại tọa độ dòng:** Sau khi hoàn tất các nhiệm vụ con, quét từ khóa cũ (`= 0` kết quả) và kiểm tra chính xác mọi tọa độ `StartLine–EndLine` trong `SKILL.md`.
  3. **Chạy Script Kiểm Toán Cấu Trúc & Bản Chất Tự Động (`Code Gate` bắt buộc):**
     `python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<đường_dẫn_thư_mục_skill>"`
     *(Nếu phát hiện bất kỳ lỗi `[FAIL]` nào → sửa ngay lập tức cho đến khi đạt `[PASS 100%]`)*.

**⏸️ CỔNG DUYỆT U3 (DỪNG CỨNG CUỐI CÙNG):** Trình bày Tổng kết lộ trình + Kết quả kiểm tra chéo + Báo cáo `[PASS 100%]` của Script kiểm toán.
Kết thúc bằng: *"Nếu bạn đồng ý → nói: **'Duyệt Pha U3, hoàn tất nâng cấp'**."*
