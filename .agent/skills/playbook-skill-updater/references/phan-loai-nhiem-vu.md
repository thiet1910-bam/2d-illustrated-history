# Phân Loại Nhiệm Vụ: NẶNG và NHẸ

> File này phục vụ **Pha U0** (Phân Loại Nhiệm Vụ).
> Trả lời: **Nhiệm vụ này NẶNG hay NHẸ? Đi quy trình nào?**
>
> Tham chiếu tư duy:
> - **Charlie Munger** — "Muốn thành công, hãy tìm mọi cách thất bại trước, rồi tránh nó." (tư duy ngược): Hỏi ngược "Nếu phân loại SAI thì hậu quả gì?" → Nhiệm vụ nặng mà chạy Luồng Nhanh = bỏ sót, sửa loạn. Nhiệm vụ nhẹ mà chạy Quy Trình Đầy Đủ = lãng phí thời gian.
> - **Elon Musk** — Tư duy gốc rễ: Không hỏi "giống trường hợp nào?" mà hỏi "bản chất thay đổi là gì?"

---

## §1. CÂY QUYẾT ĐỊNH PHÂN LOẠI

```
Vấn đề cập nhật ảnh hưởng bao nhiêu FILE?
├─ 1-2 file
│   ├─ Loại thay đổi = Đổi tên/thuật ngữ/lỗi chính tả/số liệu?
│   │   └─ ✅ → NHẸ (Luồng Nhanh)
│   ├─ Loại thay đổi = Sửa nội dung phần (< 30 dòng)?
│   │   └─ ✅ → NHẸ (Luồng Nhanh)
│   └─ Loại thay đổi = Thêm/xóa phần, đổi quy trình?
│       └─ ⚠️ → NẶNG (dù ít file — vì ảnh hưởng cấu trúc)
│
├─ 3+ file
│   ├─ Thay đổi chỉ là tìm + thay thế cùng 1 thuật ngữ?
│   │   └─ ✅ → NHẸ (Luồng Nhanh — nhiều file nhưng cùng loại sửa)
│   └─ Thay đổi khác nhau ở mỗi file?
│       └─ ⚠️ → NẶNG (Quy Trình Đầy Đủ)
│
└─ Không chắc?
    └─ ⚠️ → Mặc định NẶNG (an toàn hơn)
```

---

## §2. BẢNG TIÊU CHÍ CHI TIẾT

| Tiêu chí | NHẸ (Luồng Nhanh) | NẶNG (Quy Trình Đầy Đủ) |
|---|---|---|
| **Số file ảnh hưởng** | 1-2 file, hoặc nhiều file nhưng cùng loại sửa | ≥ 3 file với thay đổi khác nhau |
| **Loại thay đổi** | Đổi tên/thuật ngữ, sửa lỗi chính tả, sửa số liệu, sửa nội dung ≤ 30 dòng | Tách/gộp file, thêm quy trình, thêm tham chiếu mới, đổi cấu trúc |
| **Rủi ro tác dụng phụ** | Thấp — chỉ nội dung, không đổi cấu trúc | Cao — tham chiếu chéo, đường dẫn trỏ, đánh số bị ảnh hưởng |
| **Cần chia nhiệm vụ con?** | ❌ Không | ✅ Có — chia 2A, 2B, 2C... |
| **Quy trình** | Pha U0 → Luồng Nhanh (phản biện rút gọn + kế hoạch rút gọn + sửa + kiểm tra) | Pha U0 → U1 → U2 (+ chia nhiệm vụ con) → U3 (chạy từng nhiệm vụ con) |

---

## §3. VÍ DỤ THỰC TẾ

### Ví dụ 1: NHẸ — Đổi tên nhân vật

**Vấn đề:** "Đổi tên Grace → Sarah trong toàn skill."
**Phân loại:**
- Ảnh hưởng: nhiều file, nhưng cùng 1 loại sửa (tìm + thay thế)
- Loại: Đổi thuật ngữ
- Rủi ro: Thấp (chỉ nội dung)
→ **NHẸ (Luồng Nhanh)**

### Ví dụ 2: NHẸ — Sửa số liệu sai

**Vấn đề:** "Tiêu đề ghi '2 phong cách' nhưng có 3."
**Phân loại:**
- Ảnh hưởng: 1-2 file
- Loại: Sửa số liệu
- Rủi ro: Thấp
→ **NHẸ (Luồng Nhanh)**

### Ví dụ 3: NẶNG — Tái cấu trúc quy trình + thêm tham chiếu

**Vấn đề:** "Quy trình thiếu bước phân loại nhiệm vụ. Cần thêm Pha mới + file tham chiếu mới."
**Phân loại:**
- Ảnh hưởng: SKILL.md + file mới + khuôn mẫu
- Loại: Đổi quy trình + thêm tham chiếu
- Rủi ro: Cao (tham chiếu chéo, đánh số)
→ **NẶNG (Quy Trình Đầy Đủ)** — chia nhiệm vụ con: 2A (tạo tham chiếu mới) → 2B (sửa SKILL.md) → 2C (sửa khuôn mẫu)

### Ví dụ 4: Trường hợp đặc biệt — Sửa ít file nhưng NẶNG

**Vấn đề:** "SKILL.md cần thêm Pha mới vào quy trình."
**Phân loại:**
- Ảnh hưởng: chỉ 1 file (SKILL.md)
- Loại: Đổi quy trình — cấu trúc thay đổi
- Rủi ro: Cao (tất cả tham chiếu ánh xạ theo pha)
→ **NẶNG** — dù chỉ 1 file

---

## §4. SAU KHI PHÂN LOẠI

### Nếu NHẸ → Luồng Nhanh

```
1. Phản biện rút gọn:
   - Xác nhận nguyên nhân gốc (không chỉ triệu chứng)
   - Phát hiện nhanh tác dụng phụ tiềm ẩn
   - Trình: "[Vấn đề] → [Nguyên nhân gốc] → [Giải pháp] → [Kiểm tra tác dụng phụ]"

2. Kế hoạch rút gọn:
   - Bảng 1 cột: | File | Thay đổi | Rủi ro |
   - Không cần chia nhiệm vụ con

3. User duyệt 1 lần → Sửa → Kiểm tra → Trình kết quả
```

### Nếu NẶNG → Quy Trình Đầy Đủ

```
1. Chia nhiệm vụ con:
   - Mỗi nhiệm vụ con = 1 đơn vị công việc độc lập (VD: "2A: Tạo file tham chiếu mới")
   - Đặt tên: 2A, 2B, 2C... (hoặc mô tả ngắn)
   - Xác định THỨ TỰ: nhiệm vụ con nào phụ thuộc nhiệm vụ con nào?

2. Tạo lộ trình:
   → Dùng khuôn mẫu `templates/roadmap-nhiem-vu-nang.md`
   - Bảng lộ trình: nhiệm vụ con → mô tả → phụ thuộc → trạng thái
   - Bảng kiểm tra riêng cho mỗi nhiệm vụ con
   
3. Chạy từng nhiệm vụ con:
   - Mỗi nhiệm vụ con: Làm → Kiểm tra (bảng kiểm tra riêng) → Trình user → User duyệt
   - Chỉ chuyển nhiệm vụ con tiếp khi nhiệm vụ con trước đã duyệt
   - Nếu nhiệm vụ con không đạt → sửa → kiểm tra lại → trình lại
```

---

## §5. CẢNH BÁO

> ⚠️ **Không phân loại dựa trên "cảm giác".** Dùng cây quyết định §1 + bảng tiêu chí §2.
> ⚠️ **Không chắc = NẶNG.** An toàn hơn chạy chậm đúng hơn chạy nhanh sai.
> ⚠️ **User có quyền đổi.** AI phân loại NHẸ nhưng user muốn NẶNG → chạy NẶNG. Và ngược lại.
