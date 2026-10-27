# Nhãn Nguồn, Đa Ngôn Ngữ & Việt Hoá

> File này bổ sung cho `quy-tac-viet.md` của skill `playbook-skill-creator`.
> Chứa 3 quy tắc chuyên sâu: Đa ngôn ngữ, Nhãn nguồn, Việt hoá.

---

## §1. Quy Tắc Viết Skill Đa Ngôn Ngữ (Đầu vào ngôn ngữ A → Đầu ra ngôn ngữ B)

Khi skill nhận đầu vào bằng ngôn ngữ A (VD: tiếng Anh) nhưng đầu ra bằng ngôn ngữ B (VD: tiếng Việt), viết rõ 4 quy tắc trong SKILL.md:

| # | Quy tắc | Ví dụ |
|:--|:--------|:------|
| 1 | **Đầu ra viết bằng ngôn ngữ [B]** | "Toàn bộ đầu ra PHẢI viết bằng tiếng Việt." |
| 2 | **Trích dẫn → dịch + ghi nguồn gốc** | Trích dẫn Việt hoá + `(Gốc Anh: @user, file.md)` |
| 3 | **Tìm kiếm/cào dữ liệu bằng ngôn ngữ [A]** | "Tìm kiếm LUÔN dùng từ khoá tiếng Anh" (vì tệp khán giả là US/EU) |
| 4 | **Ngoại lệ giữ nguyên ngôn ngữ [A]** | Tên riêng, tên kênh, từ khoá SEO, thuật ngữ chuyên môn lần đầu |

**Tại sao cần ghi rõ:** AI mặc định đầu ra cùng ngôn ngữ đầu vào. Không ghi rõ → AI trả lời tiếng Anh (vì đầu vào là tiếng Anh) → user không đọc được.

---

## §2. Quy Tắc Nhãn Nguồn Cho Skill Phân Tích Dữ Liệu

Khi đầu ra của skill chứa nhận định dựa trên dữ liệu đầu vào, thêm **hệ thống nhãn nguồn** vào SKILL.md + khuôn mẫu:

**✅ Đúng — mỗi nhận định có nhãn:**
```markdown
"Chủ đề Lũ lụt: 4 video, Outlier TB 5.2x" `[📊 Dream100 data]`
```

**❌ Sai — nhận định không nhãn:**
```markdown
"Chủ đề Lũ lụt rất phổ biến và có tiềm năng cao."
```

**4 nhãn chuẩn:**
- `[📊 Tên nguồn dữ liệu]` — số liệu từ file dữ liệu thật
- `[📌 Tên nguồn thật]` — trích dẫn từ bình luận, Reddit, liên kết thật
- `[⚠️ Giả thuyết]` — AI tự suy luận, không có dẫn chứng
- `[✅ User chốt]` — quyết định do user xác nhận

**Quy tắc tỷ lệ:** `[⚠️]` > 40% tổng nhãn → CẢNH BÁO user "Dữ liệu chưa đủ tin cậy".

---

## §3. Quy Tắc Việt Hoá

Khi viết skill (cả skill mới lẫn cập nhật skill cũ), toàn bộ nội dung PHẢI viết bằng tiếng Việt. Thuật ngữ nước ngoài PHẢI dịch sang tiếng Việt + giải thích ngay lần đầu xuất hiện.

**KHÔNG viết lẫn lộn ngôn ngữ** — kiểu tiếng Anh không ra Anh, Việt không ra Việt. Điều này vô tác dụng và gây khó chịu khi đọc.

| # | Quy tắc | Ví dụ |
|:--|:--------|:------|
| 1 | **Dịch thuật ngữ nước ngoài sang tiếng Việt** | "Side-effect" → "Tác dụng phụ", "Workflow" → "Quy trình" |
| 2 | **Giải thích thuật ngữ lần đầu** | "Zetlag (tái tạo: giữ 60-80% khung xương, đổi 20-40% chi tiết)" |
| 3 | **Ngoại lệ — GIỮ ngôn ngữ gốc khi:** | (1) Tên riêng, (2) Tên file/đường dẫn kỹ thuật, (3) Ngôn ngữ tệp khán giả mục tiêu, (4) Thuật ngữ bắt buộc không có từ Việt tương đương |
| 4 | **Áp dụng khi cập nhật skill khác** | Khi dùng skill `playbook-skill-updater` → cũng Việt hoá |

**✅ Đúng:** "Chạy Luồng Nhanh rồi kiểm tra chéo tác dụng phụ."
**❌ Sai:** "Chạy Fast Track rồi cross-check side-effect." (lẫn 3 thuật ngữ Anh)

### Bảng Việt hoá thuật ngữ phổ biến

| Tiếng Anh | Tiếng Việt |
|-----------|-----------|
| Workflow | Quy trình |
| Template | Khuôn mẫu |
| Checklist | Bảng kiểm tra |
| Framework | Khung phân tích |
| Guardrail | Rào chắn |
| Pattern / Anti-pattern | Mẫu / Mẫu sai |
| Side-effect | Tác dụng phụ |
| Cross-check | Kiểm tra chéo |
| Root cause / Symptom | Nguyên nhân gốc / Triệu chứng |
| Scope creep | Phình phạm vi |
| Pointer | Đường dẫn trỏ |
| Gate | Cổng duyệt |
| Trigger phrase | Câu kích hoạt |
| Sub-task | Nhiệm vụ con |
| Roadmap | Lộ trình |
| Naming convention | Quy ước đặt tên |
