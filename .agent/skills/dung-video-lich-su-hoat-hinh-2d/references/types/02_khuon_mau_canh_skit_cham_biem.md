# Kho Khuôn Mẫu Cảnh Tiểu Phẩm Châm Biếm (`Skit Satire & Comedy Templates`)

## Mục 1. Bảng 5 Khuôn Mẫu Bố Cục Dành Riêng Cho Các Tiểu Phẩm `Skit #1 .. #4` (`S01` $\rightarrow$ `S05`)

| Mã Khuôn Mẫu Skit | Khi nào sử dụng (Nếu kịch bản Skit diễn cảnh X) | Cấu trúc Sân khấu & Diễn xuất Hài kịch (Thì dàn dựng Y) | Cấu hình Camera Cô Lập & SFX Skit |
| :--- | :--- | :--- | :--- |
| **`S01_General_Tent_Dialogue`** | Hai nhân vật lịch sử đối thoại châm biếm trong lều chỉ huy, cung điện hoặc phòng họp (VD: Tướng Ba Tư & Vua Xerxes). | Nửa đầu (`0 -> bt_switch`): Góc toàn (`zoom = 1.02, pan_x = 0`) thấy cả Nhân vật A (`x = 560`) và Nhân vật B (`x = 1360`). Nửa sau khi 1 người nói câu chốt: Bật **`viewport_isolation_mode = True`**, cắt cận (`zoom = 1.24`) chỉ lấy người đang nói kèm bong bóng thoại ngắn (`<= 5 từ`). | Nhạc nền: `bgm_satire_skit.wav`; SFX: `whoosh_transition.wav` khi đổi góc + `pop_card.wav` khi hiện bong bóng thoại. |
| **`S02_Hollywood_Myth_vs_Reality`** | Châm biếm sự phóng đại của phim ảnh/truyền thuyết so với thực tế lịch sử phũ phàng (VD: Phim *300* vs Thực tế Thermopylae). | Dựng khung máy quay phim Hollywood hoặc màn chiếu bóng; nhân vật bị vẽ lố (cao 3 mét, đeo đầy khuyên, cơ bắp bóng nhẫy dầu trẻ em `BABY OIL`) kèm mũi tên chỉ dẫn hài hước. | `zoom: 1.00 -> 1.18` vào chi tiết gây cười (chai dầu trẻ em / khuyên mũi); SFX: `pop_card.wav` + `stamp_slam.wav`. |
| **`S03_Biased_Historian_Desk`** | Bóc trần việc sử gia đối phương (VD: Herodotus Hy Lạp) ngồi chép sử thiên vị, tô hồng phe mình và bôi nhọ phe địch. | Sử gia mặc áo choàng ngồi bàn gỗ (`x = 620`), mắt `smug` liếc xéo, tay cầm bút lông gà viết lên cuộn giấy khổng lồ bên phải (`x = 1320`) với những con số bị gạch sửa lố bịch (`10,000 -> 1,000,0000`). | `zoom: 1.04 -> 1.16` vào cuộn giấy đang viết; SFX: chuỗi `typewriter_tick.wav` + `stamp_slam.wav` (`PHÓNG ĐẠI`). |
| **`S04_Field_Reporter_Gag`** | Nhân vật dẫn chuyện Ziro (áo Hoodie đỏ) cầm micro đứng giữa chiến trường cổ đại phỏng vấn lính/vua như phóng viên truyền hình. | Nhân vật Hoodie đỏ đứng ở `x = 580` chìa micro có logo Ziro về phía nhân vật cổ đại ở `x = 1280`; thanh băng rôn tin tức nóng (`BREAKING NEWS — 480 TCN`) đặt tại `Pass 2 HUD` (`y = 920px`). | Khóa `pan_x = 0, zoom = 1.04`; SFX: `pop_card.wav` + `whoosh_transition.wav`. |
| **`S05_Absurd_Visual_Gag`** | Câu thoại buông lời mỉa mai hoặc chơi chữ nghĩa đen (VD: *"Bôi dầu trẻ em lên cơ bụng 6 múi"*, *"Đội quân bất tử nhưng vẫn chết"*). | Phóng đại đạo cụ hiện đại đặt lệch thời đại ngay trong tay nhân vật cổ đại (chai `BABY OIL` khổng lồ lấp lánh ngôi sao, bảng điểm điện tử, hoặc hóa đơn tính tiền). | Cú đấm máy quay (`Punch-in zoom: 1.00 -> 1.22` trong `0.25s`) vào đạo cụ gây cười; SFX: `pop_card.wav` + `sword_clash.wav`. |

---

## Mục 2. Luật Diễn Xuất & Chuyển Cảnh Đặc Thù Trong Skit Châm Biếm

- **✅ Ví dụ Đúng (Đạt chuẩn):** Trong `Skit #1: Thermopylae`, khi Tướng Ba Tư và Vua Xerxes nói chuyện (`S01_General_Tent_Dialogue`), lúc máy quay zoom cận `1.25x` vào Tướng Ba Tư đang há hốc mồm (`shocked`), chế độ `viewport_isolation_mode = True` tự động ẩn Vua Xerxes ở rìa phải, giúp khung hình cận cảnh sạch sẽ 100%, không bị dính nửa mặt Vua Xerxes ở mép màn hình.
- **❌ Ví dụ Sai (Bị cấm):** Giữ nhịp cắt chậm rãi và nhạc nền bi tráng của Hồi phân tích bên trong đoạn Skit hài hước, hoặc để 2 nhân vật đối thoại bị cắt dọc nửa người khi máy quay lia qua lại.
