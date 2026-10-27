# Luật Đồng Bộ `voice.MP3` Nguyên Khối & Phân Cụm Thích Ứng Động (`Dynamic Adaptive Clustering`)

## Mục 1. Bộ 3 File Đầu Vào & Khóa Cứng `voice.MP3` `0.000s` (`On-Demand Audio Slicing`)

| Thành phần Đầu vào / Xử lý (Nếu xử lý X) | Quy tắc kỹ thuật & Toán học bắt buộc (Thì áp dụng Y) | Sai số cho phép | Lỗi sai cần tránh |
| :--- | :--- | :--- | :--- |
| **Bộ 3 File Đầu Vào Chuẩn (`1_input/<Ma_Tap>/`)** | Gồm: (1) `kich_ban_loi_dan.txt` (100% lời dẫn khớp Audio), (2) `kich_ban_chia_hoi.txt` (chia `HỒI / Chương`, `Phân đoạn`, `Skit`, ghi chú `(Hình ảnh: ...)`), (3) `voice.MP3` (1 file âm thanh nguyên khối). | Khớp câu chữ `100%` giữa 2 bản kịch bản | Bắt người dùng phải tự cắt tay file `voice.MP3` hoặc tự tách kịch bản bên ngoài. |
| **Quét Cấu Trúc Động Không Giới Hạn Số Hồi (`Dynamic Regex Parser`)** | Script Bước 1 dùng biểu thức chính quy (`act_regex`, `segment_regex`, `skit_regex`, `visual_note_regex` trong `config/ziro_brand_presets.json`) tự động nhận diện mọi số lượng Hồi (`3, 5, 7, 10 Hồi`) và Phân đoạn (`1.1..N.M`) mà không khóa cứng con số cố định. | Bảo toàn `100%` ghi chú `(Hình ảnh: ...)` vào từng Phân đoạn | Viết code khóa cứng 7 Hồi / 21 Phân đoạn khiến kịch bản khác bị lỗi. |
| **Cắt `voice.MP3` Cuốn Chiếu Theo Cụm Đang Dựng (`On-Demand Audio Slicing`)** | Khi bắt đầu dựng Cụm nào (`cluster_id`), script dùng `faster_whisper` (`word_timestamps=True`) + dò điểm lặng (`Silence Valley`) bóc đúng đoạn âm thanh của Cụm đó từ `voice.MP3`, cắt ra `voice_cum.wav` và các câu lẻ `beats_wav/beat_01..N.wav` (`44.1kHz PCM`). | `0.000s` (`dur = nframes / 44100.0`) | Ước lượng thời lượng bằng đếm chữ gây trôi hình lệch tiếng. |
| **Khóa Cứng Thời Lượng Hình = Tiếng (`Sample-Locked Sync`)** | Thời lượng mỗi nhịp câu bằng chính xác `nframes / 44100.0` của `beat_i.wav`. Tổng thời lượng video Cụm bằng đúng tổng các `beat_i.wav`. | `abs(video_dur - audio_dur) < 0.02s` | Thêm khoảng nghỉ giả vào hình ảnh nhưng không có trong âm thanh. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Từ bộ 3 file trong `1_input/EP01_Iran/`, Bước 1 tự động phát hiện 7 Hồi (21 Phân đoạn `1.1 -> 7.3` + `4 Skit`), gom nhóm thông minh thành các Cụm tối ưu và cắt gói âm thanh của Cụm đầu tiên (`beat_01..12.wav`) khớp `0.000s`.
- **❌ Ví dụ Sai (Bị cấm):** Chạy 1 lèo cả 29 phút 24 giây trong một lần gọi duy nhất hoặc cắt giọng đọc bằng cách chia đều số chữ.

---

## Mục 2. Thuật Toán Phân Cụm Thích Ứng Động (`90s – 240s`) & Vòng Lặp Cuốn Chiếu Có Bộ Nhớ Đệm (`Beat Cache`)

| Tình huống Thời lượng Hồi / Phân đoạn (Nếu gặp X) | Quyết định Gom hoặc Tách Cụm (`Dynamic Adaptive Clustering`) (Thì áp dụng Y) | Số Nhịp / Thời Lượng Chuẩn | Cơ chế Chuyển tiếp & Sửa lỗi (`Beat Cache`) |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1: Hồi ngắn/vừa ($\le 240\text{s}$ ~ 4 phút, $\le 22$ câu) và KHÔNG chứa Skit** | **Gom trọn cả Hồi thành 1 Cụm Render (`1 Act = 1 Cluster`, VD: `cum_01_Hoi_I`)**, nhưng bên trong JSON vẫn giữ nguyên nhãn `segment_id` (`1.1, 1.2, 1.3`) và `author_visual_note` của từng Phân đoạn để đổi bối cảnh/nhạc nền. | `10 – 22 nhịp` (`90s – 240s`) | Dựng 1 mạch cả Hồi cho liền mạch cảm xúc; lưu từng nhịp vào `cache_beats/beat_XX_<hash>.mp4`. |
| **Trường hợp 2: Hồi có chứa Tiểu phẩm `Skit` xen giữa** | **Tách riêng Tiểu phẩm `Skit` thành 1 Cụm độc lập (`cum_Skit_1`)** tại đúng ranh giới `(Chuyển nhịp Skit #...)` để đổi sang nhánh `types/02_khuon_mau_canh_skit_cham_biem.md` và nhạc nền hài châm biếm. | `8 – 16 nhịp` (`60s – 150s`) | Tách bạch 100% tông màu và âm nhạc giữa Chính luận và Hài kịch. |
| **Trường hợp 3: Hồi quá dài ($> 240\text{s}$ hoặc $> 22$ câu)** | **Tự động chia đôi Hồi tại ranh giới `Phân đoạn X.Y`** (ví dụ `Phân đoạn 2.1 + 2.2` thành `cum_Hoi_II_P1`, `Phân đoạn 2.3 + 2.4` thành `cum_Hoi_II_P2`) sao cho mỗi Cụm luôn nằm trong khung vàng `90s – 240s`. | Không vượt quá `22 nhịp / cụm` | Chống tràn bộ nhớ ngữ cảnh của AI và giữ tốc độ render mỗi cụm `< 25 giây`. |
| **Trường hợp 4: Phân đoạn đơn lẻ quá dài ($> 180\text{s}$)** | Giữ độc lập **1 Phân đoạn = 1 Cụm riêng (`cum_PhanDoan_X_Y`)**. Sau khi các Cụm đạt `DONE_PASS`, nối tức thì thành Hồi và Master 30p bằng `ffmpeg -f concat -c copy`. | Ghép nối `0.000s` không nén lại | Khi sửa lỗi 1 nhịp trong Cụm, chỉ render lại đúng 1 file `beat_XX_<hash>.mp4` mất `1.5 giây`. |

- **✅ Ví dụ Đúng (Đạt chuẩn):** Ở `Hồi I` (dài `~3 phút`, gồm 3 phân đoạn `1.1, 1.2, 1.3`, 11–12 câu lời dẫn, không có Skit), thuật toán gom thành 1 Cụm `cum_01_Hoi_I` (giữ đủ 3 `author_visual_note` của `1.1, 1.2, 1.3`). Nếu `beat_06` bị lỗi P0, chỉ sửa `beat_06` trong JSON, render lại đúng `beat_06_<hash>.mp4` trong `1.5s` và nối lại `cum_01_Hoi_I.mp4`.
- **❌ Ví dụ Sai (Bị cấm):** Tách vụn mọi phân đoạn 30 giây thành hàng chục lần dừng duyệt gây đứt mạch câu chuyện, hoặc mỗi lần sửa 1 câu lại phải render lại từ đầu cả 12 câu mất hàng phút.
