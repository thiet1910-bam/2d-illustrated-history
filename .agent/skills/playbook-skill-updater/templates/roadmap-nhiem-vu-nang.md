# Khuôn Mẫu Lộ Trình Nhiệm Vụ NẶNG

> Khuôn mẫu này dùng khi nhiệm vụ được phân loại **NẶNG** ở Pha U0.
> AI điền vào khuôn mẫu này ở **Pha U2** (Kế hoạch) và cập nhật ở **Pha U3** (Thực thi).
> Mỗi nhiệm vụ con chạy xong → trình user → user duyệt → mới chuyển nhiệm vụ con tiếp.

---

## §1. LỘ TRÌNH TỔNG THỂ

> Điền bảng này ở Pha U2. Cập nhật trạng thái ở Pha U3.

| Nhiệm vụ con | Mô tả ngắn | File ảnh hưởng | Phụ thuộc | Trạng thái |
|--------------|------------|---------------|-----------|------------|
| 2A | [Mô tả] | [File 1, File 2] | Không | ⬜ Chờ |
| 2B | [Mô tả] | [File 3] | 2A xong trước | ⬜ Chờ |
| 2C | [Mô tả] | [File 4, File 5] | 2A, 2B xong trước | ⬜ Chờ |

**Ký hiệu trạng thái:**
- ⬜ Chờ — chưa bắt đầu
- 🔄 Đang làm — AI đang thực thi
- ✅ Xong — user đã duyệt
- 🔁 Sửa lại — user yêu cầu sửa
- ❌ Hủy — không cần làm nữa

---

## §2. BẢNG KIỂM TRA TỪNG NHIỆM VỤ CON

> Mỗi nhiệm vụ con có bảng kiểm tra riêng. AI chạy bảng kiểm tra SAU KHI hoàn thành nhiệm vụ con, TRƯỚC KHI trình user.

### Khuôn Mẫu Bảng Kiểm Tra Nhiệm Vụ Con [Tên]

**Trước khi làm:**
- [ ] Đã đọc đúng file tham chiếu cần thiết cho nhiệm vụ con này?
- [ ] Hiểu rõ nhiệm vụ con này làm GÌ và KHÔNG làm gì?
- [ ] Nhiệm vụ con phụ thuộc (nếu có) đã hoàn thành?

**Trong khi làm:**
- [ ] Chỉ sửa đúng file + dòng trong kế hoạch?
- [ ] Giữ nguyên quy ước tiêu đề gốc?
- [ ] Giữ nguyên quy ước đặt tên gốc?
- [ ] Nội dung mới có nhãn nguồn? (`[📊]` / `[⚠️]` / `[📌]` / `[✅]`)

**Sau khi làm:**
- [ ] Tìm từ khóa cũ (nếu đổi thuật ngữ) → 0 kết quả?
- [ ] Kiểm tra chéo: file liên quan có bị ảnh hưởng không?
- [ ] Đường dẫn trỏ vẫn đúng?
- [ ] So sánh TRƯỚC/SAU: chỉ thay đổi đúng chỗ đã kế hoạch?

---

## §3. BÁO CÁO TỪNG NHIỆM VỤ CON (Trình User)

> Sau mỗi nhiệm vụ con, trình user báo cáo theo định dạng:

```markdown
### Nhiệm vụ con [Tên] — Hoàn Thành

**Đã làm:**
- [Liệt kê thay đổi cụ thể, file + dòng]

**Bảng kiểm tra nhiệm vụ con:**
- [x] Mục 1 — đạt
- [x] Mục 2 — đạt
- [ ] Mục 3 — ⚠️ [ghi chú nếu có vấn đề]

**Tóm tắt thay đổi:**
[Tóm tắt thay đổi — dòng TRƯỚC so với SAU]

**Kiểm tra tác dụng phụ:**
- [Liệt kê file liên quan đã kiểm tra]

→ *"Nếu OK nhiệm vụ con này → nói: **'Duyệt nhiệm vụ con [Tên]'**. Nếu cần sửa → nói chỗ cần sửa."*
```

---

## §4. BÁO CÁO TỔNG KẾT (Sau tất cả nhiệm vụ con)

> Trình sau khi TẤT CẢ nhiệm vụ con đều đã duyệt.

```markdown
### TỔNG KẾT NHIỆM VỤ NẶNG

**Lộ trình hoàn thành:**
| Nhiệm vụ con | Trạng thái | Số lần sửa lại |
|--------------|-----------|----------------|
| 2A | ✅ | 0 |
| 2B | ✅ | 1 (sửa quy ước đặt tên) |
| 2C | ✅ | 0 |

**Tổng file đã sửa:** [số]
**Kiểm tra chéo cuối cùng:**
- Cây thư mục TRƯỚC/SAU: [GIỐNG / KHÁC — chi tiết]
- Tìm từ khóa cũ: 0 kết quả ✅
- Đường dẫn trỏ: tất cả đúng ✅

→ *"Nếu OK toàn bộ → nói: **'Duyệt Pha U3'**. Nếu cần sửa → nói chỗ cần sửa."*
```

---

## §5. VÍ DỤ LỘ TRÌNH ĐÃ ĐIỀN

| Nhiệm vụ con | Mô tả ngắn | File ảnh hưởng | Phụ thuộc | Trạng thái |
|--------------|------------|---------------|-----------|------------|
| 2A | Tạo file tham chiếu `phan-loai-nhiem-vu.md` | references/phan-loai-nhiem-vu.md | Không | ✅ Xong |
| 2B | Tạo khuôn mẫu `roadmap-nhiem-vu-nang.md` | templates/roadmap-nhiem-vu-nang.md | Không | ✅ Xong |
| 2C | Sửa `triet-ly-cap-nhat.md` — thêm triết lý #6, #7 | references/triet-ly-cap-nhat.md | Không | 🔄 Đang làm |
| 2D | Sửa `bang-kiem-tra.md` — thêm mục U0 + nhiệm vụ con | templates/bang-kiem-tra.md | 2A | ⬜ Chờ |
| 2E | Sửa `SKILL.md` — tái cấu trúc quy trình | SKILL.md | 2A, 2B, 2C, 2D | ⬜ Chờ |
