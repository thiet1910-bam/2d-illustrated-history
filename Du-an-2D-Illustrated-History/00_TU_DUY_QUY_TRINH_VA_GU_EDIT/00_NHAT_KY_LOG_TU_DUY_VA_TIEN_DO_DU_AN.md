# NHẬT KÝ LOG THEO DÕI TƯ DUY, KIẾN TRÚC & TIẾN ĐỘ DỰ ÁN `2D-ILLUSTRATED-HISTORY`

> **Mục đích tài liệu:** Sổ cái theo dõi toàn bộ quá trình tiến hóa tư duy, các sai lầm thực tế đã vấp phải, quy chuẩn kỹ thuật bắt buộc và trạng thái đồng bộ của các tài liệu/Skill trong dự án `2D-Illustrated-History`.

---

## PHẦN 1: QUYẾT ĐỊNH DỌN DẸP & ĐỒNG BỘ HÓA HỒ SƠ TƯ DUY (`00_TU_DUY_QUY_TRINH_VA_GU_EDIT/`)

Qua rà soát toàn bộ 5 file trong thư mục `00_TU_DUY_QUY_TRINH_VA_GU_EDIT/`, đây là trạng thái xử lý để không bao giờ bị xung đột giữa tư duy cũ và tư duy mới:

| STT | Tên File | Phân loại (Cũ / Mới) | Hành động Đã Thực Thi | Nội dung Cốt lõi Đang Nắm Giữ |
| :-: | :--- | :---: | :--- | :--- |
| **0** | ~~`TU_DUY_QUY_TRINH_EDITOR_2D_ILLUSTRATED_HISTORY_V1.md`~~ | ❌ **TƯ DUY CŨ (Sơ đồ 6 bước rời rạc)** | **ĐÃ XÓA BỎ (`REMOVED`)** | Các quy tắc đúng (như cấm `PIL.ImageDraw`) đã được hợp nhất vào File `02`, `03`, `04`; xóa bỏ để tránh loạn với Kiến trúc 4 Giai đoạn (`GD1 -> GD4`). |
| **1** | [`01_PHAN_TICH_DOI_THU_ZIRO_HISTORY_35_PHUT.md`](01_PHAN_TICH_DOI_THU_ZIRO_HISTORY_35_PHUT.md) | ✅ **GIỮ LẠI & ĐÃ CẬP NHẬT MỚI** | **Đã bổ sung Mục 6** (`Luật Băm Nhịp Vi Mô 1.5s–2.2s`, `Luật Mật độ 4 Lớp`, `Luật Camera Liên tục`) | Giải phẫu 8 Thủ pháp cơ học + **6 Luật Chuyển Ngữ Kịch bản $\leftrightarrow$ Hình ảnh** + **Luật Băm Câu Dài thành chuỗi `Micro-Beats 1.8s`**. |
| **2** | [`02_GIAI_PHAP_VA_QUY_TRINH_SAN_XUAT_VIDEO_30_PHUT.md`](02_GIAI_PHAP_VA_QUY_TRINH_SAN_XUAT_VIDEO_30_PHUT.md) | ✅ **GIỮ LẠI & ĐÃ ĐỒNG BỘ 4 GĐ** | **Đã xóa sơ đồ 6 bước cũ, thay bằng Sơ đồ 4 Giai đoạn (`GD1 -> GD4`) & bổ sung Điểm nghẽn số 5** | Phân tích cái gì tự động được / không tự động được cho video 30 phút, giải pháp băm mệnh đề dài và tích hợp ảnh thật + AI Art. |
| **3** | [`03_DANH_GIA_SKILL_VA_KE_HOACH_KIEN_TRUC_4_GIAI_DOAN.md`](03_DANH_GIA_SKILL_VA_KE_HOACH_KIEN_TRUC_4_GIAI_DOAN.md) | ✅ **GIỮ LẠI & ĐÃ CẬP NHẬT MỚI** | **Đã bổ sung Phần 5 (`8 Lệnh Cấm Tuyệt Đối - Zero-Tolerance Anti-Patterns`) & Kiến trúc Tinh Gọn Không Vẽ Việc** | Bản thiết kế Kiến trúc Dây chuyền 4 Giai đoạn (`GD1 -> GD4`) chuẩn `playbook-skill-creator`, tích hợp `2-Pass Camera`, `0.000s Sync Lock` & `3-Layer Audio`. |
| **4** | [`04_PHE_BINH_5_PHUT_ZIRO_HISTORY_VA_DOI_CHIEU_KICH_BAN_IRAN.md`](04_PHE_BINH_5_PHUT_ZIRO_HISTORY_VA_DOI_CHIEU_KICH_BAN_IRAN.md) | ✅ **GIỮ LẠI & ĐÃ CẬP NHẬT MỚI** | **Đã ghi đầy đủ `8 Lỗi Cốt Tử`, `7 Quy chuẩn Gốc rễ` & Bài học thực chiến từ V1 + V2** | Nhật ký phê bình từng giây 5 phút đầu (`00:00 -> 05:05`) của `Ziro History`, bảng ánh xạ sang Kịch bản Iran và bài học kiểm điểm từ bản V1 & V2. |

---

## PHẦN 2: NHẬT KÝ LOG LỊCH SỬ THỬ NGHIỆM & BÀI HỌC XƯƠNG MÁU (`EXPERIMENT & FAILURE LOG`)

### 📌 Log #1 (`2026-10-26 21:15`) — Kiểm toán Skill Cũ & Xem 5 Phút Liên Tục Video Đối Thủ `Ziro History`
* **Hành động:**
  1. Chạy `validate_skill_structure.py` trên `.agent/skills/dung-video-lich-su-hoat-hinh-2d` $\rightarrow$ Phát hiện `Exit Code 1 [FAIL]` (8 lỗi cấu trúc, 3 file `references/` rỗng ruột chỉ 13–14 dòng, code bị hardcode cho 94s Bắc Triều Tiên).
  2. Cắt 5 phút đầu (`00:00 -> 05:05` = `305s`) của video `Ziro History` (`ZNYnU2NQ5w4`) thành 7 đoạn `.mp4` có âm thanh và xem trực tiếp qua `read_file` (`Lớp 1`) kết hợp đo `FFmpeg scdet + silencedetect` (`Lớp 2`).
* **Phát hiện cốt lõi:**
  - `50 điểm cắt cảnh lớn / 305s` (`ASL = 6.10s`), nhưng bên trong mỗi cảnh, **cứ mỗi `1.5s – 2.2s` lại có 1 biến đổi thị giác vi mô (`Micro-Beat`)** khớp đúng từ khóa giọng đọc.
  - Giải phẫu cơ chế **Skit Đối thoại 2 nhân vật** (*Hổ & Gấu ăn tỏi* ở `02:09` và *Tướng nhà Tùy đọc thơ* ở `04:55`): Ai nói thì chỉ miệng người đó đóng/mở + đổi tư thế tay + chữ thoại hiện ngay trên đầu người đó.

---

### 📌 Log #2 (`2026-10-26 22:18`) — [❌ THẤT BẠI] Bản Thử Nghiệm Prototype Iran V1 (`308s` Vẽ Bằng `PIL.ImageDraw`)
* **Hành động:** Chạy thử nghiệm 5 phút đầu kịch bản Iran (`Hồi I + Hồi II.1 & Skit #1`) bằng cách chia 31 nhịp (`Beat`) và dùng hàm vẽ hình học của Python (`PIL.ImageDraw`) tự vẽ bản đồ, tự vẽ thẻ ảnh lịch sử, tự vẽ nhân vật.
* **Đánh giá của Người dùng & Tự phê bình (Ray Dalio — Sự Minh bạch Tuyệt đối):**
  > *"Làm như shit. Của đối thủ chuyển cảnh nhanh, các chi tiết nhiều, của bạn thì rất ít chi tiết. Giữa kịch bản và hình ảnh không bằng đối thủ. Cơ bản là cảnh tĩnh, text không đặc sắc. Đấm vào mắt người xem."*
* **Giải phẫu 5 Lỗi Cốt Tử của Log #2 (Đã ghi vào Hồ sơ Cấm Vĩnh Viễn):**
  1. **Lỗi 1 — Tự vẽ hình học bằng code (`PIL.ImageDraw`) thay vì dùng Ảnh Tư Liệu Thật + Đồ Họa Minh Họa Chi Tiết (`Illustrated Vector / AI Art`):** Vẽ mấy hình tứ giác méo mó làm bản đồ, vẽ hình chữ nhật hồng/xanh làm phố Tehran 1970, vẽ hình bầu dục nâu làm Khối trụ Cyrus $\rightarrow$ Rẻ tiền, giả tạo, xúc phạm mắt người xem.
  2. **Lỗi 2 — Nhịp cắt quá chậm (`10s – 20s / 1 cảnh`) vì bê nguyên cả 1 câu văn dài thành 1 cảnh duy nhất:** `308 giây` chỉ có `31 nhịp` (`~10 giây/cảnh`, có cảnh đứng đơ `20.6 giây`), trong khi đối thủ băm câu dài thành các nhịp **`1.5s – 2.2s` (`Micro-Beats`)**.
  3. **Lỗi 3 — Thiếu bước "Chuyển Ngữ Đạo Diễn (`Clause-to-MicroAction`)" từ câu văn dài của kịch bản sang chuỗi hành động thị giác:** Khi kịch bản tiếng Việt viết câu ghép dài 35–45 chữ, không băm từng mệnh đề/danh từ thành chuỗi hành động liên hoàn mà bày sẵn 1 hình tĩnh từ đầu đến cuối câu.
  4. **Lỗi 4 — Text xấu và thừa thãi cái hộp phụ đề Karaoke ở đáy màn hình:** Chép nguyên câu văn dài vào hộp đen dưới đáy màn hình + lặp lại trên bong bóng thoại, làm mất sạch chất **Kinetic / Typewriter Callout Text (`1–4 từ khóa` gõ từng ký tự cạnh vật thể)** của `Ziro History`.
  5. **Lỗi 5 — Khung hình chết cứng (`Zero Camera Motion`):** Không có `Camera Push-in / Zoom-to-Target / Whip-Pan`, làm cảnh quay chết lâm sàng.

---

### 📌 Log #3 (`2026-10-27 07:40`) — [✅ ĐỘT PHÁ V2] Bản Dựng V2 Ziro Master (`Cụm A: 66.17s` & `Cụm B: 86.50s`) & Khắc Phục Triệt Để Lỗi "Giọng Nói Đi Chậm Hơn Hình Ảnh" (`0.000s Drift Lock`)
* **Hành động:**
  1. Thiết kế bộ máy `2x SSAA Vector Engine` (`render_v2_ziro_authentic_master.py`) thay thế chú lính đội nón lá bằng **Nhân vật Thương hiệu Độc quyền: Giáo Sư Du Hành (`mascot_time_traveler`)** + **10 nhân vật phụ (`Giáo sĩ`, `Sinh viên`, `Vua Cyrus`, `Hoàng đế Xerxes`, `Tướng Ba Tư`, `Chiến binh Sparta`, `Sử gia Hy Lạp`, `Xerxes 3m Hollywood`, `Quái vật đột biến`)**.
  2. Sửa triệt để lỗi giải phẫu **"Đầu và Thân không khớp nối"**: Mở rộng vai gấp `1.6x` chiều ngang đầu (`104px` vs `70px`) và hạ tâm đầu ngập sâu `14px` vào cổ áo chữ V (`head_cy = sh_y - head_ry + 14`), xóa bỏ hoàn toàn khe hở cổ trên cả 11 nhân vật.
  3. Chẩn đoán và xử lý dứt điểm phản hồi của người dùng: *"Tôi cảm giác như giọng nói đi chậm hơn hình ảnh hay sao ấy"*:
     - **Nguyên nhân 1 (`Inter-beat Drift`):** Trong `director_timeline_iran_prototype.json`, mảng khẩu hình `mouth_states_30fps` dài hơn file `.wav` gốc `~0.45s/câu` (do cộng thêm `pause_after`), nhưng hàm nối âm thanh cũ không chèn khoảng lặng này, làm Cụm A lệch `+3.90s` và Cụm B lệch `+4.63s`. $\rightarrow$ **Giải pháp khóa cứng:** Hàm `concat_wavs_locked()` đệm mẫu âm thanh chính xác tới từng sample theo `int(round(len(mouth_states_30fps) / 30.0 * sr))`, đưa độ lệch tổng về **`0.000s` tuyệt đối**.
     - **Nguyên nhân 2 (`Intra-beat Early Triggers`):** Các mốc bật hình `bt > ...` trong câu dài bị đặt sớm hơn thời điểm giọng đọc thực sự phát âm từ khóa đó `1.5s – 3.5s` (VD: ở `beat_08` tắt đèn lúc `3.1s` trong khi `5.15s` mới đọc *"lại tự nhốt mình vào bóng tối?"*; ở `beat_28` bật quái vật lúc `2.2s` trong khi `5.85s` mới đọc *"lũ quái vật đột biến gen"*). $\rightarrow$ **Giải pháp khóa cứng:** Quét các khoảng ngắt hơi (`>= 0.10s`) trong từng file `.wav` và khóa mọi mốc `bt` khớp chính xác phần trăm giây với từ khóa giọng đọc (`Syllable-Locked Visual Triggers`).

---

### 📌 Log #4 (`2026-10-27 08:06`) — Phản Biện Tinh Gọn ("Không Vẽ Thêm Việc") & Phát Hiện 3 Điểm Nghẽn Chất Lượng Hậu Kỳ ("Mất Chữ / Cắt Người Khi Camera Zoom", "Thiếu SFX/BGM Gây Đơn Độc", "Điểm Mù Kiểm Duyệt Ảnh Tĩnh")
* **1. Quyết định Tư duy Hệ thống — Cái gì CẦN và cái gì là "VẼ THÊM VIỆC" (Khi đối chiếu với `AI-Driven Documentary Factory`):**
  - ❌ **BỎ QUA (Vẽ thêm việc 100%):**
    1. Không làm bàn dựng Web `index.html` 2.500 dòng chạy GSAP (vì bên 2D đã có Engine Python `2x SSAA` vẽ trực tiếp nhân vật nhép miệng `30fps` và vật lý lò xo; làm thêm HTML là phải bảo trì 2 bộ code song song mà chất lượng hiển thị kém hơn).
    2. Không bóc vụn từng bộ phận (đầu, miệng, cánh tay, con dấu) ra hàng chục Track trong `CapCut PC` (vì kéo lệch 1 frame trong CapCut sẽ làm đầu lìa khỏi cổ, miệng lệch khỏi tiếng). Nếu cần đưa vào CapCut hậu kỳ thì chỉ xuất **từng câu `.mp4` sạch nét (`Smart Stems`)** hoặc file `.mp4` thành phẩm đã trộn đủ 3 lớp âm thanh.
    3. Không nhồi hàng nghìn dòng tọa độ rác (`x, y, w, h`) vào `storyboard.json`.
  - ✅ **GIỮ LẠI & LÀM TINH GỌN (Tối đa hóa chất lượng & độ minh bạch):**
    1. **Bảng Khớp Nối Đạo Diễn Minh Bạch (`Director Sync Sheet`):** Trước và sau khi render mỗi cụm, trình bày rõ bảng gồm 4 cột: *(1) Mốc thời gian & Lời thoại (`t0 -> t1`)*, *(2) Mốc giây `bt` bật hình/đóng dấu*, *(3) Trạng thái Camera & Lớp Hiển thị (`World Layer` vs `HUD Layer`)*, *(4) Điểm nổ Âm thanh (`SFX + BGM`)*. Người dùng nhìn bảng này là nắm 100% cách làm và khớp nối mà không cần qua phần mềm trung gian.
    2. **Kho Lưu Trữ Gu Edit 2D & Bộ Skill Chuẩn Hóa (`AGENTS.md` + `.agent/skills`):** Lưu giữ vĩnh viễn công thức V2 để không bao giờ bị trôi về bản V1 lỗi.
* **2. Giải phẫu 3 Lỗi Thực Tế Còn Tồn Đọng Trên Video V2 & Bổ Sung Thành 3 Luật Cưỡng Chế Mới (`Lỗi #6, #7, #8`):**
  - **Lỗi 6 — "Mất chữ tiêu đề, mất thẻ ảnh, cắt dọc nửa người nhân vật" khi Camera phóng to (`Zoom`) hoặc lia ngang (`Pan`):**
    - *Bằng chứng thực tế trên video V2:* Ở `beat_02` (`zoom=1.18, pan_x=-140`), hộp tiêu đề trên đỉnh bị cắt lẹm và thẻ `[CÀ PHÊ MỞ]` bật lên lúc `5.30s` bị cắt mất nửa bên phải; ở `beat_06` (`Split-Screen`) và `beat_22..27` (`Lều Ba Tư`), khi camera zoom vào bên Trái thì hộp tiêu đề ở giữa bị cắt mất một nửa chữ và nhân vật bên Phải bị cắt dọc nửa người dính ở mép ống kính!
    - *Nguyên nhân gốc rễ:* Vẽ tất cả (cả tiêu đề `HUD` lẫn 2 phe nhân vật) lên cùng 1 bức ảnh phẳng rồi mới gọi `apply_camera(img, zoom, pan_x, pan_y)` cắt lấy khung giữa.
    - **👉 Quy chuẩn Kỹ thuật Bắt buộc #5 (`Kiến trúc Vẽ 2 Lớp — 2-Pass Camera Rendering & Safe-Viewport Clamp`):**
      1. **Lớp 1 (`World Stage Pass` — Chịu tác động của `apply_camera`):** Chỉ vẽ bối cảnh, nhân vật và đạo cụ của sân khấu. Khi Camera zoom cận cảnh (`> 1.15x`) vào 1 bên trong cảnh chia đôi (`Split-Screen`) hoặc cảnh đối thoại 2 người (`Skit`), bắt buộc **cô lập vùng nhìn thấy (`Viewport Isolation`)** hoặc che sạch nửa bên kia để không bao giờ lộ "nửa cái xác người bị cắt dọc" ở mép màn hình! Mọi thẻ ảnh/chữ gắn với vật thể bật lên ở giây `bt` phải nằm 100% trong khung `Safe Viewport` của camera tại đúng giây `bt`.
      2. **Lớp 2 (`HUD & Title Overlay Pass` — Vẽ SAU KHI `apply_camera`):** Toàn bộ bảng tiêu đề trên đỉnh, nhãn năm/địa điểm cố định và các con dấu toàn màn hình (`Full-Screen Stamp`) bắt buộc phải được vẽ **SAU KHI** đã chạy `apply_camera()`. Nhờ đó, dù camera phóng to hay lia đi đâu, chữ tiêu đề luôn đứng im sắc nét 100% trong vùng an toàn, **0% bao giờ bị cắt mất chữ**.
  - **Lỗi 7 — "Cảnh đơn độc, thiếu cảm xúc" do chỉ có giọng đọc khô (`Raw Voice`), thiếu Nhạc nền (`BGM`) và Âm thanh vật lý (`SFX`):**
    - *Nguyên nhân gốc rễ:* Hàm `concat_wavs_locked()` mới chỉ ghép giọng đọc mà bỏ quên lớp `SFX` và `BGM`.
    - **👉 Quy chuẩn Kỹ thuật Bắt buộc #6 (`Bộ Trộn Âm Thanh 3 Lớp Khóa Mili-Giây — Auto-Synced 3-Layer Soundscape`):**
      1. **Lớp 1 (`Locked Voiceover`):** Giọng đọc khóa chuẩn `0.000s` drift.
      2. **Lớp 2 (`Event-Driven Foley SFX`):** Mọi hàm bật hình (`pop_scale`), đóng dấu (`stamp_scale`), lia máy (`whip_pan`), gõ chữ (`typewriter`), tắt đèn/sập song sắt (`jail_slam`), cháy nổ (`fire_crackle`), viết chữ (`quill_scribble`) bắt buộc tự động gắn sự kiện âm thanh tại đúng mili-giây `t0 + bt`!
      3. **Lớp 3 (`Dynamic Mood BGM + Auto-Ducking`):** Nhạc nền theo tâm trạng từng hồi (bí ẩn/điều tra cho Hồi 1, nhịp trống châm biếm/hành quân cho Skit), tự động hạ âm lượng (`-16dB`) khi có tiếng nói và dâng lên (`-9dB`) ở các khoảng nghỉ chuyển câu.
  - **Lỗi 8 — "Điểm mù Kiểm duyệt" khi chỉ chụp ảnh tĩnh ở cuối câu thoại (`End-of-Beat Static Grid`):**
    - *Nguyên nhân gốc rễ:* Cuối mỗi câu (`beat`), camera thường đã thu về toàn cảnh (`zoom = 1.0`), nên ảnh chụp ở giây cuối câu trông rất đầy đủ, che giấu mất việc ở giây giữa câu (`bt = 2.5s`) khi camera đang zoom `1.35x` thì chữ và người bị cắt cụt!
    - **👉 Quy chuẩn Kỹ thuật Bắt buộc #7 (`Kiểm Duyệt Video .MP4 Trực Tiếp + Ảnh Chụp Đúng Điểm Đang Zoom Cực Đại`):**
      1. Bắt buộc dùng công cụ `read_file` **mở xem trực tiếp chính file video `.mp4`** từ đầu đến cuối để kiểm tra chuyển động camera thực tế.
      2. Bảng ảnh nghiệm thu (`verify_grid`) bắt buộc phải chụp thêm các khung hình **đúng lúc Camera đang phóng to cực đại (`Peak-Zoom Frame`) và đang lia máy (`Mid-Pan Frame`)**, kết hợp hàm kiểm toán toán học báo lỗi ngay nếu bất kỳ hộp chữ hay nhân vật nào bị tràn ra ngoài khung `1920x1080`.

---

## PHẦN 3: KIẾN TRÚC CHUẨN HÓA ĐỂ LẬP KẾ HOẠCH TẠO SKILL EDIT (`TINH GỌN – KHÔNG VẼ VIỆC – CHẤT LƯỢNG TUYỆT ĐỐI`)

Dưới lăng kính **Tư duy Hệ thống (Russell Ackoff)** và **First Principles (Charlie Munger)**, toàn bộ quy trình sản xuất sẽ được đóng gói thành **Hệ thống 4 Giai đoạn Tinh Gọn (`GD1 -> GD4`)** tích hợp đầy đủ **8 Luật Cấm & 7 Quy Chuẩn Kỹ Thuật V2**:

| Giai đoạn Skill | Tên Skill Chuẩn Hóa | Nhiệm vụ Cốt lõi & Cơ chế Chốt Chặn Chất Lượng (Đã cập nhật từ Log #1 -> Log #4) |
| :--- | :--- | :--- |
| **`GD1`** | **`gd1-boc-tach-voice-va-khoa-nhip-0ms`**<br>*(Multi-Voice TTS/Alignment, `0.000s Drift Lock` & `Sub-Phrase Pause Scanner`)* | 1. Bóc tách hoặc sinh giọng đọc đa vai (`Dẫn chuyện`, `Tướng`, `Vua`...), đo khẩu hình `mouth_states_30fps` và **đệm khoảng lặng chính xác đến từng sample (`concat_wavs_locked`) đảm bảo độ lệch Audio-Video = `0.000s`**.<br>2. Quét tự động toàn bộ các điểm ngắt hơi (`>= 0.10s`) bên trong từng file `.wav` để xuất bảng mốc thời gian thực tế của từng vế câu (`Sub-phrase Timestamps`), ngăn chặn từ gốc lỗi "hình bật trước tiếng". |
| **`GD2`** | **`gd2-dao-dien-bang-khop-noi-va-phieu-nguyen-lieu`**<br>*(Director Sync Sheet, `1.8s Micro-Beats`, Safe-Camera Framing & SFX Cue Sheet)* | 1. Lập **Bảng Khớp Nối Đạo Diễn (`02a_bang_khop_noi_dao_dien.md`)** rõ ràng cho người dùng theo dõi: ứng với mỗi vế câu (`bt`), bật hình gì, ở lớp nào (`World Layer` hay `HUD Layer`), góc camera nào, và nổ tiếng `SFX` gì.<br>2. Cấm tuyệt đối phụ đề Karaoke đáy màn hình; chỉ dùng từ khóa `1–4 chữ` + con dấu (`Stamp Slam`).<br>3. Xuất **Phiếu Nguyên Liệu (`02b_asset_order.json`)**: Ảnh lịch sử thật, Bản đồ vệ tinh thật, Nhân vật/Đạo cụ 2D. |
| **`GD3`** | **`gd3-kho-nhan-vat-2d-va-nguyen-lieu-thuc`**<br>*(Brand Mascot Rig `1.6x Shoulder`, Real Archival Photos, Satellite Maps & SFX Bank)* | 1. Quản lý **Kho Nhân Vật 2D Chuẩn Giải Phẫu V2 (`Giáo Sư Du Hành` + các nhân vật lịch sử)**: Bắt buộc vai rộng `1.6x` đầu, đáy cằm ngập sâu `14px` vào cổ áo (`head_cy = sh_y - head_ry + 14`), 0% hở khớp cổ, vẽ nét vector khử răng cưa `2x SSAA`.<br>2. Tải **Ảnh Tư Liệu Lịch Sử Thật 100%** + **Bản Đồ Vệ Tinh Thật (`Esri World Imagery` + `GeoJSON`)** + Kho âm thanh vật lý **`SFX Bank` & `BGM Bed`**. |
| **`GD4`** | **`gd4-render-2lop-camera-3lop-audio-va-kiem-duyet-mp4`**<br>*(2-Pass Camera Engine, 3-Layer Audio Mixer & Direct `.MP4` + Peak-Zoom QA)* | 1. **Engine Vẽ 2 Lớp (`2-Pass Camera Rendering`):** Tách bạch `Pass 1 (World Stage có Zoom/Pan + Cô lập vùng nhìn không cắt nửa người)` và `Pass 2 (HUD/Title Overlay vẽ sau khi Zoom để 0% mất chữ)`.<br>2. **Bộ Trộn Âm Thanh 3 Lớp Tự Động (`Voice + Dynamic BGM + Event-Triggered SFX`)**: Tự động bắn tiếng `pop`, `stamp_slam`, `whoosh`, `metal_slam`, `scribble` khớp đúng mili-giây `t0 + bt` của chuyển động hình ảnh.<br>3. **Kiểm Duyệt Kép Trực Tiếp (`Peak-Zoom Grid + Direct read_file .mp4`):** Chụp ảnh kiểm tra ngay tại các đỉnh phóng to (`Peak-Zoom`) và mở xem trực tiếp file `.mp4` từ đầu đến cuối để đảm bảo `0 lỗi mất chữ/mất người` và `100% cảm xúc âm thanh`. |
