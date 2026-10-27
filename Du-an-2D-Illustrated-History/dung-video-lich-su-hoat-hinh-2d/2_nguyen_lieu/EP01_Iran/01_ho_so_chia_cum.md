# HỒ SƠ PHÂN CỤM THÍCH ỨNG ĐỘNG & DANH MỤC TƯ LIỆU TẬP PHIM (`EP01_Iran`)

## 1. Thông Số Tổng Quan Bộ 3 File Đầu Vào (`1_input/EP01_Iran/`) & Kho Tư Liệu Tập
- **Mã tập phim:** `EP01_Iran`
- **File kịch bản lời dẫn (khớp 100% Audio):** `1_input/EP01_Iran/kich_ban_loi_dan.txt`
- **File kịch bản cấu trúc (chia Hồi / Phân đoạn / Skit / Ghi chú hình ảnh):** `1_input/EP01_Iran/kich_ban_chia_hoi.txt`
- **File âm thanh gốc nguyên khối:** `1_input/EP01_Iran/voice.MP3`
- **Tổng thời lượng Audio gốc (`float64`):** `1764.020s (29m 24.02s)`
- **Tổng số Hồi / Phân đoạn / Tiểu phẩm Skit phát hiện tự động:** `7 Hồi, 21 Phân đoạn (1.1 -> 7.3), 4 Skit`
- **Tổng số Cụm Thích Ứng Động (`Dynamic Adaptive Clusters`, `90s – 240s/cụm`):** `17 Cụm`
- **Kho tài sản thương hiệu & âm thanh dùng chung toàn kênh:** `2_nguyen_lieu/0_kho_dung_chung/brand_ui_assets/` & `2_nguyen_lieu/0_kho_dung_chung/audio_sfx_bgm/`
- **Kho tư liệu hình ảnh & bản đồ riêng của Tập (chia theo Cụm + STT + Mốc giây):** `2_nguyen_lieu/EP01_Iran/tu_lieu_tap/<cluster_id>/`
- **Thư mục chứa các gói Cụm & Bộ nhớ đệm từng nhịp (`cache_beats/`):** `2_nguyen_lieu/EP01_Iran/cac_cum/`

---

## 2. Bảng Theo Dõi Tiến Độ Vòng Lặp Cuốn Chiếu Từng Cụm (`Dynamic Cluster Loop Tracker`)

| Thứ Tự | Mã Cụm (`cluster_id`) | Thuộc Hồi (`act_id`) | Các Phân Đoạn Gộp Trong Cụm (`segments`) | Loại (`HOI / SKIT`) | Số Nhịp (`beats`) | Mốc Audio (`t0 -> t1`) | Thời Lượng (`s`) | Trạng Thái (`PENDING / SLICED / RENDERED / DONE_PASS`) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `01` | `cum_01_Hoi_I` | `HỒI I` | `1.1, 1.2, 1.3` | `HOI_PHAN_TICH` | `12` | `0.00 -> 102.79` | `102.787s` | `SLICED` |
| `02` | `cum_02_Hoi_II_seg_2_1_2_2` | `HỒI II` | `2.1, 2.2` | `HOI_PHAN_TICH` | `11` | `102.63 -> 210.14` | `107.512s` | `SLICED` |
| `03` | `cum_03_Skit_1` | `HỒI II` | `2.2_Skit_1` | `SKIT_CHAM_BIEM` | `8` | `210.14 -> 251.54` | `41.402s` | `DONE_PASS` |
| `04` | `cum_04_Hoi_II_seg_2_2_2_3` | `HỒI II` | `2.2, 2.3` | `HOI_PHAN_TICH` | `12` | `251.54 -> 402.77` | `151.230s` | `PENDING` |
| `05` | `cum_05_Hoi_III_seg_3_1_3_2` | `HỒI III` | `3.1, 3.2` | `HOI_PHAN_TICH` | `11` | `402.77 -> 511.78` | `109.010s` | `PENDING` |
| `06` | `cum_06_Skit_2` | `HỒI III` | `3.2_Skit_2` | `SKIT_CHAM_BIEM` | `6` | `511.78 -> 549.04` | `37.260s` | `PENDING` |
| `07` | `cum_07_Hoi_III_seg_3_3` | `HỒI III` | `3.3` | `HOI_PHAN_TICH` | `9` | `549.04 -> 640.94` | `91.900s` | `PENDING` |
| `08` | `cum_08_Hoi_IV_seg_4_1_4_2` | `HỒI IV` | `4.1, 4.2` | `HOI_PHAN_TICH` | `18` | `640.94 -> 828.60` | `187.660s` | `PENDING` |
| `09` | `cum_09_Hoi_IV_seg_4_3` | `HỒI IV` | `4.3` | `HOI_PHAN_TICH` | `9` | `828.60 -> 926.02` | `97.420s` | `PENDING` |
| `10` | `cum_10_Hoi_V_seg_5_1_5_2` | `HỒI V` | `5.1, 5.2` | `HOI_PHAN_TICH` | `15` | `926.02 -> 1104.85` | `178.830s` | `PENDING` |
| `11` | `cum_11_Hoi_V_seg_5_3` | `HỒI V` | `5.3` | `HOI_PHAN_TICH` | `9` | `1104.85 -> 1209.72` | `104.870s` | `PENDING` |
| `12` | `cum_12_Hoi_VI_seg_6_1_6_2` | `HỒI VI` | `6.1, 6.2` | `HOI_PHAN_TICH` | `9` | `1209.72 -> 1314.31` | `104.590s` | `PENDING` |
| `13` | `cum_13_Skit_3` | `HỒI VI` | `6.2_Skit_3` | `SKIT_CHAM_BIEM` | `6` | `1314.31 -> 1339.42` | `25.110s` | `PENDING` |
| `14` | `cum_14_Hoi_VI_seg_6_2_6_3` | `HỒI VI` | `6.2, 6.3` | `HOI_PHAN_TICH` | `14` | `1339.42 -> 1500.59` | `161.170s` | `PENDING` |
| `15` | `cum_15_Hoi_VII_seg_7_1` | `HỒI VII` | `7.1` | `HOI_PHAN_TICH` | `3` | `1500.59 -> 1528.19` | `27.600s` | `PENDING` |
| `16` | `cum_16_Skit_4` | `HỒI VII` | `7.1_Skit_4` | `SKIT_CHAM_BIEM` | `5` | `1528.19 -> 1542.82` | `14.630s` | `PENDING` |
| `17` | `cum_17_Hoi_VII_seg_7_1_7_2_7_3` | `HỒI VII` | `7.1, 7.2, 7.3` | `HOI_PHAN_TICH` | `22` | `1542.82 -> 1764.02` | `221.200s` | `PENDING` |

---

## 3. Danh Mục Ghi Chú Hình Ảnh Kịch Bản & File Tư Liệu Theo Cụm (`Episode Visual & Asset Bible`)

- **Tổng số file ảnh tư liệu đã phân theo Cụm trong `2_nguyen_lieu/EP01_Iran/tu_lieu_tap/<cluster_id>/`:** `25 file` (Chuẩn định danh `{STT}_{beat_id}_{t0}s-{t1}s_{ten_mo_ta}.jpg`)

| Mã Phân Đoạn / Skit | Thuộc Cụm (`cluster_id`) | Ghi Chú Hình Ảnh Trích Xuất Tự Động Của Tác Giả (`author_visual_note`) | Các File Tư Liệu Đánh STT + Mốc Giây Trong `tu_lieu_tap/<cluster_id>/` |
| :---: | :--- | :--- | :--- |
| `1.1` | `cum_01_Hoi_I` | Hai bức ảnh chụp cùng một góc phố Tehran đặt cạnh nhau | `01_beat02_0007s-0018s_tehran_1970_shops.jpg`, `02_beat02_0010s-0018s_tehran_1970_boulevard.jpg`, `03_beat02_0012s-0018s_tehran_1970_street_extra.jpg`, `04_beat03_0018s-0028s_tehran_1980_revolution.jpg`, `05_beat03_0020s-0028s_tehran_1980_crowd.jpg`, `06_beat03_0022s-0028s_iran_1979_women_chador.jpg`, `07_beat04_0028s-0034s_satellite_iran_middle_east.jpg`, `08_beat06_0037s-0049s_act1_youth_vs_clerics.jpg`, `09_beat07_0049s-0057s_act1_three_crimes_to_prison.jpg`, `10_beat08_0057s-0065s_act1_palace_civilization_bright.jpg` |
| `1.2` | `cum_01_Hoi_I` | Cảnh sát đạo đức tuần tra, xen lẫn hình ảnh giới trẻ Iran hiện đại | `01_beat02_0007s-0018s_tehran_1970_shops.jpg`, `02_beat02_0010s-0018s_tehran_1970_boulevard.jpg`, `03_beat02_0012s-0018s_tehran_1970_street_extra.jpg`, `04_beat03_0018s-0028s_tehran_1980_revolution.jpg`, `05_beat03_0020s-0028s_tehran_1980_crowd.jpg`, `06_beat03_0022s-0028s_iran_1979_women_chador.jpg`, `07_beat04_0028s-0034s_satellite_iran_middle_east.jpg`, `08_beat06_0037s-0049s_act1_youth_vs_clerics.jpg`, `09_beat07_0049s-0057s_act1_three_crimes_to_prison.jpg`, `10_beat08_0057s-0065s_act1_palace_civilization_bright.jpg` |
| `1.3` | `cum_01_Hoi_I` | Bản đồ địa chính trị Trung Đông thu phóng vào vị trí của Iran và các mỏ dầu | `01_beat02_0007s-0018s_tehran_1970_shops.jpg`, `02_beat02_0010s-0018s_tehran_1970_boulevard.jpg`, `03_beat02_0012s-0018s_tehran_1970_street_extra.jpg`, `04_beat03_0018s-0028s_tehran_1980_revolution.jpg`, `05_beat03_0020s-0028s_tehran_1980_crowd.jpg`, `06_beat03_0022s-0028s_iran_1979_women_chador.jpg`, `07_beat04_0028s-0034s_satellite_iran_middle_east.jpg`, `08_beat06_0037s-0049s_act1_youth_vs_clerics.jpg`, `09_beat07_0049s-0057s_act1_three_crimes_to_prison.jpg`, `10_beat08_0057s-0065s_act1_palace_civilization_bright.jpg` |
| `2.1` | `cum_02_Hoi_II_seg_2_1_2_2` | Bản đồ thế giới cổ đại mở rộng, tượng Cyrus Đại đế, cận cảnh Khối trụ Cyrus bằng đất sét tại Bảo tàng Anh | `01_beat01_0108s-0125s_satellite_ancient_persia.jpg`, `02_beat04_0145s-0168s_cyrus_cylinder_british_museum.jpg`, `03_beat08_0190s-0218s_persepolis_relief_architecture.jpg`, `04_beat02_cyrus_superpower_throne_ziro.png`, `05_beat05_babylon_liberation_vs_tyrant_ziro.png`, `06_beat08_shah_1971_persepolis_tent_party_ziro.png`, `07_beat09_11_hollywood_monster_vs_thermopylae_ziro.png` |
| `2.2` | `cum_04_Hoi_II_seg_2_2_2_3` | Cảnh phim "300" của Hollywood với những chiến binh Sparta cơ bắp, đối lập với kiến trúc tráng lệ của kinh đô Persepolis | `(Chưa có tư liệu)` |
| `Skit_1` | `cum_03_Skit_1` | Cảnh phim "300" của Hollywood với những chiến binh Sparta cơ bắp, đối lập với kiến trúc tráng lệ của kinh đô Persepolis — Tiểu phẩm Skit #1: Giọng đối thoại châm biếm trên chiến trường | `01_beat01_0219s-0226s_satellite_thermopylae_pass.jpg`, `02_beat02_0226s-0235s_tent_general_and_xerxes.jpg`, `03_beat04_0235s-0244s_spartan_red_trunks_baby_oil.jpg`, `04_beat06_0244s-0252s_hollywood_3m_pierced_xerxes.jpg`, `05_beat08_0252s-0261s_greek_historian_writing.jpg` |
| `2.2` | `cum_04_Hoi_II_seg_2_2_2_3` | Cảnh phim "300" của Hollywood với những chiến binh Sparta cơ bắp, đối lập với kiến trúc tráng lệ của kinh đô Persepolis | `(Chưa có tư liệu)` |
| `2.3` | `cum_04_Hoi_II_seg_2_2_2_3` | Chiến binh Ả Rập cưỡi ngựa trên sa mạc, nghi lễ tưởng niệm Ashura của người Hồi giáo dòng Shia tại Iran | `(Chưa có tư liệu)` |
| `3.1` | `cum_05_Hoi_III_seg_3_1_3_2` | Những giếng dầu đầu tiên phun trào tại Trung Đông, xen lẫn cảnh công nhân bản địa nghèo khổ và giới quý tộc Anh | `(Chưa có tư liệu)` |
| `3.2` | `cum_05_Hoi_III_seg_3_1_3_2` | Thủ tướng Mohammad Mossadegh trên bìa tạp chí Time năm 1951, đám đông reo hò ở Tehran | `(Chưa có tư liệu)` |
| `Skit_2` | `cum_06_Skit_2` | Thủ tướng Mohammad Mossadegh trên bìa tạp chí Time năm 1951, đám đông reo hò ở Tehran — Tiểu phẩm Skit #2: Giọng đối thoại điệp viên thập niên 1950 | `(Chưa có tư liệu)` |
| `3.3` | `cum_07_Hoi_III_seg_3_3` | Bạo loạn đường phố Tehran năm 1953, xe tăng tiến vào dinh Thủ tướng, hình ảnh Shah Pahlavi đeo kính đen | `(Chưa có tư liệu)` |
| `4.1` | `cum_08_Hoi_IV_seg_4_1_4_2` | Đường phố Tehran thập niên 1970 hiện đại, chuyển sang cảnh những dãy lều lụa xa hoa giữa sa mạc Persepolis | `01_beat07_0730s-0760s_iran_1979_protest_women.jpg`, `02_beat09_0760s-0795s_tehran_1979_revolution_rally.jpg`, `03_beat12_0795s-0838s_tehran_1979_hostage_crisis.jpg` |
| `4.2` | `cum_08_Hoi_IV_seg_4_1_4_2` | Biểu tình biển người năm 1979, Khomeini bước xuống máy bay, sinh viên trèo tường Đại sứ quán Mỹ | `01_beat07_0730s-0760s_iran_1979_protest_women.jpg`, `02_beat09_0760s-0795s_tehran_1979_revolution_rally.jpg`, `03_beat12_0795s-0838s_tehran_1979_hostage_crisis.jpg` |
| `4.3` | `cum_09_Hoi_IV_seg_4_3` | Xe tăng Iraq tràn qua biên giới, lính Iran đeo mặt nạ phòng độc trong chiến hào đẫm máu | `(Chưa có tư liệu)` |
| `5.1` | `cum_10_Hoi_V_seg_5_1_5_2` | Lãnh tụ tối cao Khamenei, các cuộc duyệt binh của Vệ binh Cách mạng Hồi giáo IRGC | `(Chưa có tư liệu)` |
| `5.2` | `cum_10_Hoi_V_seg_5_1_5_2` | Bản đồ Trung Đông với các mũi tên vươn ra từ Iran tới Lebanon, Gaza, Yemen, Iraq | `(Chưa có tư liệu)` |
| `5.3` | `cum_11_Hoi_V_seg_5_3` | Đối lập giữa các bức tường vẽ khẩu hiệu chống Mỹ bên ngoài và những bữa tiệc ngầm của giới trẻ bên trong căn hộ ở Tehran | `(Chưa có tư liệu)` |
| `6.1` | `cum_12_Hoi_VI_seg_6_1_6_2` | Bản đồ Trung Đông đầu những năm 2000, cảnh Saddam Hussein bị bắt và vụ thử hạt nhân của Triều Tiên | `(Chưa có tư liệu)` |
| `6.2` | `cum_14_Hoi_VI_seg_6_2_6_3` | Những dãy máy ly tâm dưới lòng đất, các dòng code ma trận, chuyển sang chiếc xe bán tải trên con đường vắng | `(Chưa có tư liệu)` |
| `Skit_3` | `cum_13_Skit_3` | Những dãy máy ly tâm dưới lòng đất, các dòng code ma trận, chuyển sang chiếc xe bán tải trên con đường vắng — Tiểu phẩm Skit #3: Giọng đối thoại tỉnh rụi trong phòng điều khiển | `(Chưa có tư liệu)` |
| `6.2` | `cum_14_Hoi_VI_seg_6_2_6_3` | Những dãy máy ly tâm dưới lòng đất, các dòng code ma trận, chuyển sang chiếc xe bán tải trên con đường vắng | `(Chưa có tư liệu)` |
| `6.3` | `cum_14_Hoi_VI_seg_6_2_6_3` | Tướng Soleimani, đàn UAV Shahed trên bầu trời Ukraine, mưa tên lửa đạn đạo trên bầu trời Trung Đông năm 2024–2026 | `(Chưa có tư liệu)` |
| `7.1` | `cum_17_Hoi_VII_seg_7_1_7_2_7_3` | Đường phố Tehran hiện tại, đồng tiền Rial mất giá, những con đập khô cạn | `(Chưa có tư liệu)` |
| `Skit_4` | `cum_16_Skit_4` | Đường phố Tehran hiện tại, đồng tiền Rial mất giá, những con đập khô cạn — Tiểu phẩm Skit #4: Giọng đối thoại tỉnh rụi | `(Chưa có tư liệu)` |
| `7.1` | `cum_17_Hoi_VII_seg_7_1_7_2_7_3` | Đường phố Tehran hiện tại, đồng tiền Rial mất giá, những con đập khô cạn | `(Chưa có tư liệu)` |
| `7.2` | `cum_17_Hoi_VII_seg_7_1_7_2_7_3` | Chiến hào chiến tranh Iran-Iraq, cận cảnh chiếc chìa khóa nhựa, chuyển sang hình ảnh Mahsa Amini | `(Chưa có tư liệu)` |
| `7.3` | `cum_17_Hoi_VII_seg_7_1_7_2_7_3` | Quay lại bản đồ địa chính trị, rồi chuyển dần về hai bức ảnh Tehran 1970 vs Hiện tại | `(Chưa có tư liệu)` |
