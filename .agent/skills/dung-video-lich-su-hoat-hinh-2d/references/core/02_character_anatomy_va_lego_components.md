# Giải Phẫu Nhân Vật Thương Hiệu, Quy Tắc Khớp Cổ & Thư Viện Khối Lego 2D

## Mục 1. Giải Phẫu Nhân Vật Thương Hiệu & Hệ Thống Nhân Vật Lịch Sử (`Character Rig Spec`)

| Nhóm nhân vật (Nếu vẽ X) | Cấu tạo giải phẫu & Trang phục bắt buộc (Thì áp dụng Y) | Thông số kỹ thuật cứng | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Nhân vật dẫn chuyện thương hiệu (`Ziro Brand Host`)** | Đầu tròn lớn màu da sáng `#FAE0C8`, tóc nâu nhô đỉnh đầu, mặc **áo Hoodie đỏ `#D93829`** có mũ trùm sau gáy, dây rút trắng và túi bụng. | Viền ngoài `5px` đen `#18181C`; đầu `144x152px`, thân `176x210px`, bóng đổ dưới chân elip mờ. | Vẽ thân hình thang trơn tuột không tay, không cổ áo hoặc đổi màu áo sang màu khác. |
| **Nhân vật lịch sử / Đế chế cổ đại (`Historical Figures`)** | Giữ nguyên tỷ lệ đầu tròn Ziro nhưng gắn phụ kiện định danh: Vua Ba Tư đội vương miện vàng `#EBB42D` + râu quai nón; Lính Sparta mặc quần đùi đỏ + áo choàng; Sử gia Hy Lạp mặc áo choàng trắng lệch vai. | Có ít nhất **2 đạo cụ định danh trên người** (vương miện, giáo, cuộn giấy, khăn xếp) để nhìn 1 giây nhận ra ngay. | Vẽ hai nhân vật đối lập giống hệt nhau chỉ khác mỗi màu áo trơn. |
| **Quy tắc Khớp Cổ Cắm Sâu (`Deep Neck-Overlap Law`)** | Trụ cổ phải được vẽ ở lớp giữa (`Layer Mid`), đầu cắm sâu vào bên trong cổ áo tối thiểu `15px`, phần trên của trụ cổ cắm sâu vào sau cằm từ `28px – 42px`. | `neck_top = head_bottom - 35px`; `neck_bottom = torso_top + 18px`; tuyệt đối không dùng phép toán cộng tọa độ rời rạc. | Đặt đáy đầu chạm đúng đỉnh cổ (`gap = 0px`) khiến khi nhân vật nhún thở bị lộ khe hở đứt lìa đầu. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Nhân vật dẫn chuyện mặc áo Hoodie đỏ `#D93829`, trụ cổ có tọa độ `y1 = cy - 42`, `y2 = cy + 18` nằm kẹp giữa lớp Thân/Cổ áo và lớp Đầu; khi đầu nghiêng `6 độ` và nhún `8px`, khớp cổ vẫn liền mạch 100%.
- **❌ Ví dụ Sai (Bị cấm):** Vẽ đầu là hình tròn ở `y = 300`, thân là hình chữ nhật ở `y = 410` không có trụ cổ nối giữa, tạo ra khoảng trống nền giấy cắt ngang cổ nhân vật.

---

## Mục 2. Bảng Trạng Thái Biểu Cảm Khuôn Mặt & Cử Chỉ Tay (`Acting & Pose States`)

| Trạng thái cảm xúc (`emotion`) | Cấu hình Mắt & Lông mày (`eyes_state`) | Cấu hình Miệng (`mouth_state`) | Cử chỉ Tay & Đạo cụ (`arm_pose`) |
| :--- | :--- | :--- | :--- |
| **`shocked` / `scared`** *(Bị kết án, hoảng hốt)* | Đồng tử thu nhỏ, lòng trắng mở to, lông mày dựng đứng chữ V ngược, thêm 2 giọt mồ hôi thái dương. | Miệng mở rộng hình bầu dục dọc đen, lưỡi hồng ở đáy. | Hai tay giơ cao ngang đầu hoặc ôm má. |
| **`angry` / `stern`** *(Giáo sĩ cấm đoán, Tướng quát)* | Lông mày xếch chéo xuống tâm trán (`góc 25 độ`), mí trên cắt ngang nửa mắt. | Miệng mở gằn lộ hàm răng nghiến hoặc mép trễ xuống. | Tay phải chỉ thẳng về phía trước hoặc cầm búa/dấu đóng sập xuống. |
| **`smug` / `sarcastic`** *(Châm biếm Skit, Sử gia bịa chuyện)* | Mắt lim dim nửa mí nhìn liếc sang ngang, một bên mày nhướng cao. | Miệng cười nhếch mép lệch một bên. | Một tay chống cằm hoặc cầm bút lông gà viết sổ. |
| **`explaining` / `neutral`** *(Dẫn chuyện phân tích)* | Mắt tròn đen tiêu chuẩn, chớp mắt chu kỳ `3.2s` một lần (`3 frames`). | Nhép miệng 3 nấc (`closed / half / open`) theo biên độ giọng đọc. | Một tay mở lòng bàn tay hướng về phía thẻ bài/bản đồ vừa bật lên. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Trong *Skit 1 (`beat_22`)*, khi viên tướng Ba Tư hỏi *"Bọn chúng mặc cái quái gì thế?"*, biểu cảm chuyển từ `neutral` sang `shocked` kèm giọt mồ hôi và tay chỉ thẳng vào lính Sparta.
- **❌ Ví dụ Sai (Bị cấm):** Nhân vật đứng đơ như tượng gỗ với đúng 1 nét mặt cười mỉm trong suốt cảnh bị bỏ tù và cảnh chiến trận.

---

## Mục 3. Thư Viện Khối Đồ Họa Lắp Ghép Dùng Chung (`Reusable Lego Components`)

| Mã Khối Lego | Cấu trúc hiển thị vật lý | Tham số điều khiển (`Props`) | Khi nào sử dụng |
| :--- | :--- | :--- | :--- |
| **`Lego_EvidenceCard`** | Khung chữ nhật bo góc `18px`, nền `#FCF9F2`, viền đen `4px`, bóng đổ cứng `6px`, chứa Hình vẽ trung tâm + Nhãn chữ đáy. | `(x, y, w, h, title, icon_type, tilt_deg)` | Khi lời dẫn liệt kê các sự kiện, vật chứng, tội danh hoặc so sánh các mục. |
| **`Lego_RubberStamp`** | Khung viền kép màu đỏ máu `#CD2020`, chữ in hoa đậm nghiêng `-14 độ`, đập từ độ phóng đại `scale = 2.2 -> 1.0`. | `(x, y, stamp_text, trigger_bt)` | Khi lời dẫn nhắc tới lệnh cấm, bác bỏ, kết tội (`BỊ CẤM`, `TỘI ĐỒ`, `BỊA ĐẶT`). |
| **`Lego_PrisonBars`** | Hệ thống thanh sắt dọc màu xám thép `#2C3038` có ánh kim và thanh ngang khóa chặt, sập từ đỉnh màn hình `y = -1080 -> 0`. | `(bar_count, slam_bt, lock_target_x)` | Khi lời dẫn nói về bắt giam, đàn áp, tước đoạt tự do, cấm vận. |
| **`Lego_SplitDivider`** | Đường cắt dọc hoặc chéo chính giữa màn hình (`x = 960`), viền đen `6px` kèm huy hiệu đối lập `VS` hoặc mũi tên thời gian. | `(left_theme, right_theme, badge_text)` | Khi đối chiếu 2 thời kỳ (`1970 vs Nay`), 2 góc nhìn (`Hollywood vs Lịch sử thật`). |
