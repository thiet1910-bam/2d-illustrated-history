# Khung Phản Biện + Quy Tắc Đọc Skill Gốc

> File này phục vụ **Pha U1** (Đọc & Phản biện).
> Trả lời: **Đọc thế nào? Phản biện theo khung gì? Đánh giá mức độ ra sao?**

---

## §1. QUY TẮC ĐỌC SKILL GỐC

### Thứ tự đọc

```
1. SKILL.md
   → Ghi: tên, mô tả, kích hoạt, quy trình (bao nhiêu pha), rào chắn, đầu vào/đầu ra
   → Ghi: danh sách references/ + templates/ được trỏ

2. Mỗi file references/
   → Ghi: file nào phục vụ bước nào, nội dung tóm tắt 1-2 dòng

3. Mỗi file templates/
   → Ghi: định dạng, chỗ trống nào, dùng ở bước nào

4. Mỗi file scripts/ (nếu có)
   → Ghi: đoạn mã làm gì, chạy ở bước nào
```

### Ghi lại CẤU TRÚC GỐC

Sau khi đọc xong, ghi lại và trình cho user:

```
### CẤU TRÚC HIỆN TẠI (GHI NHẬN)

**Cây thư mục:**
skill-name/
├── SKILL.md
├── references/
│   ├── file-a.md
│   └── file-b.md
└── templates/
    └── file-c.md

**Tiêu đề từng file:**
- SKILL.md: Vai trò → Tham chiếu → Đầu vào → Quy trình (Pha 1-N) → Đầu ra → Rào chắn → Ví dụ
- references/file-a.md: §1 → §2 → §3
- references/file-b.md: §A → §B → §C
- templates/file-c.md: Phần 1 → Phần 2

**Tham chiếu chéo:**
- SKILL.md dòng X trỏ → references/file-a.md
- SKILL.md dòng Y trỏ → references/file-b.md
```

> **GHI NHẬN** = Đối chiếu khi sửa. Mặc định giữ nguyên cấu trúc.
> Nếu cấu trúc LÀ vấn đề cần sửa → ghi rõ thay đổi cấu trúc trong kế hoạch Pha U2 + user duyệt.

---

## §2. KHUNG PHẢN BIỆN 6 GÓC

Sau khi đọc skill + vấn đề user nêu, quét qua 6 góc:

### Góc 1: Mâu thuẫn

| Câu hỏi | Cách tìm |
|---------|----------|
| File A nói X, file B nói Y? | So sánh cùng thuật ngữ/số liệu giữa các file |
| Tiêu đề nói 1 đằng, nội dung 1 nẻo? | So sánh tiêu đề (§B. "2 phong cách") và nội dung (liệt kê 3 phong cách) |
| SKILL.md mô tả khác phần thân? | So sánh phần mô tả với quy trình |

**Ví dụ thực tế:** SKILL.md ghi "3 phong cách thị giác" nhưng `chien-luoc-concept.md` tiêu đề ghi "2 PHONG CÁCH THỊ GIÁC".

### Góc 2: Trùng lặp

| Câu hỏi | Cách tìm |
|---------|----------|
| Nội dung nào lặp ≥2 file? | Tìm cụm từ đặc trưng trong toàn skill |
| Lặp có CẦN THIẾT (rào chắn quan trọng) hay THỪA? | Đánh giá: lặp để ép AI nhớ = OK. Lặp vô nghĩa = xóa. |

**Ví dụ thực tế:** Quy tắc "Single Dad BẮT BUỘC" lặp 3 file → OK vì là rào chắn quan trọng.

### Góc 3: Thiếu

| Câu hỏi | Cách tìm |
|---------|----------|
| Nguồn dữ liệu gốc có gì mà skill chưa chắt lọc? | So sánh skill với file chiến lược/tài liệu gốc |
| Skill trỏ đến file không tồn tại? | Kiểm tra mọi đường dẫn trỏ trong SKILL.md |
| Bảng/danh sách thiếu mục? | So sánh danh sách trong skill với nguồn gốc |

**Ví dụ thực tế:** Skill tái tạo yêu cầu AI xác định "cấu trúc 1-12" nhưng không liệt kê 12 cấu trúc là gì.

### Góc 4: Thừa

| Câu hỏi | Cách tìm |
|---------|----------|
| Phần nào không ai dùng? | Hỏi user hoặc đánh giá dựa trên quy trình |
| File nào không được trỏ từ SKILL.md? | Tìm tên file trong SKILL.md |
| Kiến thức AI đã biết sẵn nhưng vẫn viết? | Đối chiếu với `triet-ly.md` nguyên tắc 1 |

### Góc 5: Lỗi thời

| Câu hỏi | Cách tìm |
|---------|----------|
| Đường dẫn nào sai (file đã chuyển)? | Kiểm tra mọi đường dẫn → file có tồn tại? |
| Thuật ngữ/tên nhân vật nào cũ? | Tìm tên cũ (VD: "Grace", "Black Man") |
| Ví dụ nào không còn phù hợp ngách? | So sánh ví dụ với định vị kênh hiện tại |

**Ví dụ thực tế:** File di chuyển từ `Du-an-story-us/` vào `Du-an-story-us/00_Ngach/03-dna-story-us/` → đường dẫn cũ sai.

### Góc 6: Tác dụng phụ

| Câu hỏi | Cách tìm |
|---------|----------|
| Sửa file A có ảnh hưởng file B? | Tìm nội dung sửa trong file A → tìm cùng nội dung trong file B |
| Đổi thuật ngữ → chỗ nào bị sót? | Tìm thuật ngữ cũ toàn skill |
| Đổi ví dụ SKILL.md → khuôn mẫu/tham chiếu còn khớp? | So sánh ví dụ giữa các file |

---

## §3. ĐÁNH GIÁ MỨC ĐỘ

| Mức | Định nghĩa | Ví dụ | Hành động |
|-----|-----------|-------|-----------| 
| 🔴 Nghiêm trọng | Gây lỗi quy trình / đầu ra sai | JSON mẫu dùng nhân vật sai hoàn toàn | SỬA NGAY |
| 🟡 Quan trọng | Không gây lỗi nhưng gây nhầm lẫn | Tiêu đề ghi "2 phong cách" nhưng có 3 | SỬA trong đợt này |
| 🟢 Nhỏ | Chỉnh trang / cải thiện | Thiếu 1 bối cảnh trong bảng màu | SỬA nếu kịp |

---

## §4. QUY TẮC PHẢN BIỆN GỢI Ý USER

```
1. User nói "sửa X"
   → Hỏi: X là TRIỆU CHỨNG hay NGUYÊN NHÂN GỐC?
   → VD: "Tiêu đề sai" có thể là triệu chứng. Nguyên nhân gốc = "thêm phong cách mới nhưng quên đổi tiêu đề".

2. User đề xuất giải pháp
   → Kiểm tra: Có giải pháp đơn giản hơn? Có tác dụng phụ không?
   → Nếu giải pháp user đúng → xác nhận + bổ sung nếu cần
   → Nếu giải pháp user sai → nói thẳng + đề xuất thay thế

3. User không đề xuất
   → AI tự đề xuất 1-2 giải pháp + so sánh ưu/nhược
```

---

## §5. ĐỊNH DẠNG ĐẦU RA PHA U1

```markdown
### CẤU TRÚC HIỆN TẠI (GHI NHẬN)
[Cây thư mục + Tiêu đề + Tham chiếu chéo]

### BẢNG PHẢN BIỆN

| # | Vấn đề | Góc | Nguồn | Mức | AI đánh giá | Giải pháp đề xuất |
|---|--------|-----|-------|-----|-------------|-------------------|
| 1 | [mô tả] | [1-6] | User / AI | 🔴/🟡/🟢 | [phân tích] | [đề xuất] |

### PHẢN BIỆN GỢI Ý USER (nếu có)
[Gợi ý đúng/sai? Nguyên nhân gốc? Giải pháp thay thế?]
```
