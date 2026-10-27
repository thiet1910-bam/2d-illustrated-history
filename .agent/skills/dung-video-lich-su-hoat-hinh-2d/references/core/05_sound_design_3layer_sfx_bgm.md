# Thiết Kế Âm Thanh 3 Lớp (`Voice + Foley SFX + Auto-Ducked BGM`)

## Mục 1. Cấu Trúc Bàn Trộn Âm Thanh 3 Lớp Bắt Buộc (`3-Layer Audio Architecture`)

| Tầng Âm Thanh | Chức năng & Nguyên tắc hoạt động | Mức âm lượng chuẩn (`dB`) | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **LỚP 1: Giọng Đọc Chính & Đối Thoại Skit (`Master Voice Track`)** | Là trục thời gian gốc (`Master Clock`). Nối trực tiếp các mẫu PCM `.wav` không suy hao, giữ nguyên tốc độ và cao độ tự nhiên. | **`0.0 dB` (Đỉnh chuẩn)** | Chỉ ghép mỗi giọng đọc khô khốc mà bỏ trống Lớp 2 và Lớp 3 làm video bị đơn độc, thiếu cảm xúc. |
| **LỚP 2: Tiếng Động Vật Lý Theo Nhịp (`Event-Driven Foley SFX`)** | Chèn chính xác vào thời điểm đạo cụ/hành động xuất hiện trên màn hình theo công thức: `t_sfx_global = beat.t0 + sub_trigger.bt`. | **`-6.0 dB` đến `-8.0 dB`** (Rõ nét nhưng không lấn chữ) | Chèn tiếng động ngẫu nhiên không khớp lúc thẻ bài bật lên hoặc tiếng nổ quá to át mất giọng người đọc. |
| **LỚP 3: Nhạc Nền Khí Sắc Tự Động Hạ Âm (`Auto-Ducked BGM Bed`)** | Chạy xuyên suốt Cụm theo đúng tâm trạng (`Mood`). Tự động hạ thấp khi có giọng nói và nâng nhẹ lên ở các khoảng nghỉ chuyển câu. | **`-16.0 dB`** (khi đang đọc) $\leftrightarrow$ **`-9.0 dB`** (khi nghỉ `> 0.35s`) | Để nhạc nền đều đều ở mức to (`-5 dB`) suốt video gây ồn ào, tranh chấp với giọng thuyết minh. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `beat_03` (*Tống vào ngục*), giọng đọc ở mức `0dB`, nhạc nền hồi hộp chạy nền ở `-16dB`, và đúng giây `bt = 1.85s` khi song sắt nhà tù sập xuống từ đỉnh màn hình thì tiếng kim loại va chạm `jail_slam.wav` vang lên ở `-6dB`.
- **❌ Ví dụ Sai (Bị cấm):** Cảnh song sắt sập xuống, con dấu đập vào mặt giấy và 3 thẻ bài bật lên diễn ra trong sự im lặng tuyệt đối ngoài giọng đọc.

---

## Mục 2. Từ Điển Ánh Xạ Hành Động Thị Giác $\rightarrow$ Tiếng Động Foley (`Visual-to-SFX Cue Mapping`)

| Sự kiện thị giác trên màn hình (Nếu xuất hiện X) | Mã file SFX bắt buộc gắn vào `sfx_events` (Thì gọi Y) | Độ dài & Đặc tính âm học | Mốc kích hoạt (`Trigger Offset`) |
| :--- | :--- | :--- | :--- |
| **Thẻ bài, huy hiệu, nhân vật bật nảy lên (`Card / Badge Pop`)** | `pop_card.wav` | `0.14s` — Tiếng bọt/nảy ấm, tần số `280Hz -> 620Hz`. | Đúng tại `bt + 0.02s` khi `scale` bắt đầu vọt lên. |
| **Máy quay lia nhanh hoặc chuyển cảnh chia đôi (`Fast Pan / Split`)** | `whoosh_transition.wav` | `0.26s` — Tiếng gió lướt mượt qua không trung. | Tại `bt = 0.00s` (mở nhịp mới) hoặc lúc bắt đầu lia máy. |
| **Con dấu đỏ đập xuống (`Rubber Stamp Slam`)** | `stamp_slam.wav` | `0.22s` — Tiếng đập trầm nặng (`95Hz`) kèm tiếng giấy đanh. | Đúng khoảnh khắc con dấu chạm mặt thẻ (`bt + 0.12s`). |
| **Song sắt nhà tù sập xuống / Khóa xích (`Prison Bars Slam`)** | `jail_bar_clang.wav` | `0.38s` — Tiếng thanh thép va đập vang vọng kim loại. | Đúng lúc đáy song sắt chạm đất (`bt + 0.18s`). |
| **Gõ chữ năm tháng / Sử gia viết cuộn giấy (`Typewriter / Quill`)** | `typewriter_tick.wav` | `0.08s x N` — Chuỗi tiếng gõ cơ học hoặc sột soạt bút lông. | Chạy rải đều trong `0.6s` đầu khi dòng chữ/cuộn giấy hiện ra. |
| **Vũ khí, mũi tên, chiến trận Skit (`Sword / Arrow Impact`)** | `sword_clash.wav` | `0.30s` — Tiếng kiếm chạm hoặc mũi tên cắm phập. | Tại đúng `bt` khi nhân vật vung vũ khí hoặc mũi tên chạm đích. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Một nhịp có 3 thẻ bài bật ra lần lượt ở `bt = [2.4s, 3.5s, 4.7s]` và 1 con dấu đập ở `bt = 5.4s` sẽ tự động sinh mảng 4 sự kiện âm thanh: `3 x pop_card.wav` + `1 x stamp_slam.wav`.
- **❌ Ví dụ Sai (Bị cấm):** Dùng duy nhất 1 tiếng `beep` điện tử chói tai cho mọi chuyển động trong video lịch sử.

---

## Mục 3. Quy Tắc Chọn Nhạc Nền Theo Tâm Trạng Cụm (`Cluster BGM Mood Selection`)

1. **`bgm_tense_history.wav` (Nhạc nền Trầm hùng / Nghịch lý lịch sử):** Dùng cho các Hồi phân tích địa chính trị, xung đột, đế chế, cấm vận (Hồi I, II, III...). Âm sắc trống trầm nhẹ + đàn dây nhịp 72 BPM.
2. **`bgm_satire_skit.wav` (Nhạc nền Châm biếm / Hài kịch Pizzicato):** Dùng riêng cho các Cụm `Skit #1 .. #4`. Âm sắc pizzicato tưng tửng nhịp 108 BPM, tạo không khí châm biếm ngay từ giây đầu tiên bước vào Skit.
