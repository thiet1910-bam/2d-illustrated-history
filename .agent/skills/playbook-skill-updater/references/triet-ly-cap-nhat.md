# 9 Triết Lý Cốt Lõi Khi CẬP NHẬT & NÂNG CẤP Skill Đa Ngành

## Mục 1. Nguyên Tắc Bảo Toàn & Chẩn Đoán Gốc Rễ (Triết lý 1 – 5)

### 1. Giữ Cấu Trúc Đang Đúng, Chỉ Đổi Cấu Trúc Khi Cấp Độ Thay Đổi
- **Cấu trúc (Vỏ)** = Cây thư mục, tên file, quy ước đánh số mục. **Nội dung (Ruột)** = Công thức, bảng quy tắc, ví dụ bên trong.
- **Quy tắc:** Mặc định giữ nguyên cấu trúc gốc nếu nó vẫn đáp ứng tốt bài toán. Chỉ tái cấu trúc thư mục khi **Cấu trúc cũ chính là nguyên nhân gây lỗi** hoặc khi cần **Nâng cấp Cấp độ Skill (`Cấp 1 → 2 → 3 → 4`)** và đã được người dùng phê duyệt ở kế hoạch.
- **✅ Đúng:** Thêm 2 tiêu chí mới vào bảng hiện có trong `references/01-tieu-chi.md`.
- **❌ Sai:** Tự ý xóa bảng cũ, đổi tên hàng loạt file khi người dùng chỉ yêu cầu sửa 1 thông số.

### 2. Tìm Nguyên Nhân Gốc Trước, Sửa Triệu Chứng Sau (`Root Cause Analysis`)
- Khi người dùng báo *"Đầu ra của skill bị sai chỗ X"*, hãy hỏi ngay: *Chỗ X bị sai là do thiếu quy tắc trong `references/`, do `SKILL.md` quên ra lệnh đọc dòng đó, do `templates/` bị lẫn rác, hay do bắt AI tự nhẩm tính toán học mà không có `scripts/`?*
- **✅ Đúng:** Phát hiện AI viết tiêu đề dài quá quy định là do bắt LLM tự đếm ký tự bằng mắt → Giải pháp gốc rễ: Bổ sung kiểm tra độ dài vào `scripts/validate_*.py`.
- **❌ Sai:** Chỉ thêm chữ *"CHÚ Ý ĐẾM KỸ KÝ TỰ!!!"* vào `SKILL.md` (sửa triệu chứng, lần sau AI vẫn đếm sai).

### 3. AI Là Nhà Phê Bình Khó Tính, Không Phải Kẻ Gật Đầu (`Radical Transparency`)
- Phải phản biện thẳng thắn gợi ý của người dùng dựa trên hiệu quả thực tế. Nếu gợi ý của người dùng làm phình bộ nhớ ngữ cảnh (*Token*), gây trùng lặp giữa các file hoặc rơi vào "Bệnh hình thức" → nói thẳng lý do và đề xuất phương án tối ưu hơn.
- **✅ Đúng:** *"Bạn đề xuất tạo thêm 4 file mới, nhưng 3 trong số đó trùng 70% với `core/`. Tôi đề xuất gom phần chung vào `references/core/` và chỉ tách phần khác biệt vào `references/types/`."*
- **❌ Sai:** Người dùng bảo gì gật đầu làm nấy khiến skill phình to và mâu thuẫn chéo.

### 4. Sửa Phẫu Thuật Có Chọn Lọc — Không Viết Lại Mù Quáng
- Chỉ sửa đúng đoạn/bảng cần nâng cấp, giữ nguyên các công thức và dữ liệu chuẩn đang hoạt động tốt để tránh làm rơi rụng kiến thức gốc.

### 5. Ngôn Ngữ Thuần Việt, Giải Thích Rõ Thuật Ngữ Chuyên Môn
- Toàn bộ nội dung viết bằng tiếng Việt rõ ràng, khoa học; mọi thuật ngữ chuyên ngành nước ngoài đều phải giải thích ngắn gọn, dễ hiểu ngay lần đầu xuất hiện.

---

## Mục 2. Tư Duy Guru & Chuẩn Kiến Trúc Thế Hệ Mới (Triết lý 6 – 9)

### 6. Lăng Kính 3 Guru Khi Phản Biện Skill (`Munger · Dalio · Musk`)
| Guru | Tư duy cốt lõi | Câu hỏi bắt buộc khi kiểm tra & nâng cấp Skill |
| :--- | :--- | :--- |
| **Charlie Munger** | Tư duy ngược (*Inversion*) | *"Nếu sửa theo cách này thì tác dụng phụ gì sẽ làm hỏng các bước khác? Cần khóa những điều cấm nào (`Banned Defaults`)?"* |
| **Ray Dalio** | Minh bạch triệt để | *"Skill này đang có lỗ hổng nghiêm trọng (🔴) nào ở cả Vỏ lẫn Ruột? Phải chỉ thẳng ra trước khi khen."* |
| **Elon Musk** | Tư duy nguyên bản (*First Principles*) | *"Bản chất bài toán này cần Cấp độ mấy (1, 2, 3 hay 4) và tỷ lệ `LLM : Code` bao nhiêu là tối ưu nhất?"* |

### 7. Phân Tách Tuyệt Đối 3 Loại File & Lệnh Đọc Phẫu Thuật (`StartLine–EndLine`)
Khi nâng cấp bất kỳ skill nào, bắt buộc quét và xử lý triệt để 2 căn bệnh kiến trúc sau:
1. **Bệnh chồng chéo nhiệm vụ giữa 3 loại file:**
   - `SKILL.md` chỉ được làm **Bộ điều hướng** ($\le 150$ dòng). Nếu có lý thuyết dài → đẩy xuống `references/`.
   - `references/` chỉ được làm **Sách hướng dẫn chuyên môn**. Nếu có quy trình `Bước 1, Bước 2` → đẩy lên `SKILL.md`; nếu có link `file:///` trỏ ra ngoài → xóa bỏ và chưng cất nội dung vào trong skill.
   - `templates/` chỉ được chứa **Khung dữ liệu đầu ra sạch (`Pure Output Schema`)**. Nếu có lời dặn dò, giải thích hay nhãn kỹ thuật → cắt bỏ sạch.
2. **Bệnh đọc tràn bộ nhớ (`Missing Line-Range Pointers`):**
   - Mọi lệnh đọc từ `SKILL.md` sang `references/` phải được nâng cấp thành **Lệnh đọc phẫu thuật 4 thành phần**: `Khi nào đọc` + `File/Mục/Khoảng dòng (StartLine → EndLine)` + `Giới hạn loại trừ` + `Tại sao đọc`.

### 8. Chữa Bệnh "Vỏ Phức Tạp, Ruột Rỗng" (`Substance Over Cargo-Cult Form`)
- Một skill có nhiều thư mục nhưng bên trong `references/` toàn văn xuôi chung chung (*"hãy phân tích kỹ, viết hấp dẫn"*) là một skill hỏng.
- Khi nâng cấp `references/`, bắt buộc **Làm Đặc Ruột (`High-Density Content`)**: Thay tính từ cảm tính bằng **Con số định lượng**, chuyển văn xuôi thành **Bảng quyết định `Nếu X → Thì Y`**, và bổ sung **Cặp đối chứng `✅ Đúng / ❌ Sai`**.

### 9. Kiểm Toán Bằng Code Tự Động (`Code Gate Verification`)
- Sau khi sửa xong bất kỳ skill nào, không được chỉ tự chấm bằng mắt. Bắt buộc chạy script kiểm toán cấu trúc:
  `python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<đường_dẫn_skill>"`
  để xác nhận `100% [PASS]` trước khi bàn giao.
