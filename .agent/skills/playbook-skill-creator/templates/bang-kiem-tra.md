# Bảng Kiểm Tra Toàn Diện Trước Khi Hoàn Thành Skill (Cả Vỏ Cấu Trúc Lẫn Ruột Bản Chất)

## Mục 1. Kiểm Tra Phần Mở Đầu YAML & Thân `SKILL.md` (Bộ Điều Hướng)
- [ ] `name`: Viết thường nối gạch ngang (`kebab-case`), $< 64$ ký tự, trùng khớp 100% với tên thư mục skill.
- [ ] `description`: Có đủ **LÀM GÌ (`WHAT`)** + **KHI NÀO DÙNG (`WHEN`)** + **1 từ khóa kích hoạt (`Kích hoạt: /...`)**. Không có trường YAML thừa.
- [ ] Tổng độ dài `SKILL.md` $\le 150$ dòng (chỉ đóng vai trò Bộ điều hướng, không nhồi lý thuyết dài dòng).
- [ ] Đã xác định đúng **Cấp độ phức tạp (`Cấp 1 → 4`)**, **Hình mẫu chức năng (`Hình mẫu 1 → 6`)** và **Chế độ vận hành (`Độc lập` hay `Dây chuyền`)**.
- [ ] Có **Bước 0: Kiểm tra Đầu vào / Trạng thái ổ cứng (`Entry Check`)** để định tuyến đúng luồng ngay từ đầu.
- [ ] Nếu là **Cấp độ 3 (`references/types/`)**: `SKILL.md` có quy tắc định tuyến chỉ đọc `core/` + đúng **1 file nhánh trong `types/`** (không đọc tràn lan cả thư mục).
- [ ] Nếu là **Cấp độ 4 (`Enterprise Hybrid Engine`)**: `SKILL.md` điều phối đúng giao thức bắt tay giữa `Scanner Script` $\rightarrow$ `LLM` $\rightarrow$ `Engine Script` $\rightarrow$ `Validator Script`.
- [ ] Có **Checklist Cổng chất lượng (`Quality Gate`)**, **Điểm dừng cứng (`Hard Gate`)** và **Danh sách Cấm mặc định (`Banned Defaults`)** kèm lý do Nhân – Quả.

## Mục 2. Kiểm Tra `references/` — Sách Hướng Dẫn Chuyên Môn ("Ruột Đặc", Tự Chủ)
- [ ] Mọi file trong `references/` đều được trỏ từ `SKILL.md` bằng **Lệnh đọc phẫu thuật 4 thành phần** (`Khi nào đọc` + `File/Mục/Dòng StartLine–EndLine` + `Giới hạn loại trừ` + `Tại sao đọc`). Không có file tham chiếu "mồ côi".
- [ ] **Đạt chuẩn "Ruột Đặc" (`High-Density Content`):**
  - [ ] Đã diệt trừ các tính từ cảm tính mơ hồ, thay bằng **Con số định lượng, Ngưỡng đo lường hoặc Công thức cụ thể**.
  - [ ] Đã nén lý thuyết thành **Bảng quyết định (`Nếu X → Thì Y`)** thay vì viết văn xuôi dài dòng.
  - [ ] Có ít nhất **1 cặp ví dụ đối chứng (`✅ Đúng` / `❌ Sai` kèm lý do)** cho các quy tắc trọng yếu.
- [ ] **Không chồng chéo nhiệm vụ:** Không chứa quy trình điều phối (`Bước 1, Bước 2`) và không trùng lặp nội dung giữa các file.
- [ ] **Tự chủ 100%:** `0%` đường dẫn `file:///` trỏ ra ngoài thư mục skill.

## Mục 3. Kiểm Tra `templates/`, `scripts/`, `config/` & Việt Hoá
- [ ] **`templates/` (nếu có — Khung dữ liệu đầu ra sạch 100%):**
  - [ ] Chỉ chứa cấu trúc trường dữ liệu đầu ra (`Pure Output Schema`) và các ô điền `[Điền ...]`.
  - [ ] `0%` lời hướng dẫn cách làm, lý thuyết giảng giải hay nhãn kỹ thuật đánh dấu cố định/thay đổi bị lọt vào trong `templates/`.
- [ ] **`scripts/` (nếu có — Kiểm toán & Tính toán thật):**
  - [ ] Code chạy độc lập không lỗi, hỗ trợ chuẩn `utf-8`, được gọi rõ cú pháp trong `SKILL.md`.
  - [ ] Thực sự kiểm tra định lượng hoặc xử lý dữ liệu bằng toán học (không phải script in chữ hình thức).
- [ ] **Tổng thể & Việt hoá:**
  - [ ] Không có file thừa (`README.md`, `CHANGELOG.md`, `INSTALLATION_GUIDE.md`).
  - [ ] Toàn bộ nội dung và tên file tiếng Việt chuẩn xác, thuật ngữ chuyên ngành nước ngoài đều được giải thích rõ ràng dễ hiểu.
- [ ] **Chạy Script Kiểm Toán Tự Động Đạt `100% [PASS]`:**
  - [ ] Đã chạy lệnh: `python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<đường_dẫn_thư_mục_skill>"` và nhận kết quả `PASS 100%`.
