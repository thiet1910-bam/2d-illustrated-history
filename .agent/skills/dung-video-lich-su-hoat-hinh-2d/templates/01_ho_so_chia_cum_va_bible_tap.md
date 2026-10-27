# HỒ SƠ PHÂN CỤM THÍCH ỨNG ĐỘNG & DANH MỤC TƯ LIỆU TẬP PHIM (`<MA_TAP>`)

## 1. Thông Số Tổng Quan Bộ 3 File Đầu Vào (`1_input/<Ma_Tap>/`) & Kho Tư Liệu Tập
- **Mã tập phim:** `[Điền mã tập, VD: EP01_Iran]`
- **File kịch bản lời dẫn (khớp 100% Audio):** `1_input/<Ma_Tap>/kich_ban_loi_dan.txt`
- **File kịch bản cấu trúc (chia Hồi / Phân đoạn / Skit / Ghi chú hình ảnh):** `1_input/<Ma_Tap>/kich_ban_chia_hoi.txt`
- **File âm thanh gốc nguyên khối:** `1_input/<Ma_Tap>/voice.MP3`
- **Tổng thời lượng Audio gốc (`float64`):** `[Điền tổng số giây / phút, VD: 1764.020s (29m 24.02s)]`
- **Tổng số Hồi / Phân đoạn / Tiểu phẩm Skit phát hiện tự động:** `[VD: 7 Hồi, 21 Phân đoạn (1.1 -> 7.3), 4 Skit]`
- **Tổng số Cụm Thích Ứng Động (`Dynamic Adaptive Clusters`, `90s – 240s/cụm`):** `[Điền tổng số cụm sau khi gom/tách thông minh]`
- **Kho tài sản thương hiệu & âm thanh dùng chung toàn kênh:** `2_nguyen_lieu/0_kho_dung_chung/brand_ui_assets/` & `2_nguyen_lieu/0_kho_dung_chung/audio_sfx_bgm/`
- **Kho tư liệu hình ảnh & bản đồ riêng của Tập (chia theo Cụm + STT + Mốc giây `{STT}_{beat_id}_{t0}s-{t1}s_{slug}.jpg`):** `2_nguyen_lieu/<Ma_Tap>/tu_lieu_tap/<cluster_id>/`

---

## 2. Bảng Theo Dõi Tiến Độ Vòng Lặp Cuốn Chiếu Từng Cụm (`Dynamic Cluster Loop Tracker`)

| Thứ Tự | Mã Cụm (`cluster_id`) | Thuộc Hồi (`act_id`) | Các Phân Đoạn Gộp Trong Cụm (`segments`) | Loại (`HOI / SKIT`) | Số Nhịp (`beats`) | Mốc Audio (`t0 -> t1`) | Thời Lượng (`s`) | Trạng Thái (`PENDING / SLICED / RENDERED / DONE_PASS`) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `01` | `cum_01_Hoi_I` | `HỒI I` | `1.1, 1.2, 1.3` | `HOI_PHAN_TICH` | `[12]` | `[0.00 -> ...]` | `[...]` | `[PENDING]` |
| `02` | `cum_02_Hoi_II_P1` | `HỒI II` | `2.1, 2.2` | `HOI_PHAN_TICH` | `[...]` | `[... -> ...]` | `[...]` | `[PENDING]` |
| `03` | `cum_03_Skit_1` | `HỒI II` | `Skit #1 (2.2)` | `SKIT_CHAM_BIEM` | `[...]` | `[... -> ...]` | `[...]` | `[PENDING]` |

---

## 3. Danh Mục Ghi Chú Hình Ảnh Kịch Bản & File Tư Liệu Theo Cụm (`Episode Visual & Asset Bible`)

| Mã Phân Đoạn / Skit | Thuộc Cụm (`cluster_id`) | Ghi Chú Hình Ảnh Của Tác Giả Trích Xuất Tự Động (`author_visual_note`) | Các File Tư Liệu Đánh STT + Mốc Giây Trong `tu_lieu_tap/<cluster_id>/` |
| :---: | :--- | :--- | :--- |
| `1.1` | `cum_01_Hoi_I` | `[Tự động trích xuất từ kich_ban_chia_hoi.txt]` | `[VD: 01_beat02_0007s-0018s_tehran_1970_shops.jpg, ...]` |
| `1.2` | `cum_01_Hoi_I` | `[Tự động trích xuất từ kich_ban_chia_hoi.txt]` | `[VD: 08_beat06_0037s-0049s_act1_youth_vs_clerics.jpg, ...]` |
