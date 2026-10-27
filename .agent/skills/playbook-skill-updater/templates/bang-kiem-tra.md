# Bảng Kiểm Tra Toàn Diện Sau Khi Cập Nhật / Nâng Cấp Skill

## Mục 1. Kiểm Tra Quy Trình Phân Loại & Phạm Vi Sửa Đổi
- [ ] Đã phân loại NẶNG / NHẸ dựa trên Cây quyết định trong `references/phan-loai-nhiem-vu.md` và được người dùng duyệt ở Pha U0?
- [ ] Nếu là nhiệm vụ NẶNG: Đã chia nhiệm vụ con (`2A, 2B...`) và dừng duyệt từng nhiệm vụ con đúng chuẩn?
- [ ] Chỉ sửa đúng các file trong kế hoạch đã duyệt; không tự ý đẻ thêm file phụ trợ bị cấm (`README.md`, `CHANGELOG.md`, `NOTES.md`)?
- [ ] Nếu đổi tên thuật ngữ / nhân vật / đường dẫn: Đã tìm kiếm toàn bộ thư mục skill và xác nhận từ khóa cũ còn `0` kết quả?

## Mục 2. Kiểm Tra Kiến Trúc 3 Tầng, Lệnh Đọc Phẫu Thuật & Mật Độ "Ruột Đặc"
- [ ] **Bộ điều hướng `SKILL.md` ($\le 150$ dòng):**
  - [ ] Mọi lệnh trỏ sang `references/` đã có đủ **4 thành phần (`Khi nào đọc` + `File/Mục/Dòng StartLine–EndLine` + `Giới hạn loại trừ` + `Tại sao đọc`)** và khớp với số dòng thực tế sau khi sửa?
  - [ ] Nếu nâng cấp lên **Cấp độ 3 (`references/types/`)**: Đã có quy tắc định tuyến chỉ đọc `core/` + đúng 1 file `types/`?
  - [ ] Nếu nâng cấp lên **Cấp độ 4 (`Enterprise Hybrid Engine`)**: Đã có giao thức bắt tay rõ ràng giữa `scanners/`, `LLM`, `engines/`, `validators/`?
- [ ] **Sách hướng dẫn `references/` (Tự chủ & Ruột Đặc):**
  - [ ] Nội dung mới/sửa đã đạt chuẩn **Ruột Đặc** (Con số định lượng + Bảng quyết định `Nếu X → Thì Y` + Cặp đối chứng `✅ Đúng / ❌ Sai`), không viết văn xuôi cảm tính?
  - [ ] Tự chủ 100% (`0%` đường dẫn `file:///` trỏ ra ngoài thư mục skill) và không chứa các bước điều phối quy trình?
- [ ] **Khuôn mẫu `templates/` (Sạch 100%):**
  - [ ] Chỉ chứa khung dữ liệu đầu ra thuần túy (`Pure Output Schema`), không bị lọt lời hướng dẫn cách làm hay nhãn kỹ thuật đánh dấu cố định/thay đổi?

## Mục 3. Kiểm Tra Việt Hoá, Nhãn Nguồn & Chạy Script Kiểm Toán Tự Động (`Code Gate`)
- [ ] Toàn bộ nội dung sửa/thêm viết bằng tiếng Việt rõ ràng, thuật ngữ chuyên ngành nước ngoài đều được giải thích ngay lần đầu?
- [ ] Các số liệu/dữ liệu thực tế mới thêm vào đều có nhãn nguồn (`[📊]`, `[📌]`, `[⚠️]`, `[✅]`), không bịa đặt?
- [ ] **Chạy Script Kiểm Toán Tự Động Đạt `100% [PASS]`:**
  - [ ] Đã chạy lệnh: `python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<đường_dẫn_thư_mục_skill>"` và nhận kết quả `PASS 100%`.
