# Quy Trình Kiểm Duyệt Đỉnh Zoom (`Peak-Zoom QA`) & Phân Loại Lỗi P0 / P1

## Mục 1. Nguyên Tắc Bắt Lỗi Tại Đỉnh Phóng To (`Peak-Zoom Inspection vs. End-Frame Blindness`)

| Phương pháp chụp ảnh QA | Thời điểm trích xuất khung hình (`t_extract`) | Cái gì phương pháp này phát hiện được? | Đánh giá hiệu quả |
| :--- | :--- | :--- | :--- |
| **❌ Chụp ở cuối nhịp (`End-of-Beat Static Snapshot` — CẤM DÙNG ĐƠN LẺ)** | Chụp tại `t = beat.t1 - 0.1s` (khi máy quay đã lùi về `zoom = 1.00x`). | Chỉ thấy bố cục tĩnh lúc đứng yên; **bỏ lọt 100% lỗi mất chữ tiêu đề và cắt đôi người** xảy ra lúc máy quay đang phóng to ở giữa nhịp! | **Mù lỗi chuyển động (`QA Blindness`)** |
| **✅ Chụp tại Đỉnh Phóng To & Lia Máy (`Peak-Zoom & Peak-Pan Snapshot` — BẮT BUỘC)** | Tự động quét mọi frame trong nhịp để tìm `t_peak = argmax(zoom(t) + abs(pan_x(t))/500)` và chụp ngay tại khoảnh khắc đó. | Bắt sống ngay lập tức lỗi chữ chạm mép trên, thẻ bài thứ 3 bị cụt lề phải, và nhân vật đối diện bị xẻ dọc nửa người khi zoom cận! | **Bắt trúng 100% lỗi cắt xén khung hình** |
| **✅ Xem Trực Tiếp File Video (`.mp4`) Bằng `read_file`** | Mở trực tiếp file `.mp4` của Cụm sau khi xuất xong. | Kiểm tra độ mượt chuyển động 30fps, nhịp bật đạo cụ theo giọng đọc và sự hòa quyện của 3 lớp âm thanh. | **Nghiệm thu thực chiến như mắt người** |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `beat_02` (dài `6.43s`), máy quay đạt đỉnh zoom `1.22x` tại `bt = 4.80s`; trình thanh tra chụp đúng khung hình tại `bt = 4.80s` để kiểm chứng cả 3 thẻ bài và dòng tiêu đề vẫn nằm gọn trong khung an toàn.
- **❌ Ví dụ Sai (Bị cấm):** Chỉ chụp khung hình ở giây `6.30s` khi `zoom = 1.00x` rồi báo cáo hoàn hảo trong khi ở giây `4.80s` chữ bị cắt mất một nửa.

---

## Mục 2. Bảng 8 Cổng Kiểm Duyệt Cứng & Phân Loại Mức Độ Lỗi (`8 Hard Gates — P0 / P1 Matrix`)

| Mã Cổng | Tiêu chí kiểm tra định lượng | Phân loại nếu vi phạm | Hành động Debug & Sửa lỗi bắt buộc |
| :--- | :--- | :--- | :--- |
| **Gate 1: Khớp Âm Thanh (`Audio-Visual Sync`)** | `abs(video_duration - wav_sum_duration) <= 0.02s`; đạo cụ bật khớp từ khóa. | **P0 (Lỗi Chết Người)** | Kiểm tra lại mảng `wav_files` trong `audio_3layer_mixer.py` và mốc `bt` trong JSON. |
| **Gate 2: Toàn Vẹn Chữ Tiêu Đề (`HUD Text Integrity`)** | Chữ tiêu đề trên cùng cách mép trên `>= 75px` (`y_center >= 110px`), không mất nét nào tại `t_peak_zoom`. | **P0 (Lỗi Chết Người)** | Chuyển toàn bộ lệnh vẽ tiêu đề sang `Pass 2 (Post-Camera HUD Overlay)`. |
| **Gate 3: Toàn Vẹn Nhân Vật & Thẻ Bài (`No Edge Clipping`)** | Không có nhân vật nào bị cắt dọc nửa mặt/thân ở mép trái/phải; không có thẻ bài nào bị lẹm viền tại `t_peak_zoom`. | **P0 (Lỗi Chết Người)** | Bật `viewport_isolation_mode = True` khi `zoom > 1.12` và thu hẹp `X_offsets` thẻ về `[-540, 0, +540]`. |
| **Gate 4: Giải Phẫu Khớp Cổ (`Neck Joint Seamless`)** | Không có khe hở giữa cằm và cổ áo ở bất kỳ tư thế nghiêng đầu hay nhún vai nào (`neck_insert >= 28px`). | **P0 (Lỗi Chết Người)** | Tăng độ cắm sâu của trụ cổ vào sau cằm trong `ziro_stage_components.py`. |
| **Gate 5: Đầy Đủ 3 Lớp Âm Thanh (`3-Layer Soundscape`)** | Phổ âm thanh có đủ Giọng đọc (`0dB`), Tiếng động SFX tại mốc `bt` (`-6dB`) và Nhạc nền BGM (`-16dB/-9dB`). | **P0 (Lỗi Chết Người)** | Bổ sung mảng `sfx_events` còn thiếu trong JSON và chạy lại bộ trộn 3 lớp. |
| **Gate 6: Tỷ Lệ Nền Sáng Ấm (`85% Daylight Ratio`)** | Tỷ lệ cảnh nền giấy sáng ấm `#F4EFE6 / #EAE0CE` đạt `>= 80%` trong Cụm. | **P1 (Lỗi Thẩm Mỹ)** | Đổi các cảnh phân tích đang dùng nền tối không cần thiết về nền giấy kem sáng ấm. |
| **Gate 7: Chống Lặp Bố Cục (`Anti-Repetition`)** | Không có quá 2 nhịp liên tiếp dùng chung 1 `scene_template`. | **P1 (Lỗi Nhịp Điệu)** | Đổi nhịp thứ 3 sang khuôn mẫu cảnh khác hoặc ẩn dụ vật lý mới. |
| **Gate 8: Mật Độ Chuyển Động (`No Dead Stretch`)** | Không có khoảng lặng hình ảnh nào đứng im quá `2.5s` mà không có đạo cụ mới hay chuyển động nhân vật. | **P1 (Lỗi Nhịp Điệu)** | Thêm đạo cụ phụ hoặc hiệu ứng đóng dấu/chuyển biểu cảm tại nửa sau của nhịp. |

---

## Mục 3. Quy Trình Sửa Lỗi Vi Phẫu Từng Nhịp Bằng Bộ Nhớ Đệm (`Hash-Based Beat-Level Cache Fix — 1.5 Giây`)

1. **Cơ chế Lưu Đệm Từng Nhịp (`cache_beats/beat_XX_<md5_8char>.mp4`):** Trong Bước 3, Engine tính mã băm (`MD5 8 ký tự`) từ thông số của từng nhịp `beat_i` trong `beat_manifest.json` và xuất từng nhịp ra file `cache_beats/beat_XX_<hash>.mp4`, sau đó nối tức thì (`ffmpeg -f concat -c copy`) thành video của Cụm.
2. **Vi phẫu 1 Nhịp trong 1.5 Giây khi phát hiện lỗi P0/P1:**
   - Ghi biên bản theo cú pháp: `[Mã Nhịp: beat_06] · [Tại t_peak = 3.1s] · [Lỗi P0: Cắt dọc nhân vật phải khi zoom 1.26x] -> [Lệnh sửa: Bật viewport_isolation_mode = true]`.
   - Sửa đúng thông số của `beat_06` trong `beat_manifest.json`. Khi chạy lại Engine Bước 3, 10 nhịp không đổi được lấy thẳng từ `cache_beats/` (`0.0s`), Engine **chỉ render lại duy nhất `beat_06` mất ~1.5 giây**, ghép lại Cụm và chụp lại `verify_peak_zoom_<cluster_id>.png` để xác nhận **0 lỗi P0** trước khi sang Cụm kế tiếp.
