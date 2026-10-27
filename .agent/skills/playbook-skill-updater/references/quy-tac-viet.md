# Quy Tắc Viết Khi SỬA Skill + Ví Dụ Đúng/Sai

> File này phục vụ **Pha U3** (Thực thi).
> Kế thừa từ `playbook-skill-creator/references/quy-tac-viet.md` + bổ sung quy tắc SỬA.
>
> 📌 Quy tắc viết CHUNG (phần mô tả, 7 phần chuẩn, phong cách, references/, templates/):
> → Xem `.claude/skills/playbook-skill-creator/references/quy-tac-viet.md`
> File này chỉ bổ sung quy tắc RIÊNG cho việc SỬA.

---

## §1. GIỮ QUY ƯỚC TIÊU ĐỀ GỐC

**Quy tắc:** Giữ nguyên H1/H2/H3 + quy ước đánh số gốc.

**✅ Đúng — Giữ quy ước, chỉ đổi số:**
```markdown
# Gốc:     ## B. 2 PHONG CÁCH THỊ GIÁC
# Sau sửa: ## B. 3 PHONG CÁCH THỊ GIÁC (từ Dream100 + USP Single Dad)
```

**❌ Sai — Đổi quy ước:**
```markdown
# Gốc:     ## B. 2 PHONG CÁCH THỊ GIÁC
# Sau sửa: ## §2. BA PHONG CÁCH THỊ GIÁC
```
→ Đổi "B." → "§2.", đổi số → chữ. Phá quy ước.

**Thêm phần mới:**
- Đánh số TIẾP (§5 sau §4), KHÔNG chèn giữa
- Nếu xóa phần → đánh số lại phần sau
- Giữ cùng quy ước (nếu gốc dùng §A/§B → mới cũng dùng §)

---

## §2. GIỮ QUY ƯỚC ĐẶT TÊN GỐC

| Gốc dùng | File mới dùng |
|-----------|--------------| 
| Tiếng Việt (`boc-tach-dna-viral.md`) | Tiếng Việt |
| viết-liền-bằng-gạch-ngang | viết-liền-bằng-gạch-ngang |
| Có tiền tố (`story-us-`) | Có tiền tố |

**❌ Sai:**
```
# Gốc: references/quy-tac-tai-tao.md
# Mới: references/zetlag_rules_v2.md    → Sai quy ước (gạch dưới, tiếng Anh, phiên bản)
```

---

## §3. GIỮ GIỌNG VĂN GỐC

| Gốc viết | Sửa phải |
|----------|----------|
| Trang trọng (bảng, tiêu đề rõ) | Trang trọng |
| Gạch đầu dòng | Gạch đầu dòng (không đổi sang đoạn văn) |
| Thể mệnh lệnh | Thể mệnh lệnh |
| Có ví dụ Đúng/Sai | Có ví dụ Đúng/Sai |

---

## §4. SỬA CÓ CHỌN LỌC — KHÔNG VIẾT LẠI TOÀN BỘ

**✅ Đúng — Sửa đúng chỗ cần sửa:**
```markdown
# Chỉ đổi dòng 203:
- Trước: | 12 | **Grace/Marcus nhìn thấy → có bấm không?** |
- Sau:   | 12 | **Sarah/David nhìn thấy → có bấm không?** |
```

**❌ Sai — Viết lại toàn bộ phần:**
```markdown
# Xóa phần E (12 câu), viết lại hoàn toàn 12 câu mới
→ Mất nội dung gốc đang đúng. Chỉ cần sửa 1 dòng.
```

---

## §5. TÌM TOÀN BỘ KHI ĐỔI THUẬT NGỮ

**Quy tắc:** Khi đổi thuật ngữ / tên nhân vật / đường dẫn → tìm TOÀN BỘ skill → đổi TẤT CẢ file.

**Quy trình:**
```
1. Xác định từ cần đổi: "Grace" → "Sarah"
2. Tìm "Grace" trong toàn thư mục skill
3. Liệt kê TẤT CẢ kết quả (file + dòng)
4. Đổi từng kết quả
5. Tìm lại → phải = 0 kết quả
```

**❌ Sai:**
```
Đổi "Grace" → "Sarah" trong SKILL.md
Quên đổi trong references/chien-luoc-concept.md dòng 161
→ Mâu thuẫn giữa 2 file
```

---

## §6. KHÔNG THÊM FILE MỚI NGOÀI KẾ HOẠCH

**Quy tắc:** Chỉ thêm/xóa file nếu kế hoạch Pha U2 ghi rõ.

**Đặc biệt CẤM tạo:**
- README.md
- CHANGELOG.md
- NOTES.md
- INSTALLATION_GUIDE.md
- Bất kỳ file không có trong kế hoạch

---

## §7. NHÃN NGUỒN KHI THÊM NỘI DUNG MỚI

Khi thêm nội dung mới vào skill (VD: thêm bảng, thêm ví dụ), gắn nhãn nguồn:

| Nhãn | Khi nào |
|------|---------|
| `[📊 Tên nguồn]` | Số liệu từ dữ liệu thật |
| `[📌 Tên nguồn]` | Trích dẫn từ tài liệu thật |
| `[⚠️ Giả thuyết]` | AI tự suy luận |
| `[✅ User chốt]` | User xác nhận |

> Không thêm nội dung mới mà không có nhãn nguồn.
> (Vì nội dung không nhãn = AI bịa → ảo giác)

---

## §8. GIỚI HẠN DÒNG SKILL.md

**Khuyến nghị:** SKILL.md NÊN ≤ 150 dòng. Không bắt buộc.

| Tình huống | Hành động |
|-----------|-----------|
| SKILL.md ≤ 150 dòng | ✅ Bình thường |
| SKILL.md 150-200 dòng | ⚠️ Xem xét: có nội dung nào nên chuyển sang references/? |
| SKILL.md > 200 dòng | 🔴 Nên tách: chuyển kiến thức chuyên sâu sang references/ |

(Vì SKILL.md dài = AI phải đọc nhiều mỗi lần kích hoạt → chậm + dễ bỏ sót. Nhưng có skill phức tạp ĐÚNG cần > 150 dòng — nên đây là khuyến nghị, không phải luật cứng.)

---

## §9. VIỆT HOÁ

**Quy tắc:**
- Toàn bộ nội dung viết bằng **tiếng Việt**.
- Thuật ngữ tiếng Anh hoặc chuyên ngành → **dịch sang tiếng Việt + giải thích ngay lần đầu xuất hiện**.
- Ngôn ngữ đơn giản, tránh thuật ngữ khó hiểu không cần thiết.
- KHÔNG viết lẫn lộn ngôn ngữ (kiểu tiếng Anh không ra Anh, Việt không ra Việt).

**Ngoại lệ — giữ nguyên ngôn ngữ gốc khi:**
1. Tên riêng (người, công ty, kênh YouTube)
2. Tên file, đường dẫn kỹ thuật (vì hệ thống file yêu cầu)
3. Ngôn ngữ gốc của tệp khán giả mục tiêu (VD: từ khoá tiếng Hàn cho kênh Hàn Quốc)
4. Thuật ngữ chuyên môn bắt buộc không có từ Việt tương đương (hiếm — phải chứng minh)

**✅ Đúng:** "Tư duy gốc rễ (phân tích từ nguyên lý nền tảng, không sao chép mù)"
**❌ Sai:** "Apply First Principles thinking with skeleton retention ratio"
**❌ Sai:** "Chạy Fast Track rồi cross-check side-effect" (lẫn lộn 3 thuật ngữ Anh)

---

## §10. QUY TẮC PHÂN BỔ THAM CHIẾU (CHỐNG MỒ CÔI)

**Quy tắc:** Đảm bảo "Đọc đúng file đúng lúc", không gom việc đọc hướng dẫn vào cuối quy trình.

| Tình huống | Cách xử lý |
|-----------|-----------|
| Bảng kiểm tra có nhiều mục cho nhiều Pha | Chia nhỏ lệnh đọc: Pha 1 đọc phần của Pha 1, Pha 2 đọc phần của Pha 2. Không dồn đọc tất cả vào Pha cuối. |
| File tham chiếu chứa hướng dẫn thực hành | Lệnh đọc file phải đặt ở chính xác Pha mà hành động đó diễn ra, không đặt ở Pha Bóc Tách/Chuẩn bị. |
| Cập nhật skill cũ bị lỗi mồ côi | Nhận diện nội dung thừa ở các file tham chiếu hiện tại và cấu trúc lại lệnh đọc (read trigger) trong SKILL.md. |

---

## §11. QUY TẮC DỪNG CỨNG

**Quy tắc:** Khi nâng cấp quy trình hoặc thêm Pha/Nhiệm vụ con, **BẮT BUỘC** phải rào chắn việc chạy một mạch.

- **Với các Pha:** "DỪNG CỨNG Ở MỖI PHA. Sau mỗi Pha bắt buộc phải DỪNG để user duyệt. CẤM TUYỆT ĐỐI tự ý chạy một mạch hết các Pha."
- **Với Nhiệm vụ con:** "Chạy xong 1 nhiệm vụ con → DỪNG để user duyệt. Cấm chạy một lúc nhiều nhiệm vụ con."
