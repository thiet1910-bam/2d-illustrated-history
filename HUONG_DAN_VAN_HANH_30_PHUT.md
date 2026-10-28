# HƯỚNG DẪN VẬN HÀNH SẢN XUẤT VIDEO 30 PHÚT (`ZIRO-HISTORY-STUDIO-V3`)
*(Dành cho Người dùng — Dễ dùng cho người mới, tiết kiệm tối đa Token AI, tự đóng gói lưu trữ 0 tốn Token)*

---

## BƯỚC 0: KIỂM TRA MÁY LẦN ĐẦU (CHỈ CHẠY 1 LẦN KHI MỚI NHẬN BÀN GIAO)
1. Nhấp đúp chuột chạy file **`KIEM_TRA_HE_THONG.bat`** nằm ngay ngoài thư mục `Ziro-History-Studio-v3/`.
2. Hệ thống sẽ tự động kiểm tra thư viện hình ảnh/âm thanh và tự dò tìm công cụ xuất video `FFmpeg / FFprobe` trên máy tính của bạn. Khi màn hình báo **`[PASS]`**, máy bạn đã sẵn sàng 100%!

---

## BƯỚC 1: CHUẨN BỊ ĐẦU VÀO CHO TẬP MỚI (CON NGƯỜI LÀM — 1 PHÚT)
1. Trong phần mềm **Antigravity IDE**, chọn `File -> Open Folder` và mở trực tiếp thư mục gốc **`Ziro-History-Studio-v3`** *(nơi bạn đặt bộ công cụ này)*.
   - *Quan trọng:* Khi mở đúng thư mục `Ziro-History-Studio-v3`, AI sẽ tự động đọc file luật `GEMINI.md` và `SKILL.md` ngay lập tức mà bạn không cần giải thích lại cách dựng video.
2. Mở thư mục con `episodes/` và tạo một thư mục tên tập mới (viết liền không dấu), ví dụ: `episodes/EP01_TrieuTien/1_input/`.
3. Thả file đầu vào của bạn vào `1_input/` (Hỗ trợ cả 2 trường hợp):
   - **Cách đầy đủ (3 file — nếu bạn đã có kịch bản đạo diễn):**
     1. `voice.MP3` *(File thu âm nguyên khối dài 10 – 35 phút)*
     2. `kich_ban_loi_dan.txt` *(Lời đọc trơn khớp 100% với file thu âm)*
     3. `kich_ban_chia_hoi.txt` *(Kịch bản có chia `HỒI I..VII`, `Phân đoạn 1.1`, ghi chú `(Hình ảnh: ...)` và các đoạn đối thoại `(Chuyển nhịp Skit #1...)`)*
   - **Cách tối giản (Chỉ có 2 file: `Text trơn + Voice`):**
     - Chỉ cần bỏ `voice.MP3` và `kich_ban_loi_dan.txt` vào `1_input/`. Khi chạy Bước 2, hệ thống sẽ tự động chia `HỒI`, nhận diện hội thoại `Skit` và tạo giúp bạn file `kich_ban_chia_hoi.txt`!

---

## BƯỚC 2: BẢO AI QUÉT BẢN ĐỒ TẬP & LÀM CUỐN CHIẾU TỪNG CỤM (AI LÀM)
Trên khung chat của Antigravity IDE, bạn chỉ cần gõ các câu lệnh ngắn gọn sau:

### 1. Lệnh khởi tạo Tập (Chạy 1 lần đầu tiên cho mỗi tập):
> *"Quét phân cụm tập `EP01_TrieuTien` và cho tôi xem bảng kế hoạch các cụm."*
- AI sẽ chạy `scan_clusters.py`, tự động chia 30 phút thành khoảng **15 – 18 Cụm nhỏ** (mỗi cụm dài `1.5 – 2.5 phút`, tách riêng các đoạn `Skit` hài kịch thành cụm riêng) và lưu vào `2_assets/timelines/cluster_plan.json`.

### 2. Lệnh dựng cuốn chiếu từng Cụm (Làm chắc từng 1–2 Cụm một):
> *"Thực hiện trọn gói `cum_01_Hoi_I` của tập `EP01_TrieuTien` chuẩn phong cách Ziro History."*
- Với mỗi cụm, AI sẽ tự động làm khép kín:
  1. Cắt âm thanh khớp `0.000s` + trích xuất dữ liệu nhép miệng `30fps` cho **Giáo Sư Áo Hoodie Đỏ** (hoặc 2 nhân vật đối đáp nếu là cụm `Skit`).
  2. Duyệt tìm (`--list`) và tải ảnh lịch sử thật từ Wikimedia Commons có gắn mã cụm `c01_`, `c02_`... (hoặc dùng bản đồ vệ tinh toàn cầu NASA `world_satellite.jpg` / vẽ nền sân khấu 2D cho cảnh Skit).
  3. Lập trình hoạt cảnh HTML5 (`0%` phụ đề đáy, `0%` thanh tiêu đề đỉnh; `100%` chữ từ khóa `Typewriter`, đồng hồ số quay vọt, bản đồ vệ tinh Spotlight, Skit làm mờ chữ `38%`).
  4. Chụp bảng `Peak-Zoom QA` tự kiểm tra mắt trước $\rightarrow$ Hòa âm 3 lớp `48kHz` $\rightarrow$ Xuất file `4_output/clusters/cum_XX.mp4`.

### 💡 Mẹo tiết kiệm Token cực mạnh khi làm tới Cụm 5, Cụm 10, Cụm 17:
- Cứ sau mỗi **3 – 4 Cụm** đã duyệt xong, cuộc trò chuyện sẽ dài ra. Bạn chỉ cần gõ lệnh **`/compact`** trên khung chat (hoặc mở hẳn 1 tab Chat mới tinh!) rồi nhắn:
  > *"Đọc `cluster_plan.json` của `EP01_TrieuTien` và làm tiếp Cụm tiếp theo đang `PENDING`."*
- Vì toàn bộ tiến độ và quy tắc đã nằm sẵn trên ổ cứng (`cluster_plan.json` + `SKILL.md`), tab Chat mới tinh sẽ làm tiếp các cụm sau mượt mà như mới mà tốn cực ít token!

---

## BƯỚC 3: GỘP VIDEO 30 PHÚT, DỌN RÁC & CẤT RA KHO LƯU TRỮ NGOÀI (CON NGƯỜI TỰ LÀM — 0 TỐN TOKEN AI!)

Sau khi bạn đã có đủ các file `cum_01.mp4` ... `cum_17.mp4` trong `episodes/<Ma_Tap>/4_output/clusters/`:

1. **Nhấp đúp chuột** vào file **`GOP_VIDEO_VA_DON_RAC.bat`** nằm ngay ngoài thư mục `Ziro-History-Studio-v3/`.
2. Nhập mã tập (ví dụ: `EP01_TrieuTien`) $\rightarrow$ Gõ phím **`3`** rồi nhấn `Enter`:
   - Máy tính sẽ tự động nối toàn bộ các cụm thành 1 file duy nhất **`4_output/master/EP01_TrieuTien_Master.mp4`** (chỉ mất ~3 giây, giữ nguyên chất lượng gốc 100%, độ lệch âm thanh `0.0ms`).
   - Đồng thời tự động **xóa sạch 100% thư mục rác tạm `.cache/EP01_TrieuTien/`** (giải phóng hàng trăm MB file `.wav` cắt lẻ).
3. Mở thư mục `Ziro-History-Studio-v3/episodes/`, bấm chuột phải **`Cut` (Cắt)** nguyên thư mục `EP01_TrieuTien` và **`Paste` (Dán)** sang ổ cứng Kho Lưu Trữ riêng của bạn!
   - Thư mục `Ziro-History-Studio-v3` quay về trạng thái rỗng sạch tinh tươm, sẵn sàng cho tập tiếp theo.
   - *(Lưu ý: Nếu sau này bạn muốn sửa lại 1 cụm của tập cũ, chỉ cần copy thư mục tập đó từ Kho Lưu Trữ bỏ ngược vào lại `episodes/`, mọi thứ chạy lại ngay lập tức!)*
