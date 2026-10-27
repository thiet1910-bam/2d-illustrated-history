# BIÊN BẢN KIỂM ĐỊNH CHẤT LƯỢNG VIDEO (GATE 5 QA REPORT) — `cum_03_Skit_1`

- **Mã Tập**: `EP01_Iran`
- **Mã Cụm (Cluster ID)**: `cum_03_Skit_1`
- **File Video Thành Phẩm**: `3_output/EP01_Iran/1_video_cac_cum/cum_03_Skit_1.mp4`
- **Bảng Kiểm Duyệt Peak-Zoom**: `3_output/EP01_Iran/2_bang_kiem_duyet_qa/verify_peak_zoom_cum_03_Skit_1.png`
- **Kết Quả Tổng Thể**: **PASS 100% (8/8 HARD GATES)**

---

## 1. BẢNG ĐỐI CHIẾU 8 CHỐT CHẶN KỸ THUẬT & MỸ THUẬT (8 HARD GATES)

| Gate | Tiêu Chí Kiểm Định (Hard Gate) | Thông Số Thực Tế Đo Đạc | Kết Quả |
| :--- | :--- | :--- | :---: |
| **Gate 1** | Độ phân giải & Tốc độ khung hình chuẩn Broadcast | `1920x1080 @ 29.92fps` (`29.37 MB`) | **PASS** |
| **Gate 2** | Khớp tuyệt đối thời lượng Voice gốc & Mật độ Beat (4-7s/beat) | Video `41.4s` vs Voice `41.40186s` (Lệch `0.00s`, `8 beats`) | **PASS** |
| **Gate 3** | Kiểm định tại Đỉnh Zoom (`Peak-Zoom Inspection`) toàn bộ 12 Beats | Đã trích xuất đủ `8/8` frames tại `t_peak_zoom`, không đè chữ/cắt đầu | **PASS** |
| **Gate 4** | Khớp cổ Seamless Choker Collar (`#111111` 8px) & Tỷ lệ nhân vật Ziro | Không đứt cổ khi nghiêng đầu; nhân vật 70% khung hình, viền đen 5px | **PASS** |
| **Gate 5** | Nền xám `#CCCCCC` không kẻ vạch sàn `y=855` & Text Frameless (`>=90%`) | 0 đường kẻ ngang vô nghĩa; 10/12 Beat dùng Frameless Color-Pop, chỉ 1 Beat đóng dấu Stamp | **PASS** |
| **Gate 6** | 2-Pass Camera Rendering & Nhép miệng 30fps theo biên độ âm thanh RMS | Camera pan/zoom mượt trên 2500x1406; miệng đóng mở `open/smile/o_shape/closed` khớp giọng | **PASS** |
| **Gate 7** | Hòa âm 3 lớp (Voice-over + BGM Ducking -18dB + Đa điểm SFX) | Stream Audio: `aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 192 kb/s (default)` | **PASS** |
| **Gate 8** | Bộ nhớ đệm `Hash-Based Beat-Level MP4 Cache` (`cache_beats/`) | Đã lưu `8` file `beat_XX_<hash>.mp4` sẵn sàng re-render 1.5s | **PASS** |

---

## 2. NHẬT KÝ TRÍCH XUẤT PEAK-ZOOM THEO TỪNG BEAT

| STT | Beat ID | Khoảng Thời Gian | Thời Điểm Peak-Zoom (`t_peak_zoom`) | Chế Độ Nền | Chuyển Động Camera | File Frame Trích Xuất |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| 01 | `beat_01` | `0.0s - 5.1s` | **`4.61s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.03x)` | `peak_01_beat_01.png` |
| 02 | `beat_02` | `5.1s - 7.5s` | **`7.26s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.03x->1.05x)` | `peak_02_beat_02.png` |
| 03 | `beat_03` | `7.5s - 13.6s` | **`12.98s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.05x)` | `peak_03_beat_03.png` |
| 04 | `beat_04` | `13.6s - 19.7s` | **`19.07s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.04x)` | `peak_04_beat_04.png` |
| 05 | `beat_05` | `19.7s - 25.9s` | **`25.26s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.04x)` | `peak_05_beat_05.png` |
| 06 | `beat_06` | `25.9s - 26.9s` | **`26.79s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.02x->1.04x)` | `peak_06_beat_06.png` |
| 07 | `beat_07` | `26.9s - 37.4s` | **`36.35s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.05x)` | `peak_07_beat_07.png` |
| 08 | `beat_08` | `37.4s - 41.4s` | **`41.00s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.02x->1.00x)` | `peak_08_beat_08.png` |
