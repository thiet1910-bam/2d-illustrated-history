# Giải Phẫu Nhân Vật Thương Hiệu, Cử Động Vi Mô (`Micro-Life Rig`) & 5 Đường Nét Chuyển Động 2D

## Mục 1. Giải Phẫu Nhân Vật, Khớp Cổ Cắm Sâu & Cử Động Sống Động (`Character Rig & Micro-Life Spec`)

| Nhóm cấu hình (Nếu vẽ X) | Cấu tạo giải phẫu & Chuyển động bắt buộc (Thì áp dụng Y) | Thông số kỹ thuật cứng trong JSON / Engine | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Nhân vật dẫn chuyện (`Ziro Brand Host`) & Nhân vật lịch sử (`Historical Roles`)** | Đầu tròn lớn `#FAE0C8`, viền đen `5px` `#18181C`; mỗi vai lịch sử (`king`, `general`, `spartan`, `scholar`, `hollywood_xerxes`) có mũ/vương miện, râu, áo giáp và đạo cụ riêng (`scroll` có dấu sáp đỏ, `scepter`, `quill`, `shield`, `baby_oil`). | Trụ cổ cắm sâu `neck_insert_px: 28..42px`; trong Skit bật `hide_label: true` (không vẽ biển tên dưới chân). | Vẽ hai nhân vật giống hệt nhau chỉ đổi màu áo hoặc lộ khe hở đứt cổ khi nghiêng đầu. |
| **Chớp mắt tự nhiên & Nhún nhịp thở khi thoại (`Auto Eye-Blink & Speech Bobbing`)** | Tự động chớp mắt chu kỳ **`3.1s` một lần** (khép mí mắt trong `0.13s`, lệch pha theo tọa độ `x` để 2 người không chớp cùng lúc) và nhún nhẹ thân trên `2.5px` theo nhịp giọng đọc. | `blink = True` mặc định trong `paste_char_safe`; biên độ nhún `bob_y = sin(bt * 9.5) * 2.5px`. | Để mắt nhân vật mở trừng trừng bất động suốt 40 giây như hình nộm giấy. |
| **Bước đi trên sân khấu & Đổi tư thế tay/mặt giữa nhịp (`Walk Stride & Mid-Beat Pose Swap`)** | Nhân vật bước đi ngang sân khấu với 2 chân sải luân phiên (`walk_vx`, `walk_start_bt`) và tự động đổi tư thế tay/biểu cảm đúng giây cao trào (`pose_swap_bt`). | `walk_vx: px/s`, `walk_start_bt: s`; `pose_swap_bt: s`, `swap_left_arm`, `swap_right_arm`, `swap_emotion`. | Giữ nguyên 1 cánh tay giơ cứng đơ từ đầu nhịp đến cuối nhịp dù cảm xúc câu thoại đã đảo chiều. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `beat_01` (*Skit 1*), Tướng Ba Tư cầm bức mật thư có dấu sáp đỏ (`prop_right: "scroll"`), mắt chớp tự nhiên mỗi `3.1s`; đúng giây `bt = 2.60s` khi mở thư đọc tin khẩn, thông số `pose_swap_bt: 2.60` kích hoạt đổi tay trái lên trán (`swap_left_arm: "raise"`) và nét mặt chuyển sang `shocked`.
- **❌ Ví dụ Sai (Bị cấm):** Nhân vật đứng bất động không chớp mắt, không bước chân, không đổi tay suốt cả phân đoạn.

---

## Mục 2. Bảng Trạng Thái Biểu Cảm Khuôn Mặt & Cử Chỉ Tay (`Acting & Pose States`)

| Trạng thái cảm xúc (`emotion`) | Cấu hình Mắt & Lông mày (`eyes_state`) | Cấu hình Miệng (`mouth_state`) | Cử chỉ Tay & Đạo cụ (`left_arm` / `right_arm` / `prop_right`) |
| :--- | :--- | :--- | :--- |
| **`shocked` / `scared`** *(Hoảng hốt, Sững sờ)* | Đồng tử thu nhỏ, lòng trắng mở to, lông mày chữ V ngược, thêm giọt mồ hôi thái dương. | Miệng mở rộng bầu dục dọc đen, lưỡi hồng ở đáy. | `left_arm: "raise"`, `right_arm: "point"` hoặc cầm `scroll` / `shield`. |
| **`angry` / `stern`** *(Tướng quát, Giáo sĩ cấm đoán)* | Lông mày xếch chéo xuống tâm trán (`25 độ`), mí trên cắt ngang nửa mắt. | Miệng mở gằn lộ hàm răng hoặc mép trễ xuống. | `right_arm: "point"` hoặc cầm `scepter` / `spear` chỉ thẳng về phía trước. |
| **`smug` / `sarcastic`** *(Sử gia bịa chuyện, Mỉa mai)* | Mắt lim dim nửa mí liếc ngang, một bên mày nhướng cao đắc ý. | Miệng cười nhếch mép lệch một bên. | `left_arm: "chin"`, `right_arm: "write"` cầm bút lông ngỗng `quill`. |
| **`explaining` / `neutral`** *(Báo cáo, Phân tích)* | Mắt tròn đen tiêu chuẩn, chớp mắt chu kỳ `3.1s` một lần. | Nhép miệng theo biên độ giọng đọc. | Mở lòng bàn tay hướng về phía bản đồ hoặc đạo cụ đang vẽ. |

---

## Mục 3. Bộ 5 Đường Nét Chuyển Động Vector 2D Chuẩn Ziro (`5 Animated Vector Line Primitives`)

| Mã Hiệu Ứng (`type` trong `vector_overlays`) | Hành vi Đồ họa Chuyển động Thực tế trên Sân khấu | Tham số Điều khiển trong JSON (`custom_scene_graph.vector_overlays`) | Khi nào sử dụng |
| :--- | :--- | :--- | :--- |
| **1. `live_pencil_line`** *(Bút chì 2D tự vẽ đường đi)* | Cây bút chì gỗ vàng 2D có đầu tẩy hồng di chuyển theo quỹ đạo `points`, vẽ đường liền hoặc nét đứt (`dashed: true`) tới đâu hiện tới đó theo thời gian `draw_dur`. | `bt`, `draw_dur`, `points: [[x,y],...]`, `color`, `width`, `dashed`, `show_pencil: true`, `label`. | Khi chỉ đường tiến quân, vẽ biên giới hoặc đánh bọc sườn trên bàn bản đồ (`13:56`). |
| **2. `wavy_steam_lines`** *(3 làn sóng hương/khói hình sin)* | 3 đường sóng hình sin uốn lượn bay lên liên tục (`sin(t*5.5 + phase)`) tạo hiệu ứng bốc khói nóng hoặc tỏa hương thơm dầu trẻ em. | `bt`, `x`, `y`, `height`, `spread`, `color`, `label`. | Khi tả mùi hương tỏa ra (dầu trẻ em, trà nóng) hoặc khói bốc lên từ chiến trường. |
| **3. `sparkle_bursts`** *(Sao 4 cánh lấp lánh `✦`)* | Các ngôi sao 4 cánh co giãn nhịp nhàng (`pulsing scale`) quanh vật thể hoặc cơ bắp bóng nhẫy. | `bt`, `points: [[x,y,radius], ...]`, `color: "#FFD54F"`. | Khi nhấn mạnh độ bóng bẩy, lố bịch của hình tượng Hollywood hoặc kho báu. |
| **4. `live_quill_scroll`** *(Cuộn giấy tự mở & Bút lông viết chữ)* | Cuộn giấy da dê mở rộng và cây bút lông ngỗng 2D tự động lướt viết từng dòng chữ (`lines`), tự động gạch đỏ từ cũ và bật chữ phóng đại kèm dấu chấm than `!`. | `bt`, `x`, `y`, `w`, `h`, `title`, `lines: [{bt, text, strike, color, bold}]`, `show_quill: true`. | Khi sử gia cổ đại (Herodotus) ngồi chép sử, thổi phồng số liệu hoặc ký sắc lệnh. |
| **5. `live_ruler_measure`** *(Thước đo chiều cao tự rút lên)* | Thanh thước đo dọc có vạch chia tự động kéo từ chân lên đỉnh đầu (`0.0m -> 3.0m`) kèm bảng số nhảy động theo chiều cao nhân vật. | `bt`, `x`, `y_bottom`, `y_top`, `max_val: 3.0`, `unit: "m"`, `color`. | Khi châm biếm sự phóng đại kích thước/chiều cao nhân vật (Xerxes cao 3 mét) hoặc đo quy mô. |
| **6. `checklist_board`** *(Bảng kiểm đánh dấu tích xanh `✓`)* | Bảng giấy kem treo cạnh nhân vật, lần lượt tích dấu `✓` xanh lá vào từng ô vuông đúng mốc giọng đọc liệt kê từng món đồ. | `bt`, `x`, `y`, `w`, `h`, `title`, `items: [{bt, text, checked}]`. | Khi liệt kê danh sách trang bị kỳ quặc (Áo choàng đỏ, quần đùi da, dầu trẻ em). |
