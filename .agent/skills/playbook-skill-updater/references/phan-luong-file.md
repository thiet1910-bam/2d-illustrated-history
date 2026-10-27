# Ma Trận Phân Luồng Khi SỬA & NÂNG CẤP Skill (Cấp 1 → Cấp 4)

## Mục 1. Cây Quyết Định: Sửa Gì → Đặt Ở Đâu?

```text
Loại thay đổi khi cập nhật Skill là gì?
├─ Thêm/sửa BƯỚC chạy, Cổng duyệt, hoặc Lệnh đọc dòng (`StartLine–EndLine`) ──► SKILL.md
├─ Thêm/sửa RÀO CHẮN & Danh sách Cấm mặc định (`Banned Defaults`) ───────────► SKILL.md (ngắn) hoặc references/ (chi tiết)
├─ Thêm/sửa CÔNG THỨC, Bảng quyết định (dùng chung cho mọi trường hợp) ──────► references/ (Cấp 2) hoặc references/core/ (Cấp 3)
├─ Thêm/sửa CÔNG THỨC RIÊNG cho 1 loại đối tượng/chế độ cụ thể ──────────────► references/types/ten-loai.md (Cấp 3)
├─ Thêm/sửa THAM SỐ NGƯỠNG tĩnh (.json/.yaml) để dễ cấu hình ngoài ──────────► config/ (Cấp 3, 4)
├─ Thêm/sửa ĐỊNH DẠNG KHUNG ĐẦU RA (chỉ chứa trường dữ liệu sạch) ────────────► templates/
├─ Thêm/sửa LOGIC QUÉT FILE, TÍNH TOÁN hoặc KIỂM TOÁN TỰ ĐỘNG ───────────────► scripts/ (validate_*.py hoặc scanners/engines/validators)
└─ Đổi THUẬT NGỮ / TÊN BIẾN / ĐƯỜNG DẪN ────────────────────────────────────► Tìm toàn bộ skill, đổi đồng loạt TẤT CẢ các file
```

---

## Mục 2. Bảng Phân Luồng Sửa Đổi & Ranh Giới Cấm Chồng Chéo

| Loại sửa đổi | Đặt ở file nào? | Quy tắc bắt buộc khi sửa (Chống làm hỏng kiến trúc) |
| :--- | :--- | :--- |
| **Thêm/sửa Bước quy trình** | `SKILL.md` (Phần Quy trình) | Phải gắn kèm **Lệnh đọc phẫu thuật 4 thành phần (`StartLine–EndLine`)** tới đúng mục trong `references/`. |
| **Thêm/sửa Công thức & Tiêu chí** | `references/*.md` (hoặc `core/`, `types/`) | Phải trình bày dạng **Bảng quyết định + Con số định lượng + Ví dụ `✅/❌`**. Sau khi sửa xong phải đếm lại dòng để cập nhật `StartLine–EndLine` trong `SKILL.md`. |
| **Khi 1 file `references/` thêm tư duy mới** | Giữ nguyên 1 file (chia `## Mục 1`, `## Mục 2`) nếu tổng $\le 80$ dòng | **Chống tách vụn (`Anti-Fragmentation`):** Nếu tổng file $\le 80$ dòng và cùng phục vụ 1 Bước, **CẤM tách file mới** (chỉ chia `## Mục` và trỏ `StartLine–EndLine`). Chỉ tách thành 2 file khi vượt `> 80–100 dòng` và thuộc 2 bước/nhánh độc lập, sau đó bắt buộc chạy `validate_skill_structure.py` để diệt **File mồ côi**. |
| **Sửa Khuôn mẫu đầu ra** | `templates/*.md` | **CẤM** thêm lời giải thích cách làm hay ghi chú nhắc việc vào `templates/`. Chỉ thêm/sửa các trường dữ liệu và ô `[Điền ...]`. |
| **Thêm/sửa Kiểm toán định lượng** | `scripts/*.py` | Code phải chạy độc lập không lỗi, kiểm tra bằng toán học thật và được gọi rõ cú pháp lệnh trong `SKILL.md`. |
| **Đổi tên thuật ngữ / đường dẫn** | Toàn bộ các file trong thư mục Skill | Dùng công cụ tìm kiếm quét toàn bộ thư mục skill, đổi hết và kiểm tra lại phải còn `0` kết quả cũ. |
