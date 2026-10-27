# BÁO CÁO GIẢI PHẪU CHI TIẾT VIDEO ĐỐI THỦ `ZIRO HISTORY` (`ZNYnU2NQ5w4` — 35 PHÚT 28 GIÂY)

> **Phương pháp kiểm chứng (Tuân thủ Cơ chế Đọc Video Kép trong [`GURU.md`](../../GURU.md)):**
> - **[👁️ Đã kiểm tra bằng mắt trên luồng Video `.MP4` liên tục]:** Đã cắt và nạp trực tiếp 4 luồng video `.mp4` (`clip_01_intro_00_30s.mp4`, `clip_02_intro_30_65s.mp4`, `clip_03_myth_tiger_bear_120_150s.mp4`, `clip_04_korean_war_map_940_970s.mp4`) vào `read_file` (`video/mp4`) để xem chuyển động từng giây (`00:00 -> 00:01 -> 00:02...`) kèm âm thanh như khán giả thật.
> - **[📊 Đã xác minh bằng số liệu (`FFmpeg scdet` & `yt-dlp`)]:** Đã đo tự động mật độ cắt cảnh, cấu trúc 13 chương và tốc độ xuất hiện hiệu ứng.

---

## 1. Thông Số Tổng Quan Của Video Đối Thủ (`[📊 Đã xác minh bằng số liệu]`)

- **Kênh:** `Ziro History` | **Tiêu đề:** *The Entire History of North Korea in 35 minutes* (`https://www.youtube.com/watch?v=ZNYnU2NQ5w4`)
- **Tổng thời lượng:** `2,128 giây` (`35 phút 28 giây`)
- **Cấu trúc phân chương:** Chia làm **13 Chương** (Mở đầu + 11 Chương nội dung trên Cuộn giấy cổ + Kết luận). Trung bình mỗi chương dài **`163 giây` (`~2 phút 43 giây`)**.
- **Mật độ chuyển cảnh (`FFmpeg scdet` đo trên 300 giây đầu):** `49 cú cắt cảnh / 300 giây` $\rightarrow$ Trung bình **`6.12 giây / 1 phân cảnh chính`**. Tuy nhiên, bên trong mỗi phân cảnh `6 giây`, cứ mỗi **`1.5s – 2.0s`** lại có một chi tiết nhỏ bật thêm lên (chữ gõ thêm, số nhảy, nhân vật chớp mắt hoặc giơ tay).

---

## 2. Phát Hiện Quan Trọng Khi Xem Luồng `.MP4` Liên Tục (Những Gì Ảnh Chụp Tĩnh Trước Đây Bỏ Sót)

Khi xem trực tiếp luồng video `.mp4` chạy từng giây (`[👁️ Đã kiểm tra bằng mắt]`), bản chất kỹ thuật thật sự của `Ziro History` lộ rõ: **Họ KHÔNG vẽ hoạt hình truyền thống từng khung hình (Frame-by-Frame Animation), mà dùng "Hoạt hình Cắt Giấy Lắp Ghép (`2D Cutout Puppet & Motion Graphics`)" với 8 Thủ Pháp Cơ Học lặp đi lặp lại suốt 35 phút**:

| STT | Thủ pháp của `Ziro History` | Bằng chứng cụ thể phát hiện khi xem luồng `.MP4` liên tục | Bản chất kỹ thuật (Họ làm thế nào?) |
| :-: | :--- | :--- | :--- |
| **1** | **Chữ gõ từng ký tự (`Typewriter Text`) & Bộ đếm số chạy (`Number Counter`)** | - Ở giây `00:14–00:17` (`clip_01`): Con số dân số chạy vọt từ `14,661,547` $\rightarrow$ `25,938,370` $\rightarrow$ `26,000,000 people`.<br>- Ở giây `00:04` & `00:07` (`clip_03`): Số nhánh tỏi đếm `1 -> 15 -> 20 cloves of garlic`, số ngày đếm `1 -> 47 -> 100 days`. | Không dùng phụ đề tĩnh! Mọi dòng chữ trên màn hình đều xuất hiện theo hiệu ứng gõ phím (`Typewriter`) khớp đúng lúc giọng đọc phát âm cụm từ đó. |
| **2** | **Nhân bản 1 Icon nhỏ thành hàng/lưới (`Icon Grid Repeater`)** | - Ở giây `00:04` (`clip_03`): Khi nói *"20 cloves of garlic"*, chỉ lấy **1 hình vẽ củ tỏi duy nhất** rồi nhân bản ra thành 2 hàng (mỗi hàng 10 củ) bật lên lần lượt (`pop-in`). | Tiết kiệm 90% công vẽ: Chỉ cần 1 icon PNG tách nền, dùng vòng lặp đặt tọa độ `(x + i*gap, y)` và cho bật lên lệch nhau `0.05s`. |
| **3** | **Nhân vật 2D là "Con rối giấy tĩnh" chỉ đổi Miệng, Mắt và 1 Cánh tay (`Paper-Doll State Swap`)** | - Ở `clip_03` (`00:09–00:29`, cảnh Hổ và Gấu trong hang): Thân con Hổ và con Gấu **đứng im 100% suốt 20 giây**! Khi con nào nói thì **chỉ mỗi cái miệng tròn mở/đóng**; đến giây `00:13` và `00:24` thì cánh tay con Gấu đổi từ ảnh `tay xuôi` sang ảnh `tay cầm củ tỏi`; đến giây `00:29` nói *"I'm out"* thì tắt hiển thị (`opacity = 0`) con Hổ! | **Không hề có chuyển động xương phức tạp!** Mỗi nhân vật chỉ là 1 ảnh thân tĩnh + 2 trạng thái miệng (`mở/đóng`) + 2 trạng thái mắt (`mở/nhắm` hoặc `nhíu mày`) + 2 trạng thái cánh tay. |
| **4** | **Di chuyển phương tiện bằng cách trượt ngang ảnh PNG (`Linear X-Slide`)** | - Ở `clip_04` (`00:17–00:19`): Cảnh Kim Nhật Thành đứng giữa 2 chiếc xe tăng T-34. Hai chiếc xe tăng chỉ là **1 tấm ảnh PNG tĩnh trượt ngang từ mép màn hình vào** (`x` dịch chuyển tịnh tiến, bánh xe thậm chí không cần quay!). | Dùng 1 ảnh PNG phương tiện tách nền + dịch chuyển tọa độ `X` (`Slide-in`). |
| **5** | **Hiệu ứng Bật/Tắt trạng thái ngay trên cùng 1 hình (`State Toggle`)** | - Ở `clip_01` (`00:28`): Khi nói *"died in 1994"*, đôi mắt của Kim Nhật Thành trong khung ảnh chuyển từ `mở` sang `nhắm (`- -`)`.<br>- Ở `clip_02` (`00:33`): Khi nói *"and the other half go dark?"*, toàn bộ các ô cửa sổ màu vàng bên nửa `NORTH` **tắt phụt sang màu đen**. | Cùng một bố cục hình học, chỉ đổi thuộc tính màu sắc (`fill = yellow -> black`) hoặc đổi lớp mắt đúng giây phát âm từ khóa. |
| **6** | **Bản đồ Vệ tinh Rọi Đèn (`Spotlight Vignette`) + Mặt nạ Chiếm đóng (`Moving Clip-Mask Frontline`)** | - Ở `clip_04` (`00:10–00:29`, Chiến tranh Triều Tiên 1950): Xung quanh bán đảo Triều Tiên được làm tối (`Spotlight`), chỉ làm sáng vùng bán đảo. Khi quân miền Bắc đánh xuống vòng vây Busan (`00:21 -> 00:28`), **vùng màu đỏ loang dần từ Bắc xuống Nam** theo đúng hình dáng đường bờ biển, chỉ chừa lại góc vuông nhỏ ở Busan! | Không phải vẽ lại hàng trăm bản đồ! Họ dùng **1 mặt nạ hình dáng bán đảo Triều Tiên (`Polygon Mask`)**, bên trong đặt 1 khối màu Đỏ có đường biên phía dưới trượt dần xuống (`y_frontline` tăng dần) để đè lên khối màu Xanh! |
| **7** | **Danh sách Dấu tích (`Checklist [✓]`) & Đóng dấu lên Ảnh lịch sử (`Archival Photo + Stamp`)** | - Ở `clip_04` (`00:01–00:09`): Hiện tiêu đề `"Kim's promises"` cùng 3 ô vuông tích xanh `[✓]` gõ chữ bên cạnh; ngay sau đó hiện ảnh đen trắng bo góc của `Joseph Stalin` + nhãn thời gian `[early 1950]` góc trên trái + con dấu xanh `[YES]` đóng nghiêng bên phải. | Công thức cố định khi giải thích nguyên nhân/lịch sử hiện đại: `Checklist` cho lý do + `Thẻ ảnh tư liệu thật đóng dấu` cho nhân vật có thật. |
| **8** | **Chú Lính Dẫn Chuyện Cố Định (`Host Stick-Soldier`) làm "Keo Dán" nối mọi cảnh** | - Xuất hiện ở góc trái (`x=220`), góc phải (`x=1700`) hoặc chính giữa (`x=960` khi chuyển ý lớn ở `00:18` của `clip_02`). | Giúp video có "linh hồn" xuyên suốt 35 phút mà không cần người thật lên hình. |

---

## 3. GIẢI PHẪU SONG HÀNH KỊCH BẢN $\leftrightarrow$ VIDEO (`SCRIPT-TO-VISUAL INTERLOCK` — THEO GURU #6 WALTER MURCH, EISENSTEIN & ACKOFF)

> **Phản biện tư duy phiến diện 1 chiều:**
> Nếu chỉ nhìn video mà không đọc kịch bản (`Transcript`), ta chỉ thấy *"trên màn hình có cửa hàng KIM & SONS, có cái tivi và song sắt, có con Hổ nói chuyện với con Gấu"*. Đó mới chỉ là **Phần xác (Thủ pháp đồ họa)**, hoàn toàn mù tịt về **Phần hồn (Tư duy Đạo diễn chuyển ngữ từ Chữ sang Hình)**.
> Khi đầu vào thực tế chỉ là `Kịch bản + Voice`, câu hỏi sống còn là: **"Đứng trước một câu chữ khô khan trong kịch bản, não bộ của Ziro History đã dịch câu chữ đó thành hình ảnh và nhịp dựng theo công thức nào?"**

Dưới đây là bảng đối chiếu **Từng câu kịch bản (`sample_intro_180s.en.vtt`) $\leftrightarrow$ Từng giây hình ảnh thực tế (`clip_01..04.mp4`)** (`[👁️ Đã kiểm tra bằng mắt]` & `[📊 Đã xác minh bằng số liệu]`) để bóc trần **6 Luật Chuyển Ngữ Từ Kịch Bản Sang Hình Ảnh (`6 Script-to-Visual Translation Rules`)**:

### 3.1. Bảng Đối Chiếu Thực Tế Từng Giây: Kịch Bản Nói Gì $\rightarrow$ Hình Ảnh Làm Gì?

| Mốc Giây | Nguyên văn Kịch bản (`Transcript` từng vế câu) | Hình ảnh & Nhịp khớp nối thực tế trên màn hình (`Video Stream`) | Luật Chuyển Ngữ Đạo Diễn (`Script -> Visual Rule`) |
| :-: | :--- | :--- | :--- |
| **`00:13 – 00:18`** | *"On the northern half of the Korean Peninsula..."*<br>*"...live **26 million people**..."* | - Vế 1 (`00:13`): Phóng vào bản đồ vệ tinh bán đảo Triều Tiên, tô đỏ nửa phía Bắc.<br>- Vế 2 (`00:15`, đúng từ **"26 million"**): Nền xám bật lên dòng chữ gõ phím + **Bộ đếm số chạy vọt** từ `14,661,547` $\rightarrow$ `26,000,000 people`. | **Luật 4 (Số liệu định lượng):** Hễ kịch bản có **Con số lớn** $\rightarrow$ Cấm hiện số tĩnh, bắt buộc biến thành **Bộ đếm số chạy vọt (`Number Counter`)** đúng giây phát âm con số. |
| **`00:22 – 00:29`** | *"...whose founder, **Kim Il-sung**, is still officially the country's eternal president, even though he **died in 1994**."* | - Vế 1 (`00:22`, từ **"Kim Il-sung"**): Khung ảnh nhân vật Kim Nhật Thành bật lên bên phải chú lính, mắt mở bình thường.<br>- Vế 2 (`00:28`, đúng từ **"died in 1994"**): **Trên cùng bức ảnh đó**, đôi mắt đổi sang nhắm tịt (`- -`) + hiện dòng chữ đỏ `died in 1994`. | **Luật 5 (Mệnh đề bước ngoặt / Đảo chiều):** Khi câu kịch bản có vế sau mang tính đảo ngược (`even though he died...`), **không cắt sang cảnh mới**, mà **đổi trạng thái (`State Toggle`) ngay trên bức hình đang mở** đúng mili-giây đọc từ khóa bước ngoặt! |
| **`00:30 – 00:35`** | *"Since then, his son and his grandson have run the place **like a family business**."* | - Kịch bản dùng cụm ẩn dụ trừu tượng *"like a family business"* (như một tiệm tạp hóa gia đình).<br>- Hình ảnh dịch **theo nghĩa đen hài hước**: Vẽ nguyên một **cửa tiệm mặt phố 2D** có biển hiệu đỏ **`KIM & SONS - since 1948`**, treo ảnh người cha trong tủ kính, còn ông con và ông cháu đứng bán hàng trước cửa! | **Luật 1 (Cụ thể hóa ẩn dụ trừu tượng thành hình ảnh nghĩa đen châm biếm — `Literal Visual Gag`):** Gặp câu so sánh/thành ngữ (`like a...`) $\rightarrow$ Vẽ luôn hình ảnh nghĩa đen của câu so sánh đó thành một bức biếm họa. |
| **`00:39 – 00:43`** | *"...where **watching a South Korean TV show** (1) / **can get you sent** (2) / **to a prison camp** (3)."* | **Bẻ 1 câu nhân quả thành 3 nhịp Trái $\rightarrow$ Giữa $\rightarrow$ Phải:**<br>- Nhịp 1 (`00:39`, *"watching a... TV show"*): Chiếc Tivi xanh bật lên ở bên trái.<br>- Nhịp 2 (`00:41`, *"can get you sent"*): Mũi tên cong trắng đầu đỏ bắn từ trái sang phải.<br>- Nhịp 3 (`00:42`, *"to a prison camp"*): Khung song sắt nhà tù + chữ đỏ `prison camp` đập xuống bên phải! | **Luật 2 (Bẻ câu Nhân - Quả thành Sơ đồ 3 Nhịp Trái $\rightarrow$ Mũi tên $\rightarrow$ Phải — `Intra-Sentence Cause-Effect Staging`):** Tuyệt đối không bày sẵn cả Tivi lẫn Nhà tù từ giây đầu! Phải giấu kết quả đi, đọc đến vế nào mới bật hình vế đó từ Trái qua Phải. |
| **`00:59 – 01:04`** | *"So how did **one half become one of the richest countries on Earth** (1), and **the other half go dark** (2)?"* | - Vế 1 (`00:59`): Chia đôi màn hình `SOUTH` (trái) và `NORTH` (phải). Cả 2 bên đều có các tòa nhà sáng đèn vàng.<br>- Vế 2 (`01:03`, đúng 2 từ **"go dark"**): Toàn bộ cửa sổ đèn vàng bên nửa `NORTH` **tắt phụt sang màu đen** + gõ chữ `...went dark`. | **Luật 5 (Đổi trạng thái Sáng/Tối theo từ khóa đối lập):** Dùng chính sự thay đổi ánh sáng trên hình để minh họa trực tiếp động từ *"go dark"*. |
| **`02:02 – 02:30`** | *"Eat only mugwort and **20 cloves of garlic**, stay inside a cave... for **100 days**... **Day three. I can't feel my tongue.** / Stay strong. Have another clove. / **Day five. I'm out.**"* | - Khi đọc *"20 cloves of garlic"*: Đếm số `1 -> 20` + nhân bản **20 icon củ tỏi** xếp thành 2 hàng.<br>- Khi kể chuyện Hổ & Gấu trong hang: Thay vì đọc văn xuôi lịch sử khô khan, kịch bản tự viết thành **1 vở kịch Sitcom hài 4 câu thoại** giữa Hổ và Gấu, kèm vạch đếm ngày (`III` $\rightarrow$ `IIII` $\rightarrow$ `<s>IIII</s>`) góc trên phải! | **Luật 6 (Chuyển đoạn kể chuyện khô khan thành Kịch Đối Thoại Sitcom ngắn — `Embedded Micro-Sitcom`):** Cứ mỗi 3–4 phút thông tin nặng, kịch bản tự cài 1 đoạn hội thoại hài hước 15–20 giây giữa 2 nhân vật để giải trí và giữ chân khán giả. |
| **`15:39 – 15:50`** | *"He promised **it would be quick** (1). **The southern people would rise up** (2). **It'd be over in weeks** (3). In early 1950, **Stalin finally said yes** (4)."* | - 3 câu liệt kê lời hứa (1, 2, 3) $\rightarrow$ Biến thành bảng **`Kim's promises`** với **3 dòng tích xanh `[✓]`** gõ lần lượt.<br>- Câu chốt (4) (*"Stalin finally said yes"*) $\rightarrow$ Hiện ảnh tư liệu thật của Stalin và **đóng con dấu xanh `[YES]`** cái rầm đúng chữ *"yes"*! | **Luật 3 (Liệt kê lý do/điều kiện $\rightarrow$ Bảng Checklist `[✓]` + Chốt quyết định bằng Ảnh thật Đóng dấu `[STAMP]`):** Quy trình chuẩn để biến một đoạn văn giải thích chính trị khô khan thành đồ họa bắt mắt. |

---

## 4. TỔNG KẾT 6 LUẬT CHUYỂN NGỮ "KỊCH BẢN $\rightarrow$ HÌNH ẢNH" (BỘ NÃO ĐẠO DIỄN CỦA ZIRO HISTORY)

Khi chỉ có `Kịch bản + Voice`, muốn AI dựng ra đúng chất `Ziro History` chứ không phải ghép ảnh vô hồn, AI bắt buộc phải phân loại từng câu trong kịch bản theo **6 Luật Chuyển Ngữ** này:

1. **Luật 1 — Gặp Ẩn dụ / So sánh (`"như một..."`, `"giống như..."`):** Dịch thẳng hình ảnh ẩn dụ đó ra nghĩa đen hài hước (VD: *"như công ty gia đình"* $\rightarrow$ Vẽ cửa hàng tạp hóa `KIM & SONS`; *"tôm nằm giữa các con cá voi"* $\rightarrow$ Vẽ con tôm kẹp giữa 3 con cá voi).
2. **Luật 2 — Gặp Câu Nhân - Quả (`"Nếu A thì dẫn đến B"`, `"Làm X sẽ bị Y"`):** Chia màn hình làm 3 nhịp thời gian theo đúng thứ tự từ: `[Vế A bật bên trái]` $\rightarrow$ `[Mũi tên bắn sang phải]` $\rightarrow$ `[Vế B đập xuống bên phải]`.
3. **Luật 3 — Gặp Đoạn Liệt kê 2–4 ý + Câu Chốt Quyết định:** Gom 2–4 ý liệt kê thành **Bảng Checklist `[✓]` gõ từng dòng**, và câu chốt quyết định của nhân vật lịch sử thì dùng **Thẻ Ảnh Tư Liệu Thật + Đóng Dấu (`[YES]` / `[DENIED]` / `[SURVIVED]`)**.
4. **Luật 4 — Gặp Con số Định lượng / Thời gian (`"26 triệu người"`, `"20 củ tỏi"`, `"100 ngày"`, `"80% lãnh thổ"`):** Bắt buộc kích hoạt **Bộ Đếm Số Chạy Vọt (`Number Counter`)** hoặc **Lưới Nhân Bản Icon (`Icon Repeater`)** đúng giây giọng đọc phát âm con số.
5. **Luật 5 — Gặp Câu Đối lập / Bước ngoặt (`"nhưng..."`, `"mặc dù đã chết..."`, `"nửa kia chìm vào bóng tối"`):** Giữ nguyên khung hình ở vế 1, và đúng mili-giây đọc từ khóa bước ngoặt ở vế 2 thì **đổi trạng thái trực tiếp trên hình (`Mắt mở -> Mắt nhắm`, `Đèn sáng -> Đèn tắt`, `Mặt cười -> Mặt mếu`)**.
6. **Luật 6 — Gặp Sự kiện Lịch sử / Truyền thuyết Dài:** Xen kẽ giữa giọng người dẫn chuyện (`Host Stick-Soldier`) và các đoạn **Đối thoại Sitcom ngắn (`Paper-Doll Dialogue`)** với lớp miệng đóng/mở theo từng câu thoại và bộ đếm trạng thái ở góc màn hình.

---

## 5. Phân Bổ Tỷ Trọng Các Loại Cảnh Trong Toàn Bộ 35 Phút Video (`[📊 Đã xác minh bằng số liệu]`)

Qua quét toàn bộ 24 tấm lưới Storyboard (`600 mẫu khung hình` suốt 35 phút 28 giây) và 7 luồng video `.mp4` (5 phút đầu liên tục `00:00 -> 05:05`), cấu trúc 1 tập video 35 phút của `Ziro History` chia chính xác theo tỷ lệ sau:

1. **Nhóm A — Sân khấu xám `#CCCCCC` + Chú lính dẫn chuyện + (Khung ảnh lịch sử thật / Checklist / Con số đếm / Lặp Icon / Sơ đồ Nhân - Quả):** Chiếm **~40% thời lượng** (`~14 phút`).
2. **Nhóm B — Bản đồ Vệ tinh Địa chính trị Thật + Spotlight + Tô vùng lãnh thổ + Mặt nạ tiến quân + Mũi tên/Icon quân sự:** Chiếm **~25% thời lượng** (`~9 phút`).
3. **Nhóm C — Cuộn giấy 11 Chương (`Chapter Scroll`) + Cảnh chuyển ý trung tâm (`Bridge Shots`) + Chia đôi màn hình so sánh (`Split-Screen`):** Chiếm **~10% thời lượng** (`~3.5 phút`).
4. **Nhóm D — Bối cảnh 2D Minh Họa Nhiều Chi Tiết (Đồi cỏ, Hang động, Cung điện, Cửa hàng, Lớp học, Lều trại) + Các con rối giấy 2D đối thoại/trượt ngang:** Chiếm **~25% thời lượng** (`~8.5 phút`).

---

## 6. CẬP NHẬT TRỌNG YẾU (TỪ BÀI HỌC THỰC CHIẾN): TẠI SAO VIDEO CỦA `ZIRO HISTORY` NHANH, DÀY ĐẶC CHI TIẾT VÀ CUỐN HÚT, CÒN LÀM SAI SẼ RA "CẢNH TĨNH ĐẤM VÀO MẮT"?

Khi đối chiếu trực tiếp 5 phút liên tục của `Ziro History` (`00:00 -> 05:05`) với thất bại của bản thử nghiệm đầu tiên, đây là **4 Bí Mật Cốt Lõi về Nhịp Điệu, Mật Độ Chi Tiết và Chuyển Ngữ Kịch Bản** mà hệ thống 4 Giai đoạn bắt buộc phải tuân thủ:

### 6.1. Luật Băm Nhịp Vi Mô (`1.5s – 2.2s Micro-Beat Decomposition`) — Cấm để 1 câu văn dài đứng im trên 1 cảnh!
* **Bẫy chết người khi dựng từ kịch bản văn xuôi tiếng Việt:**
  - Một câu văn trong kịch bản thường dài `30 – 45 chữ` (mất **`10 giây – 18 giây`** để đọc hết câu).
  - Nếu coi `1 câu văn = 1 cảnh (1 Beat)` $\rightarrow$ Màn hình sẽ đứng im suốt `10s – 18s` $\rightarrow$ Người xem chán ngấy ngay lập tức!
* **Cách `Ziro History` thực sự làm:**
  - Họ **KHÔNG dựng theo đơn vị "Câu chấm câu (`.`)"**, mà dựng theo đơn vị **"Cụm Danh từ / Động từ Kích hoạt (`Micro-Beat 1.5s – 2.2s`)"**!
  - Một câu dài `12 giây` bắt buộc phải được băm thành **5 đến 6 `Micro-Beats` liên hoàn**:
    - `0.0s – 2.0s` (Mệnh đề 1): Bật bối cảnh nền + Nhân vật chính.
    - `2.0s – 4.0s` (Cụm danh từ 1): Đạo cụ số 1 nảy lên (`Pop-in`) kèm chữ gõ `Typewriter` (2–3 từ).
    - `4.0s – 6.0s` (Cụm động từ): Camera phóng nhanh (`Zoom-in 1.15x`) hoặc Mũi tên bắn sang phải.
    - `6.0s – 8.0s` (Cụm số liệu): Bộ đếm số (`Counter`) quay tít hoặc Lưới 20–400 Icon bật lên rào rào.
    - `8.0s – 10.0s` (Mệnh đề đảo chiều *"Nhưng..."*): Đổi trạng thái ngay trên hình (`Tắt đèn`, `Chớp mắt`, `Rơi cây giáo`, `Đổ mồ hôi`) hoặc cắt gắt (`Hard Cut`) sang nhân vật đối lập!
    - `10.0s – 12.0s` (Cú chốt): Đập con dấu cao su (`[NONSENSE]` / `[YES]`) kèm rung màn hình (`Camera Shake`).

### 6.2. Luật Mật Độ Chi Tiết 4 Lớp Trong 1 Khung Hình (`4-Layer Visual Richness`) — Cấm dùng hàm hình học `PIL.ImageDraw` vẽ sơ sài!
Một khung hình của `Ziro History` không bao giờ chỉ có 1–2 hình khối trơ trọi, mà luôn có sự kết hợp của **Nguyên liệu thật + Đồ họa minh họa chi tiết cao**:
1. **Lớp 1 — Bối cảnh Nền giàu chi tiết (`Rich Environment / Real Satellite Map`):**
   - Nếu là Bản đồ: Phải là **Ảnh vệ tinh địa hình thật độ phân giải cao** (có núi non, đại dương, ánh đèn thành phố đêm), tuyệt đối không vẽ đa giác màu trơn bằng code!
   - Nếu là Bối cảnh 2D (như *Hang đá Hổ & Gấu*, *Tiệm KIM & SONS*, *Lều tướng nhà Tùy*): Phải là bức tranh minh họa 2D (`AI Illustrated Vector Art`) có đầy đủ chiều sâu, tường gạch, bàn ghế, ngọn nến, đống tỏi, cây thông, rèm lều.
2. **Lớp 2 — Tư liệu Lịch sử Thật đóng khung (`Authentic Archival Photos`):**
   - Mọi hiện vật, địa danh, nhân vật có ảnh chụp lịch sử (Phố Tehran 1970/1980, Khối trụ Cyrus ở Bảo tàng Anh, Tranh tường Goguryeo, Ảnh vệ tinh NASA) **bắt buộc dùng ảnh chụp thật 100%**, đóng khung bo góc trắng có đổ bóng.
3. **Lớp 3 — Nhân vật Con rối 2D & Đạo cụ Tương tác (`Modular Paper-Doll + Physics Props`):**
   - Nhân vật có nét vẽ hoạt hình chỉn chu, tách riêng lớp Miệng (`Closed/Half/Open`), Mắt (`Open/Blink`), Lông mày (`Normal/Angry/Worried`), Tay (`Down/Point/Hold Prop`) và các hạt biểu cảm (`Giọt mồ hôi`, `Gân máu đỏ`, `Khói hôi xanh`, `Mưa tỏi/vàng`).
4. **Lớp 4 — Chữ Đạo Diễn Động (`Kinetic / Typewriter Callout Text` — Tuyệt đối CẤM hộp phụ đề Karaoke dưới đáy!):**
   - **Cấm tuyệt đối** việc vẽ một hộp đen dưới đáy màn hình chép lại nguyên văn câu kịch bản dài 30 chữ.
   - Chữ trong `Ziro History` chỉ là **Từ khóa ngắn (`1 – 4 từ`)** đặt ngay cạnh vật thể hoặc trên đầu nhân vật, xuất hiện bằng hiệu ứng **Gõ từng ký tự (`Typewriter`)** hoặc **Đập từng chữ (`Word Pop`)** đúng mili-giây giọng đọc phát âm từ đó!

### 6.3. Luật Chuyển Động Camera Liên Tục (`Zero Static Frame Rule`)
* Không một khung hình nào được phép đứng yên (`Static Scale = 1.0`) quá `0.5 giây`.
* Mọi cảnh đều phải gắn **Quỹ đạo Camera (`Camera Rig`)**:
  - `Slow Push-In` (`1.00x -> 1.08x`) khi đang dẫn chuyện tăng kịch tính.
  - `Fast Zoom-To-Target` (`1.0x -> 1.45x` theo hàm `easeOutCubic`) khi chỉ vào một thành phố trên bản đồ hoặc một chi tiết trên bức ảnh.
  - `Whip-Pan` (Lia máy ngang tốc độ cao có làm mờ chuyển động nhẹ) khi chuyển từ Vế Trái sang Vế Phải.
  - `Damped Screen Shake` (Rung lắc màn hình tắt dần) khi đóng dấu mộc đỏ, nổ bom, hoặc sập ổ khóa.
