# BIÊN BẢN NGHIỆM THU 8 CỔNG CHẤT LƯỢNG & KIỂM DUYỆT ĐỈNH ZOOM (`<CLUSTER_ID>`)

## 1. Thông Tin Xuất Bản Cụm Video
- **Mã Tập & Mã Cụm:** `[Điền episode_id / cluster_id]`
- **Đường dẫn Video xuất ra:** `3_output/<Ma_Tap>/1_video_cac_cum/<cluster_id>.mp4`
- **Đường dẫn Lưới ảnh Đỉnh Zoom (`Peak-Zoom Grid`):** `3_output/<Ma_Tap>/2_bang_kiem_duyet_qa/verify_peak_zoom_<cluster_id>.png`
- **Thời lượng Giọng đọc gốc (`.wav`):** `[Điền giây]`
- **Thời lượng Video xuất ra (`.mp4`):** `[Điền giây]`
- **Độ lệch đồng bộ (`Sync Drift`):** `[Điền giây, yêu cầu <= 0.020s]`

---

## 2. Bảng Chấm Điểm 8 Cổng Kiểm Duyệt Cứng (`8 Hard Gates`)

| Mã Cổng | Hạng Mục Kiểm Toán | Ngưỡng Yêu Cầu | Số Liệu Thực Tế | Kết Quả (`PASS / FAIL`) |
| :--- | :--- | :--- | :--- | :---: |
| **Gate 1** | Khớp âm thanh tuyệt đối (`Audio-Visual Sync`) | `Drift <= 0.020s` | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 2** | Toàn vẹn chữ tiêu đề tại Đỉnh Zoom (`Pass 2 HUD`) | `y_center >= 110px`, 0 nét chữ bị cắt | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 3** | Toàn vẹn nhân vật & thẻ bài (`No Edge Clipping`) | 0 nhân vật bị xẻ dọc, 0 thẻ bị cụt mép | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 4** | Giải phẫu khớp cổ cắm sâu (`Neck Seamless`) | `neck_insert = 28..42px`, 0 khe hở | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 5** | Đầy đủ 3 lớp âm thanh (`Voice + SFX + BGM`) | Có đủ SFX tại `bt` và BGM tự hạ âm | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 6** | Tỷ lệ nền sáng ấm Ziro (`Daylight Ratio`) | `>= 80%` cảnh nền sáng ấm | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 7** | Đa dạng bố cục (`Anti-Repetition`) | Không lặp cùng mẫu quá 2 nhịp liên tiếp | `[Điền số liệu]` | `[PASS/FAIL]` |
| **Gate 8** | Mật độ chuyển động (`No Dead Stretch`) | Không đứng hình quá `2.5s` | `[Điền số liệu]` | `[PASS/FAIL]` |

---

## 3. Nhật Ký Khám Nghiệm Từng Nhịp Tại Đỉnh Phóng To (`Peak-Zoom Frame Audit`)

| Mã Nhịp (`beat_id`) | Thời Điểm Chụp Đỉnh Zoom (`t_peak`) | Hệ Số Zoom & Pan (`zoom, pan_x`) | Trạng Thái Chữ HUD & Nhân Vật | Phân Loại Lỗi (`NONE / P0 / P1`) | Phương Án Xử Lý |
| :---: | :---: | :---: | :--- | :---: | :--- |
| `[beat_01]` | `[VD: 3.20s]` | `[zoom=1.18, pan_x=0]` | `[Nguyên vẹn 100%]` | `NONE` | `Không cần sửa` |
