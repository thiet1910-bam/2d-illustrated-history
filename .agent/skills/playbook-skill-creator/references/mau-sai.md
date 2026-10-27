# Bảng CẤM, Chống Trùng Lặp & Chống "Bệnh Hình Thức / Rỗng Ruột"

## Mục 1. 10 Điều CẤM Đưa Vào Bất Kỳ Skill Nào

| # | ❌ CẤM TUYỆT ĐỐI | Lý do (Nhân – Quả) | Cách xử lý đúng |
| :-: | :--- | :--- | :--- |
| 1 | Các file phụ trợ cho người đọc (`README.md`, `CHANGELOG.md`, `INSTALL.md`) | Skill là bộ nhớ chỉ dẫn cho AI thực thi, không phải kho tài liệu giới thiệu phần mềm. | Xóa bỏ hoàn toàn. Mọi chỉ dẫn điều hướng đặt tại `SKILL.md`. |
| 2 | Kiến thức phổ thông AI đã biết sẵn | Làm lãng phí bộ nhớ ngữ cảnh (*Token*) và làm loãng sự chú ý của AI. | Xóa bỏ. Chỉ giữ công thức đặc thù, ngưỡng định lượng riêng của bài toán. |
| 3 | Lệnh đọc chung chung không có khoảng dòng (`→ Đọc references/file.md`) | Khiến AI nạp toàn bộ các file cùng lúc gây tràn bộ nhớ hoặc đọc sót mục quan trọng. | Ghi đủ 4 thành phần: `Khi nào đọc` + `File/Mục/Dòng (StartLine–EndLine)` + `Giới hạn loại trừ` + `Tại sao đọc`. |
| 4 | Nhét lời hướng dẫn cách làm vào trong `templates/` | Khi AI điền dữ liệu vào `templates/`, các câu hướng dẫn sẽ bị chép lẫn vào file đầu ra bàn giao. | Giữ `templates/` là **Khung dữ liệu đầu ra sạch 100% (`Pure Output Schema`)**. Mọi lời dạy cách làm chuyển sang `references/`. |
| 5 | Đặt quy trình bước chạy (`Bước 1, Bước 2`) vào trong `references/` | Làm chồng chéo quyền chỉ huy giữa `SKILL.md` và `references/`, gây mâu thuẫn thứ tự thực thi. | Quy trình bước chạy chỉ nằm ở `SKILL.md`. `references/` chỉ chứa công thức và bảng tra cứu. |
| 6 | Đặt đường dẫn `file:///` trỏ ra ngoài thư mục skill ở trong `references/` | Khi di chuyển skill hoặc khi đường dẫn ngoài thay đổi, skill bị đứt gãy hoàn toàn. | Chưng cất toàn bộ kiến thức cần thiết vào thẳng các file trong `references/` để skill tự chủ 100%. |
| 7 | Tính từ cảm tính mơ hồ trong `references/` (*"ngắn gọn, hấp dẫn, chuyên nghiệp, mượt mà"*) | Mỗi lần chạy AI sẽ tự suy diễn một kiểu, tạo ra sản phẩm công nghiệp rập khuôn, không kiểm soát được chất lượng. | Quy đổi thành **Con số định lượng**, **Bảng quyết định `Nếu X → Thì Y`** và **Cặp ví dụ `✅ Đúng / ❌ Sai`**. |
| 8 | Tạo thư mục `references/types/` (Cấp độ 3) nhưng bắt AI đọc toàn bộ các file trong `types/` | Phá hỏng hoàn toàn cơ chế tiết kiệm Token của kiến trúc Đa nhánh (`Single-Branch Loading`). | Ở Bước 1 của `SKILL.md`, định tuyến rõ thuộc loại nào thì **chỉ đọc `core/` + đúng 1 file `types/` của loại đó**. |
| 9 | Đặt mã giả (pseudo-code) hoặc script "làm cảnh" vào `scripts/` | AI gọi chạy sẽ báo lỗi hệ thống hoặc trả về kết quả `PASS` giả tạo dù dữ liệu sai. | Mọi file trong `scripts/` phải là code chạy thật, kiểm tra/tính toán bằng toán học thực tế. |
| 10 | Trường YAML thừa trong phần mở đầu `SKILL.md` | Gây lỗi bộ đọc tự động của hệ thống Agent. | Chỉ dùng đúng 2 trường `name` và `description`. |

---

## Mục 2. 5 Quy Tắc Chống Trùng Lặp & Chống "Vỏ Phức Tạp, Ruột Rỗng"

| # | Quy tắc cốt lõi | ✅ Đúng Bản Chất | ❌ Sai (Bệnh Hình Thức / Rỗng Ruột) |
| :-: | :--- | :--- | :--- |
| 1 | **1 nội dung = 1 nơi duy nhất** | Công thức chấm điểm chỉ nằm ở `references/02-tieu-chi.md`; `SKILL.md` chỉ trỏ dòng đọc tới đó. | Chép bảng điểm vào cả `SKILL.md`, `references/` lẫn `templates/` → khi sửa 1 nơi, 2 nơi kia lệch nhau. |
| 2 | **Chọn Cấp độ khớp đúng độ phức tạp thực tế** | Bài toán 60 dòng quy tắc → làm **Cấp độ 1** (1 file `SKILL.md`). Bài toán xử lý 100 file dữ liệu → làm **Cấp độ 4** (`scanners/engines/validators`). | Bài toán nhỏ xíu cũng đẻ ra 5 thư mục rỗng; hoặc bài toán tính toán lớn lại bắt AI tự nhẩm bằng lời văn. |
| 3 | **Ruột `references/` phải là Bảng & Số** | Mở file `references/` ra thấy ngay Bảng thông số, Cây quyết định, Danh sách Cấm và Ví dụ `✅/❌`. | Mở file `references/` ra toàn văn xuôi lý thuyết sáo rỗng như bài văn mẫu. |
| 4 | **Khớp nối chặt chẽ nếu là Skill Dây chuyền (`Pipeline`)** | Tên trường dữ liệu ở `templates/` đầu ra của Skill trước trùng khớp 100% với đầu vào mà Skill sau cần đọc. | Mỗi Skill xuất một kiểu định dạng tự do khiến Skill bước sau không đọc tự động được. |
| 5 | **Kiểm toán bằng Script trước khi báo cáo** | Luôn chạy `validate_skill_structure.py` (khi tạo/sửa skill) và `validate_*.py` (khi chạy skill) để xác nhận 0 lỗi. | Tự đánh dấu tích `[x]` bằng mắt mà không chạy lệnh kiểm tra thực tế. |
