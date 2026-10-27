# Kiến Trúc Xây Dựng Skill Đa Ngành: 4 Cấp Độ Phức Tạp & 6 Hình Mẫu Chức Năng

## Mục 1. Ma Trận 4 Cấp Độ Phức Tạp Của Skill (`4 Universal Complexity Tiers`)

> **Nguyên tắc chống "Bệnh hình thức" (`Anti-Cargo-Cult`):** Không bao giờ tạo thư mục phức tạp chỉ để trông cho nguy hiểm, và cũng không bao giờ nhồi nhét một bài toán lớn vào 1 file đơn giản. Hãy dùng **Cây Quyết Định Định Lượng** dưới đây để chọn đúng 1 trong 4 Cấp độ, và phải nắm vững **Bản chất vận hành bên trong** của từng cấp độ:

### 1.1. Cây Quyết Định Chọn Cấp Độ (Định Lượng Rõ Ràng)
```text
Tổng khối lượng quy tắc chuyên môn > 100 dòng HOẶC cần khuôn mẫu đầu ra cố định?
├─ KHÔNG (< 100 dòng, 1 nhiệm vụ đơn lẻ, không cần tính toán) ──► Chọn CẤP ĐỘ 1 (Siêu Tinh Gọn)
└─ CÓ ──► Phải xử lý dữ liệu lớn (> 10 file), tính toán phức tạp, gọi API/CLI ngoài HOẶC biên dịch file kỹ thuật?
          ├─ CÓ ──► Chọn CẤP ĐỘ 4 (Hệ Thống Lai Công Nghiệp: Code Engine + LLM)
          └─ KHÔNG ──► Có ≥ 3 phân nhánh đối tượng/chế độ/ngôn ngữ mà mỗi nhánh cần > 50 dòng quy tắc riêng?
                       ├─ CÓ ──► Chọn CẤP ĐỘ 3 (Đa Nhánh: Tách Luật Chung core/ và Luật Riêng types/)
                       └─ KHÔNG ──► Chọn CẤP ĐỘ 2 (Tiêu Chuẩn 3 Tầng: SKILL.md + references/ + templates/ + validate.py)
```

### 1.2. Giải Phẫu Chi Tiết 4 Cấp Độ (Từ Hiện Tượng Thư Mục Đến Bản Chất Vận Hành)

#### 🔹 CẤP ĐỘ 1: Siêu Tinh Gọn (`Micro / Self-Contained Skill`)
- **Khi nào dùng:** Quy tắc ngắn gọn ($< 100$ dòng), 1 nhiệm vụ đơn lẻ, không phân nhánh phức tạp, không cần tính toán bằng code (VD: Áp dụng bộ quy chuẩn đặt tên biến, kiểm tra giọng văn thương hiệu ngắn, tóm tắt biên bản họp).
- **Cấu trúc thư mục:** Chỉ **1 file `SKILL.md` duy nhất** (0 thư mục con).
- **Bản chất vận hành:** Mọi quy tắc định lượng, danh sách cấm và cặp ví dụ `✅ Đúng / ❌ Sai` nằm gọn ngay trong `SKILL.md`. AI đọc 1 lần và thực thi ngay, tốn ít bộ nhớ nhất.
- **❌ Lỗi hình thức cần tránh:** Đẻ thêm `references/` hay `templates/` chỉ để chứa 15–20 dòng chữ, làm AI tốn thêm bước đọc file vô ích.

#### 🔹 CẤP ĐỘ 2: Tiêu Chuẩn 3 Tầng (`Standard Modular Skill`)
- **Khi nào dùng:** Quy trình có 2–5 bước tuần tự, tổng kiến thức chuyên môn từ $100 - 500$ dòng, đầu ra cần tuân thủ khuôn mẫu cố định và có các tiêu chí đếm được (ký tự, số mục, từ khóa cấm).
- **Cấu trúc thư mục:**
  ```text
  ten-skill/
  ├── SKILL.md                  ← Bộ điều hướng thuần túy (≤ 150 dòng)
  ├── references/               ← Sách hướng dẫn chuyên môn tách theo Bước (01-..., 02-...)
  ├── templates/                ← Khung dữ liệu đầu ra sạch (Pure Output Schema)
  └── scripts/
      └── validate_output.py    ← (Khuyên dùng) Script kiểm toán định lượng đầu ra
  ```
- **Bản chất vận hành:**
  1. `SKILL.md` điều phối từng bước và chỉ định đọc chính xác từng mục/dòng (`StartLine–EndLine`) trong `references/` ở đúng bước cần dùng (bước 1 không đọc tài liệu của bước 3).
  2. Khi xuất kết quả, AI lấy khung từ `templates/` (không chứa rác hướng dẫn) để điền dữ liệu sạch.
  3. Trước khi báo cáo người dùng, chạy `scripts/validate_output.py` để kiểm tra bằng toán học các tiêu chí định lượng (độ dài, cấu trúc, từ cấm).

#### 🔹 CẤP ĐỘ 3: Đa Nhánh & Đa Chế Độ (`Polymorphic / Multi-Branch Skill` — Học từ `Remotion` & `Anthropic`)
- **Khi nào dùng:** Cùng một nhiệm vụ nhưng có **$\ge 3$ loại đối tượng / ngành hàng / định dạng / ngôn ngữ khác nhau**, mà mỗi loại có bộ công thức riêng $> 50$ dòng (VD: Soạn hợp đồng cho 5 loại giao dịch khác nhau; Thiết kế kịch bản cho 4 nhóm chủ đề khác nhau; Viết tài liệu đa ngôn ngữ).
- **Cấu trúc thư mục:**
  ```text
  ten-skill/
  ├── SKILL.md                  ← Có Bảng Định Tuyến Nhánh ở Bước 1 ("Route Once, Then Leave")
  ├── config/                   ← (Tùy chọn) Chứa file .json/.yaml tham số cấu hình ngoài
  ├── references/
  │   ├── core/                 ← LUẬT BẤT BIẾN (Áp dụng cho MỌI nhánh: tiêu chuẩn chất lượng, danh sách cấm chung)
  │   └── types/                ← LUẬT BIẾN THIÊN (Mỗi file = 1 nhánh riêng: loai-a.md, loai-b.md, loai-c.md...)
  ├── templates/                ← Khuôn mẫu đầu ra
  └── scripts/                  ← Script kiểm toán
  ```
- **Bản chất vận hành (Tại sao phải tách `core/` và `types/`?):**
  1. **Nguyên lý Bất biến & Biến thiên:** Mọi quy tắc chung (chiếm ~60%) phải gom vào `references/core/` để viết 1 lần duy nhất, không lặp lại. Phần khác biệt đặc thù của từng loại (chiếm ~40%) tách riêng vào từng file trong `references/types/`.
  2. **Cơ chế Định tuyến "Đọc 1 Bỏ 9" (`Single-Branch Loading`):** Ở Bước 1 của `SKILL.md`, sau khi xác định bài toán của người dùng thuộc `Loại A`, AI chỉ được phép đọc `references/core/` + **duy nhất 1 file `references/types/loai-a.md`**. **CẤM TUYỆT ĐỐI** đọc các file `loai-b.md`, `loai-c.md` còn lại. Cơ chế này giúp một skill chứa hàng ngàn dòng kiến thức của 10 nhánh khác nhau nhưng khi chạy chỉ tốn bộ nhớ bằng 1 skill nhỏ!
- **❌ Lỗi hình thức cần tránh:** Tạo ra thư mục `core/` và `types/` nhưng lại chép lặp lại quy tắc chung vào từng file trong `types/`, hoặc trong `SKILL.md` lại ra lệnh *"Đọc toàn bộ thư mục `references/types/`"*.

#### 🔹 CẤP ĐỘ 4: Hệ Thống Lai Công Nghiệp (`Enterprise Hybrid Engine` — Chuẩn Repo 50k Sao như `HeyGen HyperFrames`, `AutoClip`)
- **Khi nào dùng:** Khi bài toán đòi hỏi xử lý số lượng file đầu vào lớn (hàng chục/trăm file dữ liệu, code, media), tính toán toán học phức tạp, gọi công cụ CLI/API bên ngoài, xuất file kỹ thuật đòi hỏi độ chính xác 100% (JSON/XML/Timeline/Code), hoặc điều phối nhiều tác tử con (`Sub-agents`).
- **Cấu trúc thư mục:**
  ```text
  ten-skill/
  ├── SKILL.md                  ← Nhạc trưởng điều phối Bắt tay 4 bước giữa Code và AI
  ├── config/                   ← Tham số ngưỡng, cấu hình môi trường (settings.json)
  ├── references/               ← Chỉ chứa quy tắc suy luận cho AI + Bảng mã lỗi P0/P1/P2
  ├── templates/                ← Lược đồ dữ liệu trung gian & đầu ra (JSON/MD Schemas)
  └── scripts/
      ├── scanners/             ← Bước 1: Quét dữ liệu thô quy mô lớn → Xuất bảng tóm tắt nhẹ (manifest.json)
      ├── engines/              ← Bước 3: Đọc quyết định của AI → Tính toán nặng / Biên dịch sản phẩm thật
      └── validators/           ← Bước 4: Kiểm toán toán học / Xuất ảnh nghiệm thu thị giác (Vision Linter)
  ```
- **Bản chất vận hành — Giao Thức Bắt Tay 4 Bước Giữa Code Và AI (`4-Step Data Handshake Protocol`):**
  1. **Bước 1 — Máy Quét (`Scanner Script`):** LLM không thể đọc trực tiếp 100 file dữ liệu hay file nhị phân (video, âm thanh, bảng tính lớn). `SKILL.md` ra lệnh chạy `scripts/scanners/scan_input.py` trước tiên để máy quét toàn bộ dữ liệu thô và nén thành 1 file tóm tắt siêu nhẹ (`manifest.json` hoặc bảng chỉ số) chỉ chứa những con số AI cần biết.
  2. **Bước 2 — Não AI Suy Luận (`LLM Reasoning`):** AI đọc `manifest.json` + quy tắc trong `references/` → thực hiện phần việc mà máy không làm được (phân tích ngữ nghĩa, sáng tạo nội dung, sắp xếp cấu trúc logic) → xuất ra file kế hoạch chuẩn theo `templates/` (VD: `plan.json` hoặc bản thiết kế chuẩn).
  3. **Bước 3 — Máy Biên Dịch (`Engine Script`):** `SKILL.md` gọi `scripts/engines/build_output.py` đọc file kế hoạch của AI để thực hiện các phép tính số học chính xác tuyệt đối, cắt ghép hoặc biên dịch ra sản phẩm cuối cùng.
  4. **Bước 4 — Thanh Tra Tự Động & Mắt Thần (`Validator Script + Multimodal QA`):** Chạy `scripts/validators/verify.py` để kiểm tra sản phẩm. Nếu sản phẩm là giao diện/hình ảnh/video, script xuất ra bảng ảnh chụp (`verify_sheet.png`) để AI dùng công cụ đọc ảnh (`read_file`) kiểm tra trực tiếp bằng mắt và tự sửa hết các lỗi nghiêm trọng (`P0/P1`) trước khi trình người dùng!
- **❌ Lỗi hình thức cần tránh:** Có thư mục `scripts/` nhưng vẫn bắt AI ngồi nhẩm tính toán học bằng tay trong prompt, hoặc script chỉ in ra câu thông báo giả mà không thực sự phân tích dữ liệu.

---

## Mục 2. 6 Hình Mẫu Chức Năng Phổ Quát Cho Mọi Ngành (`6 Universal Functional Archetypes`)

Bất kể bạn tạo skill cho ngành Tài chính, Lập trình, Marketing, Pháp lý, Sản xuất nội dung hay Vận hành doanh nghiệp, hãy chọn **1 trong 6 Hình mẫu xử lý** dưới đây (hoặc tổ hợp chúng) dựa trên bản chất công việc:

| Mã | Tên Hình Mẫu Phổ Quát | Tỷ lệ `LLM` : `Code` | Cấp độ thường dùng | Bản Chất Logic Xử Lý Bên Trong `SKILL.md` | Ví Dụ Áp Dụng Đa Ngành |
| :--- | :--- | :-: | :-: | :--- | :--- |
| **Hình mẫu 1** | **Phân Kỳ $\rightarrow$ Hội Tụ Sáng Tạo**<br>(`Diverge-Converge Ideation`) | `90% LLM`<br>`10% Code` | Cấp 2, 3 | **3 Nhịp:** (1) Đọc dữ liệu nền $\rightarrow$ (2) **Phân kỳ bắt buộc ra $N$ phương án có góc tiếp cận khác hẳn nhau** (chống thiên kiến 1 góc nhìn) $\rightarrow$ (3) Chấm điểm theo tiêu chí & Hội tụ thành 1 bản hợp đồng đầu ra duy nhất. | Đề xuất chiến lược kinh doanh; Thiết kế kiến trúc hệ thống; Lên ý tưởng sản phẩm/chiến dịch. |
| **Hình mẫu 2** | **Cây Phân Nhánh & Thiết Kế Phân Cấp**<br>(`Conditional Tree & Hierarchical Planner`) | `90% LLM`<br>`10% Code` | Cấp 2, 3 | **2 Nhịp:** (1) Chạy Cây quyết định ở đầu để phân loại bài toán và chỉ nạp đúng 1 file nhánh trong `references/types/` $\rightarrow$ (2) Triển khai bản thiết kế từ tầng tổng thể xuống tầng chi tiết (`Mục 1 -> 1.1, 1.2`). | Soạn thảo hợp đồng theo loại giao dịch; Lập kế hoạch dự án; Thiết kế kịch bản/quy trình chi tiết. |
| **Hình mẫu 3** | **Cẩm Nang Thực Thi & Cổng Kiểm Toán Đầu Vào**<br>(`Action SOP & Input Gatekeeper`) | `20% LLM`<br>`80% Code` | Cấp 1, 2 | **2 Pha:** (A) Trước khi làm: Xuất phiếu hướng dẫn thao tác chuẩn (SOP) siêu gọn. (B) Sau khi thu thập: Chạy `scripts/` kiểm tra số lượng, định dạng và chất lượng dữ liệu đầu vào trước khi cho đi tiếp. | Kiểm tra bộ dữ liệu khách hàng cung cấp; Kiểm tra môi trường trước khi Deploy code; Nghiệm thu nguyên liệu thực địa. |
| **Hình mẫu 4** | **Kiến Trúc "Bánh Mì Kẹp"**<br>(`Code -> LLM -> Code Sandwich`) | `50% Code`<br>`50% LLM` | Cấp 3, 4 | **3 Tầng Kẹp Giữa:** (1) `Scanner Script` lọc & tính toán dữ liệu thô $\rightarrow$ (2) `LLM` phân tích, tổng hợp và viết nội dung khớp với con số đã tính $\rightarrow$ (3) `Validator Script` đối chiếu toán học & khóa file đầu ra. | Phân tích báo cáo tài chính/chứng khoán; Xử lý dữ liệu khảo sát lớn; Khớp nối kịch bản hậu kỳ với dữ liệu thực tế. |
| **Hình mẫu 5** | **Bộ Biên Dịch Kỹ Thuật & Nghiệm Thu Đa Phương Thức**<br>(`Deterministic Engine + Multimodal QA`) | `90% Code`<br>`10% Vision/LLM` | Cấp 4 | **3 Bước Máy:** (1) Chạy `Engine Script` biên dịch file cấu hình thành sản phẩm kỹ thuật $\rightarrow$ (2) Chạy `Validator Script` kiểm tra lỗi và xuất ảnh/log nghiệm thu $\rightarrow$ (3) `LLM` đọc ảnh/log nghiệm thu, nếu có lỗi `P0/P1` thì tự sửa và chạy lại. | Tự động hóa kiểm thử giao diện Web/App; Vẽ biểu đồ/đồ họa từ dữ liệu; Xuất file kỹ thuật (CAD/NLE/Media). |
| **Hình mẫu 6** | **Bộ Điều Hướng Đa Chế Độ**<br>(`Multi-Mode Pointer Router`) | `90% LLM`<br>`10% Code` | Cấp 2, 3 | **Luật `"Route Once, Then Leave"`:** `SKILL.md` cực ngắn ($< 60$ dòng), nhận diện chế độ người dùng gọi ở Bước 1 $\rightarrow$ Chỉ nạp duy nhất 1 file quy trình của chế độ đó, giữ sạch bộ nhớ ngữ cảnh. | Trợ lý đa nghiệp vụ (chế độ A: kiểm toán, chế độ B: báo cáo, chế độ C: dịch thuật); Bộ công cụ chuyển đổi đa định dạng. |

---

## Mục 3. 6 Mẫu Cấu Trúc Cơ Bản (`M1 → M6` — Các Viên Gạch Nền Tảng)

Khi viết chi tiết bên trong một Skill (dù ở Cấp độ 1, 2, 3 hay 4), bạn sẽ kết hợp các viên gạch cấu trúc cơ bản sau:

1. **M1 — Skill Chỉ Trỏ (`Pointer Skill`):** `SKILL.md` chỉ là bảng phân luồng ngắn gọn dẫn sang các file con theo từng chế độ.
2. **M2 — Skill Tự Đủ (`Self-Contained Skill`):** Mọi quy tắc gói gọn trong 1 file `SKILL.md` ($< 100$ dòng), không có thư mục con (tương ứng **Cấp độ 1**).
3. **M3 — Quy Trình Nhiều Pha (`Phased Workflow`):** Chia quy trình thành các Bước/Pha tuần tự; mỗi bước chỉ đọc đúng phần tài liệu tham chiếu của bước đó và có cổng kiểm tra rõ ràng.
4. **M4 — Ép Khuôn Đầu Ra (`Template-First Schema`):** Bắt buộc đọc khuôn mẫu sạch trong `templates/` trước khi xuất kết quả để đảm bảo 100% đúng cấu trúc trường dữ liệu.
5. **M5 — Cây Quyết Định (`ASCII Decision Tree`):** Đặt sơ đồ phân nhánh `├─ / └─` ngay đầu bước xử lý để AI chọn đúng nhánh quy tắc tùy theo điều kiện đầu vào.
6. **M6 — Dẫn Dắt Bằng Nguyên Lý & Rào Chắn (`Philosophy + Banned Defaults`):** Dùng cho các bước sáng tạo mở — kết hợp thông số định lượng với bảng `DANH SÁCH CẤM MẶC ĐỊNH` để chặn lối mòn công nghiệp của AI.


---

## Mục 4. 3 Ví Dụ Giải Phẫu Thực Tế: Từ Bản Chất Ra Hiện Tượng & Chống "Bệnh Hình Thức / Rỗng Ruột"

> **Tại sao phải đọc kỹ 3 ví dụ này?** Để AI hiểu rằng cấu trúc thư mục (Hiện tượng) sinh ra là để phục vụ cơ chế xử lý thông tin (Bản chất). Nếu chỉ tạo đúng tên thư mục mà bên trong viết sai cơ chế hoặc viết văn xuôi sáo rỗng thì skill đó hoàn toàn vô dụng.

### 4.1. Ví Dụ 1 (Cấp Độ 2 — Tiêu Chuẩn 3 Tầng): Bài Toán *"Rà Soát Rủi Ro Hợp Đồng Thương Mại"*
- **🔍 Bản chất bài toán:** Mọi hợp đồng đều đi qua 3 bước kiểm tra tuần tự; AI giỏi đọc hiểu câu chữ pháp lý nhưng cần bảng ngưỡng an toàn cố định và cần kiểm tra xem biên bản xuất ra có đủ các mục bắt buộc hay không.
- **📁 Hiện tượng cấu trúc đúng:** `SKILL.md` + `references/01-tieu-chi-rui-ro.md` + `templates/bien-ban-ra-soat.md` + `scripts/validate_report.py`.
- **⚖️ Đối chứng Nội dung bên trong (`❌ Hình thức rỗng ruột` vs. `✅ Đúng bản chất ruột đặc`):**
  - **❌ Làm sai (Bệnh hình thức / Rỗng ruột):** Tạo đủ 4 file nhưng bên trong `references/01-tieu-chi-rui-ro.md` lại viết văn xuôi: *"Hãy đọc kỹ hợp đồng, chú ý các điều khoản thanh toán và phạt vi phạm sao cho chặt chẽ, bảo vệ quyền lợi công ty"*. Trong `templates/bien-ban-ra-soat.md` lại ghi: *"Hãy viết nhận xét chi tiết vào đây"*.
  - **✅ Làm đúng (Ruột đặc & Tách bạch 3 tầng):**
    - Trong `references/01-tieu-chi-rui-ro.md` lập **Bảng Quyết Định Định Lượng**: `| Điều khoản | Ngưỡng an toàn bắt buộc | Dấu hiệu rủi ro đỏ (Cấm ký) | Mẫu câu sửa chuẩn |` (VD: Phạt vi phạm $\le 8\%$ giá trị hợp đồng; Thời hạn thanh toán $\le 30$ ngày kể từ ngày xuất hóa đơn).
    - Trong `templates/bien-ban-ra-soat.md`: Chỉ chứa bảng trống thuần túy và ô `[Điền mức độ rủi ro]`, không chứa bất kỳ câu hướng dẫn nào.
    - Trong `scripts/validate_report.py`: Code đếm số điều khoản đã kiểm tra và quét xem còn ô `[Điền ...]` nào bị bỏ sót không.

### 4.2. Ví Dụ 2 (Cấp Độ 3 — Đa Nhánh `core/` + `types/` Kiểu Remotion): Bài Toán *"Viết Bài Quảng Cáo Cho 5 Ngành Hàng (Bất Động Sản, Mỹ Phẩm, Phần Mềm SaaS, Giáo Dục, F&B)"*
- **🔍 Bản chất bài toán:** 5 ngành hàng có 5 công thức tâm lý khách hàng và danh sách từ cấm pháp lý hoàn toàn khác nhau. Nếu nhồi cả 5 ngành vào 1 file sẽ làm tràn bộ nhớ ngữ cảnh (*Token*) và khiến AI lấy giọng văn Bất động sản áp sang Mỹ phẩm!
- **📁 Hiện tượng cấu trúc đúng:** Tách `references/core/luat-viet-chung.md` (cấu trúc câu, độ dài đoạn) + `references/types/` gồm 5 file riêng (`bat-dong-san.md`, `my-pham.md`, `saas.md`...).
- **⚖️ Đối chứng Cơ chế vận hành (`❌ Hình thức` vs. `✅ Đúng bản chất`):**
  - **❌ Làm sai (Bệnh hình thức):** Tạo thư mục `core/` và `types/` rất đẹp, nhưng trong `SKILL.md` lại ra lệnh: *"Bước 1: Đọc toàn bộ thư mục `references/`"* (vẫn nạp cả 5 ngành vào bộ nhớ!), hoặc chép lặp lại quy tắc chung của `core/` vào từng file trong `types/`.
  - **✅ Làm đúng (Cơ chế Định tuyến "Đọc 1 Bỏ 4" — `Single-Branch Loading`):** Trong `SKILL.md` Bước 1 đặt Cây quyết định: *"Xác định ngành hàng của người dùng → Chỉ đọc `references/core/luat-viet-chung.md` (`StartLine: 1` → `EndLine: 45`) + **duy nhất 1 file** trong `references/types/` khớp với ngành đó. **Cấm tuyệt đối** mở 4 file ngành còn lại."*

### 4.3. Ví Dụ 3 (Cấp Độ 4 — Lai Code Engine 3 Tầng Kiểu HeyGen): Bài Toán *"Phân Tích 50 File CSV Doanh Thu Bán Hàng & Xuất Báo Cáo Biểu Đồ HTML"*
- **🔍 Bản chất bài toán:** LLM không thể đọc trực tiếp 50 file CSV (hàng vạn dòng số) vì sẽ tràn bộ nhớ và cộng nhầm 100%; nhưng code Python cộng số trong 0.5 giây với độ chính xác tuyệt đối, còn LLM rất giỏi nhìn bảng số tổng hợp để phân tích nguyên nhân tăng/giảm doanh thu.
- **📁 Hiện tượng cấu trúc đúng:** `SKILL.md` + `config/thresholds.json` + `references/01-quy-tac-phan-tich.md` + `scripts/scanners/aggregate_csv.py` + `scripts/engines/render_html.py` + `scripts/validators/check_report.py`.
- **⚖️ Đối chứng Giao thức phối hợp (`❌ Hình thức` vs. `✅ Đúng bản chất`):**
  - **❌ Làm sai (Bệnh hình thức):** Tạo thư mục `scripts/` nhưng bên trong chỉ viết vài dòng code in thông báo, còn trong `SKILL.md` vẫn bắt AI tự mở từng file CSV để nhẩm tính doanh thu và tự gõ tay hàng trăm dòng code biểu đồ HTML.
  - **✅ Làm đúng (Giao thức Bắt tay 4 bước `Scanner → LLM → Engine → Validator`):**
    1. **Bước 1 (`Scanner`):** `SKILL.md` gọi `aggregate_csv.py` quét 50 file CSV và nén thành 1 file `summary_manifest.json` siêu nhẹ (chỉ 30 dòng chỉ số tổng hợp).
    2. **Bước 2 (`LLM`):** AI đọc `summary_manifest.json` + `references/01-quy-tac-phan-tich.md` → viết nhận xét chiến lược vào `insights.json`.
    3. **Bước 3 (`Engine`):** `SKILL.md` gọi `render_html.py` ghép `summary_manifest.json` + `insights.json` thành file báo cáo biểu đồ `report.html`.
    4. **Bước 4 (`Validator`):** Gọi `check_report.py` kiểm tra toàn bộ số liệu trong `report.html` khớp 100% với `summary_manifest.json` trước khi trình người dùng.
