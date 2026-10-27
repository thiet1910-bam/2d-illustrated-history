# Quy Trình Kiểm Duyệt Đỉnh Zoom (`Peak-Zoom QA`) & Phân Loại Lỗi P0 / P1

## Mục 1. Nguyên Tắc Bắt Lỗi Tại Đỉnh Phóng To (`Peak-Zoom Inspection vs. End-Frame Blindness`)

| Phương pháp chụp ảnh QA | Thời điểm trích xuất khung hình (`t_extract`) | Cái gì phương pháp này phát hiện được? | Đánh giá hiệu quả |
| :--- | :--- | :--- | :--- |
| **❌ Chụp ở cuối nhịp (`End-of-Beat Static Snapshot` — CẤM DÙNG ĐƠN LẺ)** | Chụp tại `t = beat.t1 - 0.1s` (khi máy quay đã lùi về `zoom = 1.00x`). | Chỉ thấy bố cục tĩnh lúc đứng yên; **bỏ lọt 100% lỗi mất chữ tiêu đề và cắt đôi người** xảy ra lúc máy quay đang phóng to ở giữa nhịp! | **Mù lỗi chuyển động (`QA Blindness`)** |
| **✅ Chụp tại Đỉnh Phóng To & Lia Máy (`Peak-Zoom & Peak-Pan Snapshot` — BẮT BUỘC)** | Tự động quét mọi frame trong nhịp để tìm `t_peak = argmax(zoom(t) + abs(pan_x(t))/500)` và chụp ngay tại khoảnh khắc đó (`verify_peak_zoom_<cluster_id>.png`). | Bắt sống ngay lập tức lỗi chữ chạm mép trên, thẻ bài bị cụt lề phải, và nhân vật đối diện bị xẻ dọc nửa người khi zoom cận! | **Bắt trúng 100% lỗi cắt xén khung hình** |
| **✅ Bảng Ghép Khung Hình 1fps (`Contact Sheet .jpg`) + Đo Phổ FFmpeg (`scdet` & `volumedetect`)** | Xuất bảng lưới `sheet_<cluster_id>.jpg` xem trực tiếp bằng `read_file` kết hợp đo `volumedetect` / `RMS dBFS` của file `.mp4`. *(Lưu ý: Mở ảnh `.png`/`.jpg` bằng `read_file`, tránh gọi `read_file` trực tiếp trên nhiều file nhị phân `.mp4` nặng gây tràn bộ đệm)*. | Kiểm chứng bằng mắt toàn bộ chuỗi chuyển động, chữ thoại trên đầu làm mờ `38%`, 5 đường nét vector và xác minh số liệu âm lượng SFX (`-28..-35 dBFS`). | **Nghiệm thu Kép: Mắt Thật + Số Liệu Thật** |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `cum_03_Skit_1`, trình thanh tra chụp `verify_peak_zoom_cum_03_Skit_1.png` + bảng lưới `sheet_our_cum03_skit1_v2.jpg` để kiểm tra bằng mắt (`[👁️ Đã kiểm tra bằng mắt]`) chữ thoại làm mờ `38%` trên đầu nhân vật, đồng thời chạy FFmpeg đo xác nhận `mean_volume = -18.1 dB`, SFX RMS `-33.8 dBFS` (`[📊 Đã xác minh bằng số liệu]`).
- **❌ Ví dụ Sai (Bị cấm):** Chỉ chụp khung hình cuối nhịp khi `zoom = 1.00x` rồi báo cáo hoàn hảo mà không kiểm tra lúc máy quay đạt đỉnh zoom.

---

## Mục 2. Bảng 8 Cổng Kiểm Duyệt Cứng & Phân Loại Mức Độ Lỗi (`8 Hard Gates — P0 / P1 Matrix`)

| Mã Cổng | Tiêu chí kiểm tra định lượng | Phân loại nếu vi phạm | Hành động Debug & Sửa lỗi bắt buộc |
| :--- | :--- | :--- | :--- |
| **Gate 1: Khớp Âm Thanh (`Audio-Visual Sync`)** | `abs(video_duration - wav_sum_duration) <= 0.02s`; đạo cụ và lượt thoại bật khớp từ khóa. | **P0 (Lỗi Chết Người)** | Kiểm tra lại mảng `wav_files` trong `audio_3layer_mixer.py` và mốc `bt` trong JSON. |
| **Gate 2: Toàn Vẹn Chữ Tiêu Đề & Thoại Trên Đầu (`HUD & Skit Speech Integrity`)** | Ở Hồi phân tích: tiêu đề `Pass 2` có `y_center >= 110px`. Ở Skit: `hud_banner.style = "NONE"`, chữ thoại đặt trên đầu người nói và làm mờ `38%` (`opacity: 0.38`) theo lượt thoại. | **P0 (Lỗi Chết Người)** | Chuyển tiêu đề Hồi sang `Pass 2`; ở Skit xóa sạch HUD đỉnh và dùng `skit_speech_captions` có `dim_after_bt`. |
| **Gate 3: Toàn Vẹn Nhân Vật & Sân Khấu (`No Edge Clipping`)** | Không có nhân vật nào bị cắt dọc nửa mặt/thân ở mép trái/phải; Skit dùng bối cảnh 2D toàn màn hình (`skit_stage_bg`), không thả thẻ ảnh viền trắng đè lên cảnh đối thoại. | **P0 (Lỗi Chết Người)** | Bật `viewport_isolation_mode = True` khi `zoom > 1.12` và khai báo `skit_stage_bg` chuẩn cho Skit. |
| **Gate 4: Giải Phẫu Khớp Cổ & Cử Động Vi Mô (`Neck Joint & Micro-Life`)** | Không lộ khe hở cổ (`neck_insert >= 28px`); nhân vật có chớp mắt `3.1s`, nhún thoại, bước đi (`walk_vx`) hoặc đổi tay (`pose_swap_bt`). | **P0 (Lỗi Chết Người)** | Tăng độ cắm sâu của trụ cổ và bổ sung `pose_swap_bt` / `walk_vx` trong `actors`. |
| **Gate 5: Đầy Đủ 3 Lớp Âm Thanh Êm Dịu (`Calibrated 3-Layer Soundscape`)** | Phổ âm thanh có đủ Giọng đọc (`0dB`), SFX gốc Ziro (`-14.5dB` gain / `-28..-35 dBFS` RMS) và BGM tự hạ âm (`-20.0dB` / `-12.5dB`). | **P0 (Lỗi Chết Người)** | Đồng bộ `ziro_authentic_sfx` và hạ `gain_db` về `-14.0..-16.5 dB` để SFX êm dịu dưới giọng đọc. |
| **Gate 6: Tỷ Lệ Nền Sáng Ấm (`85% Daylight Ratio`)** | Tỷ lệ cảnh nền sáng ấm (`DAYLIGHT_WARM` / `SAND_EMPIRE`) đạt `>= 80%` trong Cụm. | **P1 (Lỗi Thẩm Mỹ)** | Đổi các cảnh phân tích đang dùng nền tối không cần thiết về nền sáng ấm. |
| **Gate 7: Chống Lặp Bố Cục (`Anti-Repetition`)** | Không có quá 2 nhịp liên tiếp dùng chung 1 `scene_template` hoặc 1 bối cảnh đứng yên. | **P1 (Lỗi Nhịp Điệu)** | Đổi nhịp thứ 3 sang khuôn mẫu cảnh khác hoặc bối cảnh `skit_stage_bg` mới. |
| **Gate 8: Mật Độ Chuyển Động & Đường Nét Vector (`No Dead Stretch`)** | Không có khoảng lặng hình ảnh quá `2.5s`; tận dụng 5 đường nét chuyển động (`live_pencil_line`, `wavy_steam_lines`, `sparkle_bursts`, `live_quill_scroll`, `live_ruler_measure`). | **P1 (Lỗi Nhịp Điệu)** | Thêm hiệu ứng đường nét vector chuyển động hoặc đổi tư thế tay tại nửa sau của nhịp. |

---

## Mục 3. Quy Trình Sửa Lỗi Vi Phẫu Từng Nhịp Bằng Bộ Nhớ Đệm (`Hash-Based Beat-Level Cache Fix — 1.5 Giây`)

1. **Cơ chế Lưu Đệm Từng Nhịp (`cache_beats/beat_XX_<md5_8char>.mp4`):** Trong Bước 3, Engine tính mã băm (`MD5 8 ký tự`) từ thông số của từng nhịp `beat_i` trong `beat_manifest.json` và xuất từng nhịp ra file `cache_beats/beat_XX_<hash>.mp4`, sau đó nối tức thì (`ffmpeg -f concat -c copy`) thành video của Cụm.
2. **Vi phẫu 1 Nhịp trong 1.5 Giây khi phát hiện lỗi P0/P1:**
   - Ghi biên bản theo cú pháp: `[Mã Nhịp: beat_06] · [Tại t_peak = 3.1s] · [Lỗi P0: Cắt dọc nhân vật phải khi zoom 1.26x] -> [Lệnh sửa: Bật viewport_isolation_mode = true]`.
   - Sửa đúng thông số của `beat_06` trong `beat_manifest.json`. Khi chạy lại Engine Bước 3, các nhịp không đổi được lấy thẳng từ `cache_beats/` (`0.0s`), Engine **chỉ render lại duy nhất nhịp vừa sửa mất ~1.5 giây**, ghép lại Cụm và chụp lại `verify_peak_zoom_<cluster_id>.png` để xác nhận **0 lỗi P0** trước khi sang Cụm kế tiếp.
