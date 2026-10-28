# Ziro-History-Studio-v3 (Universal Handover Edition)

**Xưởng Sản Xuất Video Lịch Sử, Địa Chính Trị & Kinh Tế Hoạt Hình 2D Dài Tập (`10 – 35 Phút`, `1920x1080 @ 30fps`) — Khớp 100% DNA Ziro History & Tự Chủ Đa Chủ Đề Toàn Cầu**

`Ziro-History-Studio-v3` là một gói công cụ & Skill AI độc lập hoàn toàn (`100% Self-Contained`), kết hợp **Phân Cụm Thích Ứng Động (`90s–240s`) + Nhép Môi `30fps` Tự Động Theo Giọng Đọc + Bản Đồ Vệ Tinh Toàn Cầu Offline + Hậu Kiểm Thị Giác QA** với **Lõi Render HTML5 Canvas + Playwright Siêu Tốc**.

---

## 1. Năng Lực Cốt Lõi Của Hệ Thống

1. **Nhân Vật Thương Hiệu Dẫn Chuyện (`shared/ziro_kit/brand_host.js`)**:
   - **Giáo Sư / Nhà Sử Học Áo Hoodie Đỏ (`#D93829`)**, đầu tròn trắng viền mực đen dày `5px`, cổ liền thân, kính cận tròn, xuất hiện xuyên suốt `~40%` thời lượng trên phông xám lì `#CCCCCC`.
   - **Nhép môi tự động `30fps` (`mouth = 0..3`)** trích xuất trực tiếp từ biên độ sóng âm `voice.MP3`, chớp mắt tự nhiên và có 6 tư thế đạo cụ (gậy chỉ bảng, kính lúp, nhún vai, khoanh tay, giật mình đánh rơi gậy).
2. **Tiểu Phẩm Châm Biếm Skit Đa Thời Đại (`shared/ziro_kit/skit_rig.js`)**:
   - Hai nhân vật đứng đối diện trên bối cảnh 2D phẳng: **ai đang nói mới nhép môi + chữ thoại trên đầu sáng `100%`; người đứng nghe tự động ngậm miệng + câu thoại trước mờ xuống `38%` (`opacity = 0.38`)**.
   - Tích hợp sẵn **9 nhóm trang phục đa chủ đề** (`president_suit`, `diplomat`, `general_military`, `soldier_helmet`, `supreme_leader`, `scientist_coat`, `king_ancient`, `warrior_ancient`, `citizen_modern`) kèm hàm gắn miệng rời `drawActorMouth` phục vụ mọi quốc gia & giai đoạn lịch sử.
3. **100% Kinetic Typography — Xóa Sổ Hộp Phụ Đề Đáy & Thanh Tiêu Đề Đỉnh (`shared/ziro_kit/kinetic_type.js`)**:
   - Cấm tuyệt đối phụ đề karaoke dưới đáy hay thanh tin tức trên đỉnh.
   - Sử dụng **Chữ từ khóa gõ máy chữ `1–4 từ`** (`drawTypewriter`), **Đồng hồ số nhảy Odometer** (`drawOdometerCounter`), **Lưới biểu tượng** (`drawIconGrid`), **Danh sách `[✓]`** (`drawChecklist`) và **Cuộn giấy cổ chuyển Hồi động** (`drawMasterScroll`).
4. **Bản Đồ Vệ Tinh Toàn Cầu Offline & Săn Ảnh Tư Liệu Xác Minh (`shared/ziro_kit/maps.js` + `engine/fetch_wikimedia.py`)**:
   - Có sẵn bản đồ vệ tinh Trái Đất chuẩn kinh-vĩ độ của NASA (`shared/maps/world_satellite.jpg`), cho phép thu phóng Spotlight vào **bất kỳ quốc gia nào trên thế giới** (Mỹ, Triều Tiên, Nga, Trung Quốc, Việt Nam, Châu Âu, Trung Đông...) bằng tọa độ `(lat, lon)`.
   - Công cụ `fetch_wikimedia.py` hỗ trợ `--list` & `--pick` để duyệt chọn chính xác ảnh lịch sử thật và tự động gắn tiền tố mã cụm `c01_`, `c02_` giữ ngăn nắp cho tập dài 30 phút.
5. **Quy Trình Tiết Kiệm Tối Đa Token Cho Con Người (`0 Token` Khi Đóng Gói)**:
   - AI chỉ dựng cuốn chiếu từng cụm (`cum_XX.mp4`). Khi xong toàn tập, người dùng nhấp đúp **`GOP_VIDEO_VA_DON_RAC.bat`** để nối `Master.mp4` trong `~3 giây` (không nén lại, lệch `0.0ms`) và xóa sạch `.cache/` trước khi cất sang kho lưu trữ ngoài.

---

## 2. Cấu Trúc Thư Mục Bàn Giao Sạch (`4 Trụ Cột`)

```text
Ziro-History-Studio-v3/
├── KIEM_TRA_HE_THONG.bat                  # [1-Click] Kiểm tra & cài đặt môi trường cho máy mới nhận bàn giao
├── GOP_VIDEO_VA_DON_RAC.bat               # [1-Click] Gộp video Master 30 phút & dọn sạch .cache (0 tốn Token AI)
├── HUONG_DAN_VAN_HANH_30_PHUT.md          # Sổ tay hướng dẫn tiếng Việt từng bước cho người dùng mới
├── GEMINI.md                              # Luật tự động kích hoạt Skill khi mở thư mục trong Antigravity IDE
├── .agent/skills/ziro-history-studio-v3/  # Bộ Skill chuẩn (SKILL.md, references/, templates/)
├── engine/                                # Trụ cột 1: Lõi xử lý tự động
│   ├── bins.py                            # Tự động dò tìm FFmpeg / FFprobe đa máy tính (không khóa cứng đường dẫn)
│   ├── preflight.py                       # Kiểm tra sức khỏe toàn hệ thống
│   ├── scan_clusters.py                   # Chia cụm thích ứng, cắt WAV 0.000s & trích khẩu hình nhép môi 30fps
│   ├── fetch_wikimedia.py                 # Duyệt chọn (--list/--pick) & tải ảnh lịch sử Wikimedia gắn mã cụm cXX_
│   ├── mix_audio.py                       # Hòa âm 3 lớp 48kHz Stereo (Voice + Auto-Duck BGM + Pan SFX)
│   ├── render.js                          # Render Full HD 30fps qua HTML5 Canvas + Playwright -> H.264 MP4
│   ├── build_qa_sheet.py                  # Xuất bảng ảnh hậu kiểm Peak-Zoom QA + đo độ lệch hình/tiếng
│   └── concat_master.py                   # Ghép nối Master MP4 toàn tập nguyên bản (-c copy)
├── shared/                                # Trụ cột 2: Kho tài sản dùng chung toàn kênh
│   ├── ziro_kit/                          # brand_host.js, skit_rig.js, kinetic_type.js, maps.js, helpers.js
│   ├── maps/                              # Bản đồ vệ tinh toàn cầu NASA (world_satellite.jpg)
│   ├── sfx/                               # 18 hiệu ứng âm thanh chuẩn 48kHz PCM WAV
│   └── bgm/                               # 2 nhạc nền bản quyền sạch 48kHz (Phân tích căng thẳng & Skit châm biếm)
├── episodes/                              # Trụ cột 3: Nơi tạo các tập phim mới (Bàn giao rỗng, sạch 100%)
│   └── HUONG_DAN_TAO_TAP_MOI.md
└── .cache/                                # Trụ cột 4: Bộ nhớ tạm tự sinh khi chạy (Tự động xóa khi xong tập)
```

---

## 3. Khởi Động Nhanh Cho Người Mới Nhận Bàn Giao

1. **Lần đầu tiên trên máy mới:** Nhấp đúp chuột chạy **`KIEM_TRA_HE_THONG.bat`** để hệ thống tự động kiểm tra `Node.js`, `Playwright`, `Python` và tự dò tìm `FFmpeg / FFprobe` trên máy của bạn.
2. **Đọc hướng dẫn thực chiến (2 phút):** Mở file **`HUONG_DAN_VAN_HANH_30_PHUT.md`** và làm theo 3 bước để sản xuất ngay tập phim 30 phút đầu tiên!
