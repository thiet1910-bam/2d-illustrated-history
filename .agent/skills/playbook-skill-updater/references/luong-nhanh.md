# Luồng Nhanh — Quy Trình Rút Gọn Cho Nhiệm Vụ NHẸ (4 Bước `LN-1 → LN-4`)

## Mục 1. Bảng Điều Hướng Đọc Tài Liệu Theo Bước (Luồng Nhanh)

| Bước trong Luồng Nhanh | Tài liệu cần đọc & Khoảng dòng | Mục đích đọc |
| :--- | :--- | :--- |
| **Bước LN-1:** Đọc skill & Phản biện nhanh | • `references/khung-phan-bien.md` (`StartLine: 1` → `EndLine: 162`)<br>• `references/mau-cap-nhat.md` (`StartLine: 1` → `EndLine: 81`) | Nắm quy tắc đọc skill gốc, quét nhanh 6 góc phản biện và chọn đúng mẫu cập nhật (`M1 → M8`). |
| **Bước LN-2 & LN-3:** Lập kế hoạch rút gọn | • `references/phan-luong-file.md` (`StartLine: 1` → `EndLine: 27`) | Xác định chính xác nội dung cần sửa phải đặt ở file nào (`SKILL.md`, `references/`, `templates/`, `scripts/`). |
| **Bước LN-4:** Thực thi & Kiểm toán tự động | • `references/quy-tac-viet.md` (`StartLine: 1` → `EndLine: 182`)<br>• `references/mau-sai.md` (`StartLine: 1` → `EndLine: 45`)<br>• `templates/bang-kiem-tra.md` (`StartLine: 1` → `EndLine: 24`) | Sửa có chọn lọc, giữ quy ước gốc, cập nhật tọa độ dòng `StartLine–EndLine` và chạy script kiểm toán cấu trúc. |

---

## Mục 2. Chi Tiết 4 Bước Thực Thi Luồng Nhanh

### Bước LN-1 & LN-2 — Đọc Skill Gốc & Phản Biện Rút Gọn
1. Đọc toàn bộ file của skill cần sửa (`SKILL.md`, `references/`, `templates/`, `scripts/`).
2. Ghi nhận **Cấu trúc hiện tại** và chẩn đoán **Nguyên nhân gốc rễ** (không chỉ sửa triệu chứng bề mặt).
3. Kiểm tra nhanh xem skill có bị lỗi **Chồng chéo 3 tầng**, **Thiếu số dòng `StartLine–EndLine`**, hay **Rỗng ruột** không.

### Bước LN-3 — Lập Kế Hoạch Rút Gọn & Dừng Duyệt
Trình bày bảng kế hoạch gọn:
`| # | File cần sửa | Thay đổi cụ thể (Dòng/Mục) | Rủi ro tác dụng phụ & Cách khóa |`

**⏸️ CỔNG DUYỆT LUỒNG NHANH (DỪNG CỨNG):**
Kết thúc bằng: *"Nếu bạn đồng ý → nói: **'Duyệt Luồng Nhanh, thực thi ngay'**. Nếu cần điều chỉnh → chỉ rõ điểm cần sửa."*

### Bước LN-4 — Thực Thi, Cập Nhật Số Dòng & Chạy Script Kiểm Toán (`Code Gate`)
1. Sửa chính xác những mục đã được duyệt. Nếu số dòng trong `references/` hoặc `templates/` thay đổi, cập nhật lại tọa độ `StartLine–EndLine` trong `SKILL.md`.
2. Kiểm tra chéo: tìm từ khóa cũ (phải bằng `0` kết quả).
3. **Chạy Script Kiểm Toán Tự Động bắt buộc:**
   `python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<đường_dẫn_thư_mục_skill>"`
   *(Nếu có bất kỳ lỗi `[FAIL]` nào, phải sửa ngay cho đến khi đạt `[PASS 100%]`)*.

**⏸️ CỔNG DUYỆT HOÀN TẤT:** Trình kết quả sửa đổi + kết quả chạy script `[PASS 100%]`. Kết thúc bằng: *"Nếu đồng ý → nói: **'Duyệt hoàn tất'**."*
