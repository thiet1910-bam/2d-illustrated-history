# Bảng CẤM Khi Cập Nhật Skill

> File này phục vụ **Pha U3** (Thực thi).
> Kế thừa từ `playbook-skill-creator/references/mau-sai.md` + bổ sung mẫu sai CẬP NHẬT.
>
> 📌 Mẫu sai CHUNG (8 điều cấm + 5 quy tắc chống trùng lặp):
> → Xem `.claude/skills/playbook-skill-creator/references/mau-sai.md`
> File này chỉ bổ sung mẫu sai RIÊNG cho việc CẬP NHẬT.

---

## 6 Mẫu Sai Khi CẬP NHẬT Skill

| # | ❌ Mẫu sai | Tại sao sai | ✅ Làm đúng |
|:--|:--|:--|:--|
| U1 | **Sửa loạn** — AI sửa 10 file khi user chỉ yêu cầu 1 | Phình phạm vi phá cấu trúc. User mất kiểm soát. | Chỉ sửa file trong kế hoạch Pha U2 đã duyệt |
| U2 | **Đổi tên tiêu đề** — AI đổi "§A. BÓC TÁCH" thành "§1. PHÂN TÍCH" | Phá quy ước, user mất phương hướng. Các đường dẫn trỏ cũ hỏng. | Giữ tiêu đề gốc. Chỉ đổi nội dung bên trong. |
| U3 | **Thêm file lạ** — AI tạo `README.md`, `NOTES.md`, `SUMMARY.md` | Không ai yêu cầu. Vi phạm nguyên tắc "chỉ viết những gì cần". | Chỉ tạo file có trong kế hoạch Pha U2 |
| U4 | **Sửa không kiểm tra chéo** — Đổi nhân vật ở SKILL.md nhưng quên khuôn mẫu | Mâu thuẫn giữa các file. AI sau đọc sẽ bị rối. | Tìm sau khi sửa. Từ khóa cũ phải = 0 kết quả. |
| U5 | **Sửa triệu chứng** — User nói "tiêu đề sai" → AI sửa tiêu đề → nhưng nguyên nhân gốc là nội dung thiếu | Chữa ngọn không chữa gốc. Vấn đề quay lại. | Phản biện trước (Pha U1), tìm nguyên nhân gốc, sửa sau. |
| U6 | **Viết lại toàn bộ** — AI xóa 1 phần rồi viết lại hoàn toàn | Mất nội dung gốc đang đúng. Có thể thêm ảo giác (AI bịa nội dung). | Sửa có chọn lọc: chỉ đổi dòng/đoạn cần đổi. Giữ phần đúng. |
| U7 | **Tách vụn file (`Micro-Fragmentation`) & Bỏ rơi File Mồ Côi (`Orphan File`)** — File mới chỉ dài 25–40 dòng và dùng chung ở 1 Bước nhưng AI lại xé lẻ thành 2–3 file nhỏ, hoặc tạo file mới trong `references/` mà quên gắn lệnh đọc `StartLine–EndLine` vào `SKILL.md`. | Đẻ thêm việc bảo trì, làm lệch đánh số thứ tự hàng loạt file (`04 -> 05 -> 06`), và tạo ra file rác không bao giờ được AI đọc tới. | Giữ chung trong 1 file nếu $\le 80$ dòng (chia `## Mục 1`, `## Mục 2` + trỏ dòng). Luôn chạy `validate_skill_structure.py` sau khi sửa để bắt sống 100% file mồ côi. |

---

## 3 Quy Tắc Chống Tác Dụng Phụ

| # | Quy tắc | Cách kiểm tra |
|:--|:--|:--|
| 1 | **Sửa 1 file → kiểm tra file liên quan** | Nếu sửa SKILL.md → kiểm tra references/ có khớp? |
| 2 | **Đổi thuật ngữ → tìm toàn skill** | `grep -rn "từ_cũ" .claude/skills/skill-name/` → phải = 0 |
| 3 | **Thêm phần → kiểm tra đánh số** | Phần mới → kiểm tra lại thứ tự đánh số tất cả file |

---

## Phong Cách Sửa SAI (Tổng hợp)

| ❌ Sai | ✅ Đúng |
|:--|:--|
| Xóa phần rồi viết lại hoàn toàn | Sửa có chọn lọc, giữ phần đúng |
| Sửa xong tự chuyển Pha tiếp | Sửa xong → hỏi lại Cổng Duyệt |
| Đổi nhân vật 1 file, quên file khác | Tìm toàn skill, đổi tất cả |
| Thêm `README.md` "cho đầy đủ" | Không thêm file ngoài kế hoạch |
| Sửa ngay khi nhận vấn đề, không đọc | ĐỌC TRƯỚC (Pha U1), SỬA SAU (Pha U3) |
| "Bạn có muốn tôi sửa không?" | Trình bảng phản biện + đề xuất câu kích hoạt |
| Viết lẫn lộn ngôn ngữ Anh-Việt | Việt hoá toàn bộ, chỉ giữ ngôn ngữ gốc khi bắt buộc |
