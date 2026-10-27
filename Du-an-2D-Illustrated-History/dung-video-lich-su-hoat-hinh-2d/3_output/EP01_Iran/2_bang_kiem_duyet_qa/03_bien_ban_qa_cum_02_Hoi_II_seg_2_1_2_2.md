# BIÊN BẢN KIỂM ĐỊNH CHẤT LƯỢNG VIDEO (GATE 5 QA REPORT) — `cum_02_Hoi_II_seg_2_1_2_2`

- **Mã Tập**: `EP01_Iran`
- **Mã Cụm (Cluster ID)**: `cum_02_Hoi_II_seg_2_1_2_2`
- **File Video Thành Phẩm**: `3_output/EP01_Iran/1_video_cac_cum/cum_02_Hoi_II_seg_2_1_2_2.mp4`
- **Bảng Kiểm Duyệt Peak-Zoom**: `3_output/EP01_Iran/2_bang_kiem_duyet_qa/verify_peak_zoom_cum_02_Hoi_II_seg_2_1_2_2.png`
- **Kết Quả Tổng Thể**: **PASS 100% (8/8 HARD GATES)**

---

## 1. BẢNG ĐỐI CHIẾU 8 CHỐT CHẶN KỸ THUẬT & MỸ THUẬT (8 HARD GATES)

| Gate | Tiêu Chí Kiểm Định (Hard Gate) | Thông Số Thực Tế Đo Đạc | Kết Quả |
| :--- | :--- | :--- | :---: |
| **Gate 1** | Độ phân giải & Tốc độ khung hình chuẩn Broadcast | `1920x1080 @ 29.95fps` (`138.4 MB`) | **PASS** |
| **Gate 2** | Khớp tuyệt đối thời lượng Voice gốc & Mật độ Beat (4-7s/beat) | Video `107.5s` vs Voice `107.511792s` (Lệch `0.01s`, `11 beats`) | **PASS** |
| **Gate 3** | Kiểm định tại Đỉnh Zoom (`Peak-Zoom Inspection`) toàn bộ 12 Beats | Đã trích xuất đủ `11/11` frames tại `t_peak_zoom`, không đè chữ/cắt đầu | **PASS** |
| **Gate 4** | Khớp cổ Seamless Choker Collar (`#111111` 8px) & Tỷ lệ nhân vật Ziro | Không đứt cổ khi nghiêng đầu; nhân vật 70% khung hình, viền đen 5px | **PASS** |
| **Gate 5** | Nền xám `#CCCCCC` không kẻ vạch sàn `y=855` & Text Frameless (`>=90%`) | 0 đường kẻ ngang vô nghĩa; 10/12 Beat dùng Frameless Color-Pop, chỉ 1 Beat đóng dấu Stamp | **PASS** |
| **Gate 6** | 2-Pass Camera Rendering & Nhép miệng 30fps theo biên độ âm thanh RMS | Camera pan/zoom mượt trên 2500x1406; miệng đóng mở `open/smile/o_shape/closed` khớp giọng | **PASS** |
| **Gate 7** | Hòa âm 3 lớp (Voice-over + BGM Ducking -18dB + Đa điểm SFX) | Stream Audio: `aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 198 kb/s (default)` | **PASS** |
| **Gate 8** | Bộ nhớ đệm `Hash-Based Beat-Level MP4 Cache` (`cache_beats/`) | Đã lưu `11` file `beat_XX_<hash>.mp4` sẵn sàng re-render 1.5s | **PASS** |

---

## 2. NHẬT KÝ TRÍCH XUẤT PEAK-ZOOM THEO TỪNG BEAT

| STT | Beat ID | Khoảng Thời Gian | Thời Điểm Peak-Zoom (`t_peak_zoom`) | Chế Độ Nền | Chuyển Động Camera | File Frame Trích Xuất |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| 01 | `beat_01` | `0.0s - 5.0s` | **`4.54s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.08x)` | `peak_01_beat_01.png` |
| 02 | `beat_02` | `5.0s - 12.6s` | **`11.82s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.12x)` | `peak_02_beat_02.png` |
| 03 | `beat_03` | `12.6s - 27.9s` | **`26.34s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.14x)` | `peak_03_beat_03.png` |
| 04 | `beat_04` | `27.9s - 31.3s` | **`30.99s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.08x->1.00x)` | `peak_04_beat_04.png` |
| 05 | `beat_05` | `31.3s - 52.5s` | **`50.34s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.11x)` | `peak_05_beat_05.png` |
| 06 | `beat_06` | `52.5s - 63.7s` | **`62.61s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.15x)` | `peak_06_beat_06.png` |
| 07 | `beat_07` | `63.7s - 67.7s` | **`67.27s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.08x->1.00x)` | `peak_07_beat_07.png` |
| 08 | `beat_08` | `67.7s - 82.3s` | **`80.85s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.14x)` | `peak_08_beat_08.png` |
| 09 | `beat_09` | `82.3s - 90.3s` | **`89.48s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.13x)` | `peak_09_beat_09.png` |
| 10 | `beat_10` | `90.3s - 95.7s` | **`95.13s`** | `SAND_EMPIRE` | `ISO_FOCUS (1.00x->1.12x)` | `peak_10_beat_10.png` |
| 11 | `beat_11` | `95.7s - 107.5s` | **`106.33s`** | `DAYLIGHT_WARM` | `ISO_FOCUS (1.00x->1.15x)` | `peak_11_beat_11.png` |
