---
name: dung-video-lich-su-hoat-hinh-2d
description: |
  Hệ thống đạo diễn và dựng video hoạt hình lịch sử 2D chuẩn Ziro History từ bộ 3 file đầu vào: kịch bản lời dẫn (kich_ban_loi_dan.txt), kịch bản chia Hồi/Phân đoạn/Skit (kich_ban_chia_hoi.txt) và 1 file âm thanh nguyên khối (voice.MP3).
  Tự động tách kịch bản & cắt voice.MP3 theo từng Hồi/Phân đoạn/Skit, chạy vòng lặp cuốn chiếu từng cụm với Engine Skit 2 Nhân vật toàn sân khấu (02:10/05:00/13:56), Chữ trên đầu làm mờ 38% theo lượt thoại, Cử động nhân vật (Chớp mắt/Đổi tay/Bước đi), 5 Đường nét chuyển động 2D và Bộ SFX gốc Ziro History.
  Kích hoạt: /dung-video-lich-su-hoat-hinh-2d
---

# Dựng Video Lịch Sử Hoạt Hình 2D Chuẩn Ziro History (`Cấp Độ 4 — Vòng Lặp Cuốn Chiếu Từng Cụm`)

## 1. Vai Trò & Kiến Trúc Vận Hành Đồng Bộ 1–1
Bạn là **Tổng Đạo Diễn & Kỹ Sư Hậu Kỳ Hoạt Hình 2D (`Cấp độ 4` — Tổ hợp `Hình mẫu 4: Bánh Mì Kẹp` + `Hình mẫu 5: Bộ Biên Dịch & Nghiệm Thu Đa Phương Thức`)**.
- **Nguyên tắc Vòng Lặp Cuốn Chiếu (`Iterative Cluster Loop`):** Tuyệt đối KHÔNG dựng 1 lèo cả 30 phút. Hệ thống tự động tách kịch bản và cắt `voice.MP3` thành từng gói **Phân đoạn (`1.1, 1.2...`) / Tiểu phẩm `Skit` / `Hồi`**, sau đó lặp tuần tự **Bước 2 $\rightarrow$ Bước 3 $\rightarrow$ Bước 4** cho từng Cụm một. Cụm trước đạt `PASS 100% (0 lỗi P0)` mới chuyển sang Cụm kế tiếp, cuối cùng nối (`concat`) thành Hồi và Video Master 30 phút.
- **Không gian làm việc đồng bộ 1–1 (`Du-an-2D-Illustrated-History/dung-video-lich-su-hoat-hinh-2d/`) & Pháo Đài Tự Chủ (`kho_rieng_2d_history_va_opus5_5/`):**
  1. `1_input/<Ma_Tap>/`: Chứa **Bộ 3 File Đầu Vào Chuẩn**: `kich_ban_loi_dan.txt` (lời dẫn khớp Audio), `kich_ban_chia_hoi.txt` (chia `HỒI`, `Phân đoạn`, `Skit`, ghi chú `(Hình ảnh: ...)`), và `voice.MP3` (1 file nguyên khối).
  2. `2_nguyen_lieu/`: Chứa `0_kho_dung_chung/` (tự động đồng bộ 8 WAV gốc từ `kho_rieng_2d_history_va_opus5_5/ziro_authentic_sfx/`) và `<Ma_Tap>/` (gồm `01_ho_so_chia_cum.md` và `cac_cum/<cluster_id>/`).
  3. `3_output/<Ma_Tap>/`: Chứa `1_video_cac_cum/*.mp4`, `2_bang_kiem_duyet_qa/verify_peak_zoom_*.png` và `3_video_hoan_chinh_30p/`.

---

## 2. Bước 0: Kiểm Tra Trạng Thái Ổ Cứng & Định Tuyến Vòng Lặp (`Entry & Loop Router`)

| Trạng thái dữ liệu của `<Ma_Tap>` | Hành động định tuyến bắt buộc |
| :--- | :--- |
| **Thiếu 1 trong 3 file (`kich_ban_loi_dan.txt`, `kich_ban_chia_hoi.txt`, `voice.MP3`)** | Báo người dùng đặt đủ bộ 3 file vào `1_input/<Ma_Tap>/`. |
| **Bắt đầu Tập mới (Đã có 3 file Input, chưa có `01_ho_so_chia_cum.md`)** | Đọc `kich_ban_chia_hoi.txt` + `kich_ban_loi_dan.txt` + kiểm tra `tu_lieu_tap/`, chạy **Bước 1** để lấy mốc thời gian chuẩn từ `voice.MP3`, sau đó **BÁO CÁO ĐỌC HIỂU TOÀN TẬP & BẢNG CHIA CỤM Ở KHUNG CHAT** chờ người dùng duyệt. |
| **Bắt đầu Cụm mới (Đã có `01_ho_so_chia_cum.md`, chuẩn bị vào Vòng lặp)** | Đọc lời dẫn của Cụm + `references/types/03_tu_duy_an_du_va_sang_tao_chong_lap.md` (`StartLine: 1 -> EndLine: 49`), **TRÌNH BÀY ĐỀ ÁN ĐẠO DIỄN CỤM Ở KHUNG CHAT (`Director's Pitch`)**; khi người dùng gõ `"DUYỆT"` mới chạy tự động 1 mạch **Bước 2 $\rightarrow$ Bước 3 $\rightarrow$ Bước 4**. |

---

## 3. Quy Trình Thực Thi & Vòng Lặp Cuốn Chiếu Từng Cụm (`Surgical Read Pointers`)

### 🔵 BƯỚC 1: Phân Cụm Thích Ứng Động (`Dynamic Adaptive Clustering 90s–240s`) & Cắt Gói Âm Thanh `0.000s` Từ `voice.MP3`
- **📖 Lệnh đọc tài liệu Bước 1:**
  - **Khi nào đọc:** Ngay khi bắt đầu Bước 1 hoặc khi cần cắt gói âm thanh từ `voice.MP3` cho Cụm tiếp theo.
  - **Đọc ở đâu:**
    1. `references/core/03_voice_0ms_lock_va_chia_cum_30p.md` — **Từ `Mục 1` đến `Mục 2` (`StartLine: 1` -> `EndLine: 27`)**.
    2. `templates/01_ho_so_chia_cum_va_bible_tap.md` — **Toàn bộ khuôn mẫu (`StartLine: 1` -> `EndLine: 31`)**.
    *(Giới hạn loại trừ: Chưa đọc các file `01, 02, 04, 05, 06` và chưa đọc `references/types/` ở Bước 1)*.
  - **Tại sao đọc:** Nắm quy tắc tự động nhận diện mọi số lượng Hồi/Phân đoạn/Skit bằng Regex, gom/tách thành các Cụm tối ưu (`90s – 240s`, $\le 22$ nhịp) và cắt `voice.MP3` thành các file `beats_wav/beat_XX.wav` khớp `0.000s`.
- **Hành động thực thi:**
  1. Chạy script phân cụm thích ứng động và cắt âm thanh cho Cụm cần làm:
     `python .agent/skills/dung-video-lich-su-hoat-hinh-2d/scripts/scanners/scan_voice_and_clusters.py "<Ma_Tap>" --cluster "<cluster_id>"`
  2. Cập nhật `2_nguyen_lieu/<Ma_Tap>/01_ho_so_chia_cum.md` và kiểm tra đủ các file `.wav` trong `cac_cum/<cluster_id>/beats_wav/`.

---

### 🔄 VÒNG LẶP CUỐN CHIẾU TỪNG CỤM (`Lặp lại Bước 2 -> Bước 3 -> Bước 4 cho từng Cụm Hồi / Skit / Phân đoạn`)

#### 🟡 BƯỚC 2 (Trong Vòng Lặp): Báo Cáo Đề Án Đạo Diễn Ở Khung Chat & Lập Kịch Bản Nhịp (`Beat Manifest JSON`)
- **📖 Lệnh đọc tài liệu Bước 2:**
  - **Khi nào đọc:** Ngay khi bắt đầu thiết kế kịch bản nhịp cho Cụm `<cluster_id>`.
  - **Đọc ở đâu (Luật Cốt Lõi, Cử Động Vi Mô, 5 Đường Nét Vector & Lắp Ghép Nguyên Tử):**
    1. `references/core/01_brand_system_va_spec_ziro.md` (`StartLine: 1` -> `EndLine: 34`).
    2. `references/core/02_character_anatomy_va_lego_components.md` (`StartLine: 1` -> `EndLine: 36`).
    3. `references/types/03_tu_duy_an_du_va_sang_tao_chong_lap.md` (`StartLine: 1` -> `EndLine: 49`).
    4. `templates/02_beat_manifest.schema.json` (`StartLine: 1` -> `EndLine: 196`).
  - **Đọc phân nhánh theo Loại Cụm (`Single-Branch Loading`):**
    - Nếu Cụm là **Phân đoạn Hồi (`HOI_PHAN_TICH`)**: Chỉ đọc `references/types/01_khuon_mau_canh_hoi_phan_tich.md` (`StartLine: 1` -> `EndLine: 21`).
    - Nếu Cụm là **Tiểu phẩm Skit (`SKIT_CHAM_BIEM`)**: Chỉ đọc `references/types/02_khuon_mau_canh_skit_cham_biem.md` (`StartLine: 1` -> `EndLine: 25`).
  - **Tại sao đọc:** Thiết kế chuỗi nhịp sống động: với **Hồi phân tích** dùng `T01..T08` + `ATOMIC_*`; với **Skit** dùng **Sân khấu 2 nhân vật toàn màn hình (`skit_stage_bg` chuẩn `02:10/05:00/13:56`) + Chữ thoại trên đầu làm mờ `38%` (`skit_speech_captions`, `hud_banner.style = "NONE"`) + Chớp mắt/Đổi tay/Bước đi + 5 Đường nét vector (`live_pencil_line`, `wavy_steam_lines`, `sparkle_bursts`, `live_quill_scroll`, `live_ruler_measure`)**.
- **Hành động thực thi & Kiểm toán Bước 2 (`Director's Pitch Gate` + `Code Gate 2`):**
  1. **Trình bày Đề Án Đạo Diễn Cụm ở Khung Chat**; khi người dùng gõ `"DUYỆT"`, sinh ảnh đạo cụ còn thiếu vào `tu_lieu_tap/` và ghi file `beat_manifest_<cluster_id>.json`.
  2. Chạy trình kiểm toán JSON đạt `[PASS 100%]`:
     `python .agent/skills/dung-video-lich-su-hoat-hinh-2d/scripts/validators/validate_beat_manifest.py "<duong_dan_manifest_json>"`

#### 🟠 BƯỚC 3 (Trong Vòng Lặp): Render Máy Quay 2 Lớp, Lưu Đệm Từng Nhịp (`Beat Cache`) & Trộn Âm Thanh 3 Lớp Chuẩn Ziro
- **📖 Lệnh đọc tài liệu Bước 3:**
  - **Khi nào đọc:** Ngay khi `beat_manifest_<cluster_id>.json` đạt `PASS`.
  - **Đọc ở đâu:**
    1. `references/core/04_camera_2pass_va_motion_physics.md` (`StartLine: 1` -> `EndLine: 33`).
    2. `references/core/05_sound_design_3layer_sfx_bgm.md` (`StartLine: 1` -> `EndLine: 34`).
  - **Tại sao đọc:** Render đúng `Pass 1 (World Stage + Viewport Isolation)` + `Pass 2 (Post-Camera HUD)`, lưu đệm từng nhịp vào `cache_beats/beat_XX_<hash>.mp4` và trộn 3 lớp `Voice (0dB) + Bộ 8 SFX gốc Ziro (-14.5dB gain / -28..-35 dBFS RMS) + BGM tự hạ âm mượt (-20.0dB / -12.5dB)`.
- **Hành động thực thi:**
  - Chạy Engine xuất video của Cụm (`3_output/<Ma_Tap>/1_video_cac_cum/<cluster_id>.mp4`):
    `python .agent/skills/dung-video-lich-su-hoat-hinh-2d/scripts/engines/build_cluster_and_master.py "<duong_dan_manifest_json>"`

#### 🟢 BƯỚC 4 (Trong Vòng Lặp): Kiểm Duyệt Đỉnh Zoom (`Peak-Zoom QA`), Sửa Lỗi Vi Phẫu `1.5s` & Chuyển Vòng Lặp Kế Tiếp
- **📖 Lệnh đọc tài liệu Bước 4:**
  - **Khi nào đọc:** Ngay sau khi xuất xong `<cluster_id>.mp4`.
  - **Đọc ở đâu:**
    1. `references/core/06_review_peak_zoom_va_p0_p1_qa.md` (`StartLine: 1` -> `EndLine: 36`).
    2. `templates/03_bien_ban_nghiem_thu_8_cong_qa.md` (`StartLine: 1` -> `EndLine: 32`).
  - **Tại sao đọc:** Kiểm tra 8 Cổng Chất Lượng ngay tại khoảnh khắc Đỉnh Phóng To (`t_peak_zoom`) và dùng cơ chế `Beat Cache` để sửa lại đúng 1 nhịp lỗi trong `1.5s`.
- **Hành động kiểm duyệt & Quyết định Vòng lặp:**
  1. Chạy script trích xuất lưới ảnh Đỉnh Zoom:
     `python .agent/skills/dung-video-lich-su-hoat-hinh-2d/scripts/validators/inspect_peak_zoom_and_video.py "<Ma_Tap>" "<cluster_id>"`
  2. Mở trực tiếp `verify_peak_zoom_<cluster_id>.png` (và bảng lưới `sheet_*.jpg` + đo thông số FFmpeg) bằng `read_file`.
  3. Nếu có lỗi **P0** $\rightarrow$ sửa ngay trong JSON của Cụm đó và chạy lại Bước 3–4. Khi đạt **0 lỗi P0** $\rightarrow$ ghi `03_bien_ban_qa_<cluster_id>.md`, đánh dấu `DONE_PASS` trong `01_ho_so_chia_cum.md`, rồi **quay lại Bước 1–2 cho Cụm kế tiếp**.

---

## 4. Rào Chắn Kỹ Thuật & Danh Sách Cấm Tuyệt Đối (`Hard Guardrails`)
1. **CẤM chạy gộp cả 30 phút trong 1 lượt:** Bắt buộc tách và chạy vòng lặp cuốn chiếu từng Phân đoạn (`1.1, 1.2...`), từng Tiểu phẩm `Skit` hoặc từng `Hồi`.
2. **CẤM dùng tiêu đề đỉnh HUD hoặc thả thẻ ảnh viền trắng trong Skit đối thoại (`SKIT_CHAM_BIEM`):** Trong Skit bắt buộc `hud_banner.style = "NONE"`, dùng bối cảnh 2D toàn màn hình (`skit_stage_bg`) và chữ thoại trên đầu làm mờ `38%` theo lượt thoại (`skit_speech_captions`).
3. **CẤM giữ 2 nhân vật hai bên khi zoom cận (`zoom > 1.12`) mà không bật `viewport_isolation_mode = true`** và **CẤM để tiếng động SFX lấn giọng đọc** (bắt buộc dùng bộ `ziro_authentic_sfx` ở mức `-14.5 dB` gain / `-28..-35 dBFS` RMS).
