# Hệ Thống Thương Hiệu, Chữ Trần Không Khung & Danh Sách Cấm Chuẩn Ziro History

## Mục 1. Ma Trận Bảng Màu, Sân Khấu Xám Vô Cực `#CCCCCC` & Quy Hoạch Kho Nguyên Liệu

| Phân loại bối cảnh / Kho lưu trữ (Nếu gặp X) | Quy tắc màu sắc & Lưu trữ bắt buộc (Thì dùng Y) | Thông số ngưỡng | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Sân khấu phân tích tối giản (`DAYLIGHT_WARM` — Studio Gray)** | Phông nền giấy xám ấm `#CCCCCC` **liền mạch 100% từ đỉnh (`y=0`) xuống đáy (`y=1080`), TUYỆT ĐỐI KHÔNG VẼ đường kẻ ngang phân chia sàn ở 1/3 dưới**; chỉ vẽ mặt đất ở cảnh môi trường ngoài trời/trong phòng (`Split-Screen cỏ/đất`, `Sa mạc`, `Lều trại`). | Chiếm **80% – 85%** tổng số cảnh trong tập phim. | Vẽ đường kẻ ngang vô nghĩa ở `y = 855px` cắt vụn nền xám `#CCCCCC` hoặc dùng nền đen u tối cho cảnh ban ngày. |
| **Cảnh ngục tù, đàn áp, bóng tối hoặc bản đồ vệ tinh** | Nền xanh đêm than chì `#1B2234` hoặc ảnh vệ tinh thực tế làm nổi bật biên giới vàng `#EBB42D`. | Chiếm **15% – 20%** tổng số cảnh đặc thù. | Lạm dụng nền tối quá 2 nhịp liên tiếp làm mất chất hoạt hình 2D. |
| **Kho Dùng Chung (`0_kho_dung_chung`) & Kho Tư Liệu Theo Cụm (`tu_lieu_tap/<cluster_id>/`)** | `0_kho_dung_chung/` chứa `brand_ui_assets/` (Sprite Ziro Host, vân giấy, mũi tên, phôi dấu PNG) và `audio_sfx_bgm/`; ảnh riêng của tập phải chia theo Cụm tại `2_nguyen_lieu/<Ma_Tap>/tu_lieu_tap/<cluster_id>/{STT}_{beat_id}_{t0}s-{t1}s_{slug}.jpg`. | Đồng bộ `100%` theo Cụm, STT và Mốc giây `[t0-t1]` | Đổ đống phẳng không chia theo Cụm, thiếu `brand_ui_assets/` vật lý, hoặc nhét ảnh tập vào `0_kho_dung_chung`. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Cảnh *Tehran 1970 (`beat_02`)* dùng nền xám `#CCCCCC` liền mạch (không có đường kẻ sàn ngang), mở ảnh `2_nguyen_lieu/EP01_Iran/tu_lieu_tap/cum_01_Hoi_I/01_beat02_0007s-0018s_tehran_1970_shops.jpg` kèm nhân vật từ `0_kho_dung_chung/brand_ui_assets/char_ziro_host/`.
- **❌ Ví dụ Sai (Bị cấm):** Kẻ đường đen ngang `y=855` trên nền `#CCCCCC`, hoặc để ảnh tư liệu lộn xộn không có STT và mốc giây ghép.

---

## Mục 2. Nghệ Thuật Chữ Trần Không Khung (`90% Frameless Color-Pop Typography`) & Vùng An Toàn

| Thành phần chữ hiển thị (Nếu vẽ X) | Quy tắc hiển thị mượt mà chuẩn Ziro (Thì áp dụng Y) | Tọa độ & Kích thước cứng | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Tiêu đề dẫn dắt & Chữ nhấn trên sân khấu (`90% Frameless Color-Pop Text`)** | **90% chữ trên màn hình phải là Chữ Trần KHÔNG ĐÓNG HỘP VIỀN ĐEN:** Dòng dẫn phụ màu mực đen `#222222` (`26–28px`) kết hợp **Từ khóa nhấn mạnh in đậm màu Đỏ `#C62828` hoặc Xanh `#1E56A0` (`36–44px`)** gõ mượt (`typewriter`) trực tiếp trên nền. | Tiêu đề `Pass 2`: `Y_center >= 115px`; Chữ sân khấu `Pass 1`: giữ trọn trong vùng an toàn `[110..1810]px`. | Khóa cứng mọi cụm từ (`DƯỚI 35 TUỔI!`, `RẠP PHIM`, `CÀ PHÊ MỞ`...) vào các hộp viền đen đổ bóng như nút bấm PowerPoint. |
| **Thẻ ảnh tư liệu & Nhãn góc phẳng (`Archival Photo & Flat Corner Tab`)** | Khung ảnh trắng `#F8F8F6` bo góc `12px`, viền đen `3px`; nhãn năm góc trên trái (`Tehran, 1970`, `Tehran, 1980`) là **Thẻ màu phẳng (`Flat Tag`) KHÔNG viền đen dày**, chú thích dưới đáy là chữ trần nghiêng nhẹ. | Bật nảy đàn hồi (`ease_out_back`) đúng mốc từ khóa `bt`. | Vẽ nhãn năm bằng hộp viền đen dày hoặc đè hộp chữ to che khuất giữa bức ảnh lịch sử. |
| **Con dấu cao su phán quyết (`< 10% Rubber Stamp Verdict`)** | **Chỉ dùng con dấu đóng hộp (`draw_stamp`) cho `< 10%` cảnh** khi có cú chốt phủ định/phán quyết châm biếm (`[HOÀN TOÀN SAI!]`, `[100% SỰ THẬT]`, `[NONSENSE]`, `[YES]`). | Con dấu bo góc `8px`, viền đỏ/xanh kèm tiếng `stamp_slam.wav`. | Lạm dụng `draw_stamp` cho các câu mô tả thông thường làm khung hình bị đóng hộp cứng nhắc. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở cảnh chia đôi `beat_06`, bên trái hiện chữ trần `"70% dân số Iran"` (đen, `28px`) và ngay dưới là chữ trần in đậm màu đỏ **`"dưới 35 tuổi"`** (`44px`, không đóng hộp), đúng chuẩn thiết kế gốc của Ziro History.
- **❌ Ví dụ Sai (Bị cấm):** Nhét 5 cụm từ của `beat_06` vào 5 cái hộp chữ nhật viền đen xếp chồng lên nhau, hoặc hiện nhãn rác `PHÂN ĐOẠN 1.1`, `ZIRO HOST`.

---

## Mục 3. Danh Sách Cấm Mặc Định (`BANNED By Default`)

1. **❌ CẤM vẽ đường kẻ ngang phân chia sàn (`y=855`) trên Sân khấu Xám `#CCCCCC`:** Phông `#CCCCCC` phải là không gian phẳng vô cực liền mạch 100%.
2. **❌ CẤM đóng hộp viền đen tràn lan (`No Boxed Text Overuse`):** Cấm biến các cụm từ mô tả (`dưới 35 tuổi`, `học thức cao`, `rạp phim`, `cà phê mở`...) thành các hộp nút bấm cứng nhắc; bắt buộc dùng **Chữ Trần Phân Cấp Màu Sắc (`Frameless Color-Pop`)**.
3. **❌ CẤM hiển thị dữ liệu quản trị hậu trường & CẤM gán cứng tên ảnh trong code `.py`:** Mọi đường dẫn ảnh `<cluster_id>/<STT>_<beat_id>_<t0>s-<t1>s_<slug>.jpg` phải đọc động 100% từ `beat_manifest.json`.
4. **❌ CẤM phá vỡ tính liên tục không gian (`Spatial Continuity`) & CẤM để khung hình chết (`> 2.5s`):** Giữ nguyên thẻ ảnh Bên trái (`1970`) khi mở thẻ Bên phải (`1980`) để đối chiếu trực diện.
