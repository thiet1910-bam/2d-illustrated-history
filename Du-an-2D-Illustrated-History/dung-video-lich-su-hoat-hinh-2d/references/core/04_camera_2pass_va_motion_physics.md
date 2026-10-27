# Giải Thuật Máy Quay 2 Lớp (`2-Pass Camera`) & Vật Lý Chuyển Động 2D

## Mục 1. Giải Thuật Máy Quay 2 Lớp — Chữ Động Không Khung & Chống Cắt Viền (`2-Pass Rendering Law`)

| Lớp Render (Thứ tự thực thi) | Thành phần nào ĐƯỢC vẽ ở lớp này? | Phép biến đổi Camera (`Zoom / Pan`) | Tại sao bắt buộc tách 2 lớp? |
| :--- | :--- | :--- | :--- |
| **LỚP 1 (`Pass 1: World Stage Canvas`)** | Bối cảnh sân khấu (`Background`), Nhân vật (`Characters`), Thẻ ảnh tư liệu (`Archival Photo Cards`), Đạo cụ, Mũi tên cong, Con dấu gắn với vật thể. | **CÓ ÁP DỤNG** `apply_camera(world_canvas, zoom, pan_x, pan_y)` kèm khóa vùng an toàn nghịch đảo (`world_safe_box`). | Tạo chiều sâu điện ảnh, lia máy từ Bên trái sang Bên phải hoặc đẩy cận vào đạo cụ theo giọng đọc. |
| **LỚP 2 (`Pass 2: Post-Camera Kinetic Text`)** | Tiêu đề dẫn chuyện không khung (`Frameless Typewriter Stage Title`) hoặc Con dấu tiêu đề đỉnh (`Stamp Header`) tại `y_center >= 115px`. | **KHÔNG ÁP DỤNG CAMERA (`zoom = 1.0, pan = 0`)** — Vẽ trực tiếp lên khung hình `1920x1080` sau khi Lớp 1 đã zoom xong. | Đảm bảo **100% dòng chữ dẫn chuyện gõ mượt mà, không đóng hộp thô cứng và không bao giờ bị cắt mất nét** khi Lớp 1 phóng to `1.25x`! |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `beat_02` (*Tehran 1970*), Lớp 1 mở thẻ ảnh `Tehran, 1970` ở bên trái rồi lia nhẹ sang phải khi thẻ *Đại lộ Tehran, Rạp phim, Cà phê mở* bật ra; sau khi Lớp 1 zoom xong, Lớp 2 gõ mượt dòng chữ trần `"BÊN TRÁI: TEHRAN THẬP NIÊN 1970"` màu xanh `#204E8A` tại `y = 115px` (không khung hộp, không có nhãn `PHÂN ĐOẠN 1.1`, không có phụ đề đáy).
- **❌ Ví dụ Sai (Bị cấm):** Vẽ chữ tiêu đề ở Lớp 1 trước khi zoom làm chữ bị xén mất nửa đầu, hoặc vẽ hộp chữ nhật viền đen cứng nhắc kèm hộp phụ đề Karaoke dưới đáy màn hình.

---

## Mục 2. Luật Cô Lập Khung Hình & Khóa Vùng An Toàn Nghịch Đảo (`Viewport Safe-Box Law`)

| Tình huống bố cục & Góc máy (Nếu gặp X) | Quy tắc cô lập khung hình bắt buộc (Thì thực hiện Y) | Ngưỡng toán học cứng | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Cảnh có $\ge 2$ nhân vật/nhóm đứng hai bên VÀ máy quay lia cận (`zoom > 1.12`, `abs(pan_x) > 80`)** | Tự động bật `viewport_isolation_mode = True`: Ánh xạ ngược vùng an toàn `[96..1824] x [182..952]` vào tọa độ sân khấu hoặc chỉ lấy nét phe đang nói trong pha zoom cận. | Không có bất kỳ nhân vật hay thẻ bài nào bị đường biên cắt `(x0, y0, x1, y1)` xẻ ngang người. | Vẽ cố định 2 nhân vật rồi zoom lệch tâm làm nhân vật đối diện bị lưỡi kéo màn hình **xẻ dọc mất nửa mặt/nửa vai** ở mép! |
| **Cảnh Sân Khấu Liên Hoàn Trái – Phải (`Left 1970 vs Right 1980`)** | Khi `beat_02` tả Bên trái: đặt thẻ chính ở `x = 680` và các thẻ chi tiết ở `x = 1360`; sang `beat_03` tả Bên phải: giữ thẻ 1970 ở `x = 640` và đập thẻ 1980 xuống `x = 1360`. | Giữ tính liên tục 100% giữa câu trước và câu sau đúng theo từ khóa *"Bên trái"* / *"Bên phải"*. | Xóa sạch cảnh Bên trái hoặc biến câu *"Bên trái"* thành 3 thẻ dàn hàng ngang khắp màn hình. |
| **Cảnh Chia Đôi Màn Hình (`Split-Screen 50/50`)** | Chia đôi dọc tại `x = 960`; nửa trái (`0..960`) dành cho phe A (VD: Giới trẻ `< 35 tuổi`), nửa phải (`960..1920`) dành cho phe B (VD: Giáo sĩ thế kỷ 7). | Giữ vạch chia và toàn bộ nhân vật, con dấu của cả 2 phe nằm gọn trong vùng an toàn sau khi zoom. | Đặt chữ trong thẻ quá dài tràn ra ngoài mép thẻ hoặc đè lên đầu nhân vật. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `beat_06` (*Giới trẻ dưới 35 tuổi lướt Instagram vs Hội đồng giáo sĩ già thế kỷ 7*), nửa trái hiện 3 sinh viên cầm điện thoại kèm các nhãn bật nảy `DƯỚI 35 TUỔI!`, `+ HỌC THỨC CAO`, `TOP INSTAGRAM THẾ GIỚI!` và tim bay; tới giây `6.2s` khi giọng đọc chuyển sang *"Nhưng họ lại bị cai trị..."*, nửa phải bật lên 3 giáo sĩ cùng con dấu `HỘI ĐỒNG GIÁO SĨ GIÀ` và `ÁO CHOÀNG THẾ KỶ THỨ 7!`.
- **❌ Ví dụ Sai (Bị cấm):** Chỉ vẽ 1 bức ảnh tĩnh suốt 12 giây không có tiến triển theo giọng đọc.

---

## Mục 3. Phương Trình Vật Lý Đàn Hồi, Gõ Chữ & Rung Chấn (`Spring, Typewriter & Shake Physics`)

1. **Hiệu ứng gõ chữ mượt mà (`Smooth Typewriter Reveal`):**
   - Số ký tự hiển thị tại thời điểm `bt`: `n_chars = int(len(text) * clamp01((bt - t0) / reveal_dur))`, nhưng **luôn căn giữa theo tổng chiều rộng của cả câu hoàn chỉnh** để dòng chữ gõ từ trái sang phải mượt như lụa mà không bị giật tâm!
2. **Hàm bật nảy thẻ ảnh / con dấu (`Overshoot Back Spring`):**
   - Mọi thẻ ảnh tư liệu, đạo cụ, con dấu khi xuất hiện tại mốc `bt` đi qua hàm `ease_out_back((bt - t0) / 0.35)` (nảy nhẹ lên `1.08x` rồi đầm chắc tại `1.00x`), kết hợp rung chấn `shake_amp = 12px * (1 - dt/0.4)` khi đóng dấu đỏ chốt hạ.
