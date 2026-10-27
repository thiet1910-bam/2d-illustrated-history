# Thiết Kế Âm Thanh 3 Lớp (`Voice + Authentic Ziro Foley SFX + Auto-Ducked BGM`)

## Mục 1. Cấu Trúc Bàn Trộn Âm Thanh 3 Lớp Chuẩn Phổ Âm Ziro History (`3-Layer Audio Architecture`)

| Tầng Âm Thanh | Chức năng & Nguyên tắc hoạt động | Mức âm lượng chuẩn (`dB` / `dBFS`) | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **LỚP 1: Giọng Đọc Chính & Đối Thoại Skit (`Master Voice Track`)** | Là trục thời gian gốc (`Master Clock`). Nối trực tiếp các mẫu PCM `.wav` không suy hao, giữ nguyên tốc độ và cao độ tự nhiên. | **`0.0 dB` (`-16.0` đến `-18.5 dBFS` RMS)** | Chỉ ghép mỗi giọng đọc khô khốc mà bỏ trống Lớp 2 và Lớp 3 làm video bị đơn độc, thiếu cảm xúc. |
| **LỚP 2: Bộ Tiếng Động Gốc Của Ziro History (`ziro_authentic_sfx`)** | Tự động đồng bộ 8 file WAV gốc trích xuất từ Ziro History (`kho_rieng_2d_history_va_opus5_5/ziro_authentic_sfx/`) và chèn chính xác tại `t_sfx_global = beat.t0 + sfx.bt`. | **Gain trộn `-14.5 dB` $\rightarrow$ thực tế đạt `-28` đến `-35 dBFS` RMS** (Thấp hơn giọng đọc `13–18 dB`, êm dịu không chói tai) | Để SFX quá to (`-6 dB`) làm tiếng bíp/tiếng đập lấn át giọng thuyết minh hoặc dùng tiếng `beep` điện tử giả tạo. |
| **LỚP 3: Nhạc Nền Khí Sắc Tự Động Hạ Âm Mượt (`Auto-Ducked BGM Bed`)** | Chạy xuyên suốt Cụm theo tâm trạng (`Mood`). Tự động hạ sâu khi có giọng nói và nâng nhẹ ở khoảng nghỉ chuyển câu (làm mượt qua cửa sổ `350ms`). | **`-20.0 dB`** (khi đang đọc) $\leftrightarrow$ **`-12.5 dB`** (khi nghỉ `> 0.35s`) | Để nhạc nền quá to (`-8 dB`) gây ồn nền hoặc cắt nhạc đột ngột không có đường bao mượt (`envelope smoothing`). |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `cum_03_Skit_1`, giọng đọc đạt `-18.1 dBFS`, nhạc nền `bgm_satire_skit.wav` chạy nền êm ái ở `-20.0 dB`, và 27 điểm tiếng động gốc `ziro_authentic_sfx` nằm ở khoảng `-33.8 dBFS` đến `-44.6 dBFS` — nghe tự nhiên như tiếng giấy, tiếng bút chì, tiếng bước chân thật trong phòng thu Ziro.
- **❌ Ví dụ Sai (Bị cấm):** Để tiếng động SFX nổ chát chúa ngang ngửa âm lượng giọng người đọc hoặc bỏ trống hoàn toàn tiếng động khi đạo cụ bật lên.

---

## Mục 2. Từ Điển 8 Tiếng Động Gốc Ziro History (`ziro_authentic_sfx`) & Bảng Ánh Xạ Tự Động

| Tên File Gốc Trong Kho (`ziro_authentic_sfx/`) | Mã Gọi Tương Đương Trong JSON (`sfx_file`) | Nguồn Trích Xuất Chuẩn (`ZNYnU2NQ5w4`) & Âm Sắc Vật Lý | Khi Nào Sử Dụng Trên Sân Khấu |
| :--- | :--- | :--- | :--- |
| **`ziro_pop_soft.wav`** *(`-29.8 dBFS`)* | `pop_card.wav` hoặc `ziro_pop_soft.wav` | `00:25.15` — Tiếng bọt giấy nảy tròn, ấm và mềm khi nhân vật/câu thoại bật lên. | Khi hiện câu thoại trên đầu nhân vật (`skit_speech_captions`), bật thẻ ảnh hoặc nảy ngôi sao `✦`. |
| **`ziro_scroll_unroll.wav`** *(`-24.8 dBFS`)* | `whoosh_transition.wav` hoặc `ziro_scroll_unroll.wav` | `02:02.40` — Tiếng giấy da dê vuốt mở sột soạt kết hợp luồng gió nhẹ lướt qua. | Khi chuyển cảnh bàn bản đồ, mở bức mật thư, mở cuộn giấy Herodotus hoặc lia máy. |
| **`ziro_rubber_stamp.wav`** *(`-29.6 dBFS`)* | `stamp_slam.wav` hoặc `ziro_rubber_stamp.wav` | `02:49.00` — Tiếng đập mộc gỗ trầm ấm xuống mặt bàn giấy (không chói gắt). | Khi đóng dấu phán quyết (`< 10%` cảnh), chốt bảng kiểm hoặc thả thước đo chạm đỉnh `3.0m`. |
| **`ziro_icon_pop_rapid.wav`** *(`-34.7 dBFS`)* | `typewriter_tick.wav` hoặc `ziro_icon_pop_rapid.wav` | `02:35.30` — Tiếng gõ/tích nhanh, mảnh và giòn như đầu bút chì/bút lông chạm giấy. | Khi bút chì 2D vẽ đường đi (`live_pencil_line`), bút lông viết cuộn giấy (`live_quill_scroll`) hoặc đánh dấu `[✓]`. |
| **`ziro_spear_drop.wav`** *(`-34.5 dBFS`)* | `sword_clash.wav` hoặc `ziro_spear_drop.wav` | `05:06.10` — Tiếng vũ khí/cán giáo chạm sàn gỗ kèm âm vang kim loại ngắn trong Skit. | Khi quân lính hành quân, chỉ giáo, bốc lửa cháy thành Athens hoặc đổi tư thế tay đột ngột. |
| **`ziro_padlock_slam.wav`** *(`-26.9 dBFS`)* | `jail_bar_clang.wav` hoặc `ziro_padlock_slam.wav` | `01:36.20` — Tiếng ổ khóa sắt và song sắt sập xuống chắc nịch. | Khi sập song sắt nhà tù (`T03_Prison_Bars_Slam`), khóa biên giới hoặc cấm vận. |
| **`ziro_light_off_thud.wav`** *(`-31.1 dBFS`)* | `ziro_light_off_thud.wav` | `00:54.30` — Tiếng dập công tắc trầm chuyển sang vùng tối. | Khi chuyển sang cảnh tối (`PRISON_NIGHT`) hoặc bật đèn chiếu rạp phim. |
| **`ziro_poem_unroll.wav`** *(`-25.1 dBFS`)* | `ziro_poem_unroll.wav` | `05:24.20` — Tiếng mở trang sách/bài thơ cổ điển trong phòng học sử gia. | Khi mở sách cổ, chiếu tư liệu lịch sử hoặc chuyển đoạn kết Skit. |

---

## Mục 3. Quy Tắc Chọn Nhạc Nền Theo Tâm Trạng Cụm (`Cluster BGM Mood Selection`)

1. **`bgm_tense_history.wav` (Nhạc nền Trầm hùng / Nghịch lý lịch sử):** Dùng cho các Hồi phân tích địa chính trị, xung đột, đế chế, cấm vận (Hồi I, II, III...). Âm sắc trống trầm nhẹ + đàn dây nhịp 90 BPM, tự động hạ âm xuống `-20.0 dB` khi có giọng đọc.
2. **`bgm_satire_skit.wav` (Nhạc nền Châm biếm / Hài kịch Pizzicato):** Dùng riêng cho các Cụm `Skit #1 .. #4`. Âm sắc pizzicato tưng tửng nhịp nhàng, tạo không khí hài kịch châm biếm ngay từ giây đầu tiên bước vào Skit.
