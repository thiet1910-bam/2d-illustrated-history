# Khuôn Mẫu `SKILL.md` Đa Ngành (Tùy Biến Theo Cấp Độ 1 → 4 & Hình Mẫu 1 → 6)

```markdown
---
name: [ten-skill-viet-thuong-gach-ngang]
description: |
  [1-2 câu: Skill làm gì và tạo ra kết quả/đầu ra gì]
  [1 câu: Dùng khi nào — Độc lập hay thuộc Bước mấy trong dây chuyền]
  Kích hoạt: /[tu-khoa-kich-hoat-duy-nhat]
---

# [TÊN SKILL] — [VAI TRÒ CỐT LÕI]

## 1. Vai trò & Kiến trúc Vận hành
- **Vai trò chuyên gia:** [Nêu ngắn gọn vai trò + Nguyên lý tư duy dẫn đường].
- **Cấp độ & Hình mẫu:** [Cấp độ 1 / 2 / 3 / 4] — [Hình mẫu 1 / 2 / 3 / 4 / 5 / 6] ([Chế độ: Độc lập `Standalone` HOẶC Dây chuyền `Pipeline`]).

## 2. Bước 0: Kiểm tra Đầu vào & Phân nhánh (`Entry Check & Routing`)
| Điều kiện đầu vào / Trạng thái ổ cứng | Hành động định tuyến bắt buộc |
| :--- | :--- |
| **Trường hợp A:** [VD: Đã có file bàn giao bước trước HOẶC người dùng đã cung cấp dữ liệu X] | [Chạy thẳng vào Bước 1 (Luồng A) / Hoặc chạy `scripts/scanners/...` nếu là Cấp độ 4]. |
| **Trường hợp B:** [VD: Chưa có dữ liệu khởi tạo HOẶC yêu cầu thuộc nhánh Y] | [Hỏi đúng thông tin còn thiếu / Hoặc định tuyến sang Luồng B]. |

## 3. Quy trình Thực thi & Lệnh Đọc Phẫu Thuật (`Surgical Read Workflow`)

### Bước 1: [Tên Bước 1 — VD: Phân tích / Định tuyến nhánh / Quét dữ liệu]
- **📖 Lệnh đọc tài liệu Bước 1:**
  - **Khi nào đọc:** Ngay khi bắt đầu Bước 1.
  - **Đọc ở đâu:** `references/[01-ten-file.md]` — **Từ `Mục 1` đến `Mục 2` (`StartLine: 1` → `EndLine: [XX]`)**. *(Giới hạn loại trừ: Không đọc Mục 3 và chưa đọc các file khác ở bước này. Nếu là Cấp độ 3, chỉ đọc `references/core/` + đúng 1 file trong `references/types/` khớp với nhánh đã chọn)*.
  - **Tại sao đọc:** Để lấy [tên bảng quy tắc / công thức định lượng cụ thể] phục vụ cho [hành động của Bước 1].
- **Hành động thực thi:**
  1. [Hành động cụ thể 1].
  2. [Hành động cụ thể 2].

### Bước 2: [Tên Bước 2 — VD: Triển khai chi tiết / Xuất kết quả theo Khuôn mẫu]
- **📖 Lệnh đọc tài liệu Bước 2:**
  - **Khi nào đọc:** Khi bước vào Bước 2.
  - **Đọc ở đâu:**
    1. `references/[02-ten-file.md]` — **Từ `Mục 1` đến `Mục [N]` (`StartLine: 1` → `EndLine: [YY]`)**.
    2. `templates/[ten-khuon-mau.md]` — **Toàn bộ file (`StartLine: 1` → `EndLine: [ZZ]`)**.
  - **Tại sao đọc:** Áp dụng công thức chuyên môn để điền dữ liệu sạch vào đúng khung đầu ra.
- **Hành động thực thi & Kiểm toán tự động (`Code Gate`):**
  1. Ghi kết quả ra file `[duong-dan-file-dau-ra]`.
  2. Chạy lệnh kiểm toán định lượng:
     `python .agent/skills/[ten-skill]/scripts/[ten-script-kiem-toan.py] "[duong-dan-file-dau-ra]"`
  3. Nếu script báo `[FAIL]`, bắt buộc sửa ngay các mục lỗi cho đến khi đạt `100% [PASS]`.

## 4. Cổng Kiểm Tra Chất Lượng & Điểm Dừng Cứng (`Quality Gate & Hard Stop`)
Trước khi báo cáo hoàn thành, xác nhận đạt toàn bộ Checklist sau:
- [ ] [Tiêu chí định lượng 1 — Có con số cụ thể].
- [ ] [Tiêu chí định lượng 2 — Có con số cụ thể].
- [ ] Script kiểm toán tự động đã báo `[PASS] 100%`.

**⏸️ ĐIỂM DỪNG CỨNG (`HARD GATE`):** Trình bày kết quả và hỏi người dùng:
*"Nếu bạn đồng ý → nói **'Duyệt'** để hoàn tất (hoặc chuyển sang bước tiếp theo). Nếu cần chỉnh sửa → chỉ rõ điểm cần sửa."*

## 5. Rào Chắn & Danh Sách Cấm Mặc Định (`Banned Defaults`)
1. ❌ **CẤM [Lỗi sai phổ biến số 1]:** Vì [Giải thích lý do Nhân – Quả].
2. ❌ **CẤM [Lỗi sai phổ biến số 2]:** Vì [Giải thích lý do Nhân – Quả].
3. ❌ **CẤM chép lời hướng dẫn vào file đầu ra:** File kết quả chỉ chứa dữ liệu sạch theo đúng `templates/`.
```
