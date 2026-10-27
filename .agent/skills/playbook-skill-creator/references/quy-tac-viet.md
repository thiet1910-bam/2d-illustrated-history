# Quy Tắc Viết `SKILL.md`, Tiêu Chuẩn Làm Đặc Ruột `references/` & Thiết Kế `templates/` + `scripts/`

## Mục 1. Quy Tắc Viết Phần Mở Đầu YAML & Cấu Trúc `SKILL.md`

### 1.1. Phần Mở Đầu YAML (`Frontmatter`)
Chỉ dùng đúng **2 trường**: `name` và `description`. CẤM thêm bất kỳ trường nào khác.
- **`name`:** Viết thường, nối bằng gạch ngang (`kebab-case`), $< 64$ ký tự, trùng khớp 100% với tên thư mục chứa skill (VD: `phan-tich-bao-cao-tai-chinh`, `kiem-toan-bao-mat-code`).
- **`description`:** Phải có đủ 3 yếu tố: **LÀM GÌ (`WHAT`)** + **KHI NÀO DÙNG (`WHEN`)** + **TỪ KHÓA KÍCH HOẠT (`Trigger` / `Kích hoạt`)**.
  - **✅ Đúng:**
    ```yaml
    description: |
      Phân tích và kiểm toán hợp đồng thương mại theo 4 nhóm rủi ro pháp lý,
      xuất biên bản rà soát điều khoản kèm phương án sửa đổi.
      Kích hoạt: /ra-soat-hop-dong
    ```
  - **❌ Sai (Thiếu Khi nào dùng & thiếu Kích hoạt, hoặc chép cả Bước 1, Bước 2 vào mô tả):**
    ```yaml
    description: Bước 1 đọc hợp đồng, Bước 2 tìm lỗi, Bước 3 viết báo cáo.
    ```

### 1.2. 6 Phần Chuẩn Trong Thân `SKILL.md` (Giới Hạn Tổng $\le 150$ Dòng)
`SKILL.md` (ở Cấp độ 2, 3, 4) **chỉ làm nhiệm vụ Điều hướng (`Pure Router & Orchestrator`)**:
1. **Vai trò & Chế độ vận hành:** Nêu ngắn gọn (2–4 dòng) vai trò chuyên gia, Cấp độ phức tạp (Cấp 1–4) và Hình mẫu chức năng (Hình mẫu 1–6).
2. **Bước 0 — Kiểm tra Đầu vào / Trạng thái ổ cứng (`Entry Check`):**
   - Nếu là *Skill Dây chuyền (`Pipeline`)*: Kiểm tra xem file bàn giao từ bước trước đã có trên ổ cứng chưa.
   - Nếu là *Skill Độc lập (`Standalone`)*: Kiểm tra người dùng đã cung cấp đủ thông tin/file đầu vào chưa và phân nhánh luồng chạy (VD: Luồng A vs Luồng B).
3. **Các Bước Thực Thi & Lệnh Đọc Phẫu Thuật (`Surgical Read Pointers`):**
   - Mỗi bước chỉ đạo rõ hành động cần làm và gắn **Lệnh đọc 4 thành phần** (`Khi nào đọc` + `File/Mục/Dòng StartLine–EndLine` + `Giới hạn loại trừ` + `Tại sao đọc`).
   - **❌ Sai:** `→ Đọc references/quy-tac.md` *(Không có số dòng, không nói đọc mục nào → AI đọc tràn bộ nhớ)*.
   - **✅ Đúng:** `→ Đọc references/01-quy-tac-kiem-toan.md — Từ Mục 1 đến Mục 2 (StartLine: 1 → EndLine: 58). (Không đọc Mục 3 ở bước này). Tại sao đọc: Lấy bảng 5 tiêu chí phân loại rủi ro.`
4. **Cổng Kiểm Tra Chất Lượng (`Quality Gate Checklist`) & Điểm Dừng Cứng (`Hard Gate`):**
   - Đặt Checklist định lượng và lệnh chạy `scripts/` kiểm toán trước khi dừng trình người dùng duyệt.
5. **Rào Chắn & Danh Sách Cấm Mặc Định (`Banned Defaults`):**
   - 3–6 quy tắc cấm kèm giải thích lý do Nhân – Quả (*"Cấm làm X — Vì sẽ gây hậu quả Y"*).
6. **Đầu Ra Bàn Giao:** Ghi rõ đường dẫn lưu file kết quả và khuôn mẫu `templates/` áp dụng.

---

## Mục 2. Tiêu Chuẩn Chưng Cất "Ruột Đặc" Cho `references/` (`High-Density Content Spec`)

> **Cảnh báo chống "Rỗng Ruột":** Rất nhiều AI tạo được cây thư mục đẹp (Hiện tượng), nhưng bên trong `references/` lại viết toàn lời khuyên chung chung sáo rỗng (không có Bản chất). Khi viết bất kỳ file nào trong `references/`, **BẮT BUỘC** phải áp dụng **4 Quy Tắc Làm Đặc Ruột** dưới đây:

### 2.1. Quy Tắc 1 — Diệt Trừ Tính Từ Cảm Tính, Thay Bằng Con Số & Công Thức (`Zero-Adjective Rule`)
Cấm viết các tính từ mơ hồ mà máy hay người đều không đo đếm được. Phải quy đổi 100% thành **Thông số định lượng**:

| ❌ Cách viết Rỗng Ruột (Tính từ cảm tính — CẤM) | ✅ Cách viết Ruột Đặc (Định lượng & Kiểm chứng được — BẮT BUỘC) |
| :--- | :--- |
| *"Hãy viết phần mở đầu thật ngắn gọn, hấp dẫn và đánh trúng tâm lý."* | *"Phần mở đầu dài đúng 3–4 câu (tổng 45–65 từ): Câu 1 nêu nghịch lý số liệu; Câu 2 chỉ rõ thiệt hại; Câu 3 cam kết giải pháp."* |
| *"Kiểm tra xem hiệu năng hệ thống có nhanh và ổn định không."* | *"Đo thời gian phản hồi API p95 ≤ 200ms, tỷ lệ lỗi 5xx < 0.1% trong 1.000 request liên tiếp."* |
| *"Chọn những đoạn dữ liệu tốt nhất để đưa vào báo cáo."* | *"Chỉ lọc các bản ghi có độ tin cậy ≥ 0.85 và biên độ dao động ≥ 15% so với trung bình 30 ngày."* |

### 2.2. Quy Tắc 2 — Nén Lý Thuyết Dài Thành Bảng Quyết Định `Nếu X → Thì Y` (`Decision Tables Over Prose`)
Không viết các đoạn văn xuôi dài 10–20 dòng để giảng giải. Hãy gom thành **Bảng Quyết Định** để AI tra cứu trong 1 giây:
- Cấu trúc bảng chuẩn trong `references/`:
  `| Phân loại / Điều kiện (Nếu gặp X) | Công thức / Quy tắc xử lý bắt buộc (Thì làm Y) | Thông số ngưỡng | Lỗi sai cần tránh |`

### 2.3. Quy Tắc 3 — Mọi Quy Tắc Trọng Yếu Phải Có Cặp Đối Chứng `✅ Đúng / ❌ Sai`
AI học từ cặp đối chứng nhanh gấp 5 lần học từ lời giải thích trừu tượng. Dưới mỗi công thức quan trọng trong `references/`, phải đặt ít nhất:
- **✅ Ví dụ Đúng (Đạt chuẩn):** Minh họa cụ thể kết quả áp dụng đúng công thức + giải thích ngắn tại sao đạt.
- **❌ Ví dụ Sai (Bị cấm):** Chỉ rõ mẫu câu/cấu trúc công nghiệp mà AI hay mắc phải + lý do tại sao bị loại.

### 2.4. Quy Tắc 4 — Chia Đầu Mục Lớn Có Ranh Giới Rõ Ràng (`Section Indexing`)
- Mỗi file trong `references/` phải được chia thành các Đầu mục lớn đánh số thứ tự rõ ràng: `## Mục 1. ...`, `## Mục 2. ...`, `## Mục 3. ...`.
- Không lồng thư mục quá sâu và **tuyệt đối không đặt đường dẫn `file:///` trỏ ra ngoài thư mục skill** (mọi kiến thức cần thiết phải được chưng cất trực tiếp vào trong `references/` để skill tự chủ 100%).

---

## Mục 3. Quy Tắc Viết `templates/` Sạch & Thiết Kế `scripts/` Thực Chiến

### 3.1. Quy Tắc Viết `templates/` — Khung Dữ Liệu Đầu Ra Thuần Túy (`Pure Output Schema`)
File trong `templates/` là cái khuôn để đúc ra sản phẩm bàn giao. Do đó:
1. **Chỉ chứa cấu trúc trường dữ liệu (Tiêu đề mục, Bảng trống, Khung JSON/Markdown) và các ô điền ngắn gọn `[Điền ...]`.**
2. **❌ CẤM TUYỆT ĐỐI** viết lời dạy cách làm (*"Hãy phân tích kỹ..."*, *"Lưu ý không được..."*, *"Bước 1 làm..."*) hoặc các nhãn kỹ thuật (*"`← CỐ ĐỊNH`"*, *"`← THAY ĐỔI`"*) vào bên trong `templates/`, vì AI sẽ chép luôn những câu rác đó vào file kết quả cuối cùng! Mọi lời hướng dẫn cách điền phải nằm ở `references/`.

### 3.2. Quy Tắc Thiết Kế `scripts/` Thực Chiến (Chống Script Làm Cảnh)
Khi skill ở Cấp độ 2, 3 hoặc 4 có sử dụng `scripts/`:
1. **Code phải chạy được thật bằng dòng lệnh** (`python ...`), xử lý đúng bảng mã tiếng Việt (`utf-8`) trên cả Windows/Linux/macOS (`sys.stdout.reconfigure(encoding="utf-8")`).
2. **Phân vai rõ ràng theo cấp độ:**
   - Với **Skill Cấp độ 2 & 3:** Thường cần 1 script `scripts/validate_*.py` để tự động đếm độ dài ký tự, kiểm tra đủ các mục bắt buộc trong file đầu ra, quét các từ khóa bị cấm và trả về kết quả `PASS` / `FAIL` kèm dòng bị lỗi.
   - Với **Skill Cấp độ 4 (`Enterprise Hybrid Engine`):** Chia rõ 3 nhóm script:
     - `scripts/scanners/`: Quét thư mục dữ liệu thô đầu vào → xuất file `manifest.json` gọn nhẹ cho AI đọc.
     - `scripts/engines/`: Nhận file kế hoạch của AI → tính toán/biên dịch ra sản phẩm kỹ thuật.
     - `scripts/validators/`: Kiểm toán sản phẩm đầu ra (hoặc xuất lưới ảnh nghiệm thu thị giác `verify_sheet.png`) trước khi kết thúc.
