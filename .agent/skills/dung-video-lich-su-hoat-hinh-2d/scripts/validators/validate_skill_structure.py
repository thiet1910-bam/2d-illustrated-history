#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trình Kiểm Toán Tự Động Cấu Trúc & Mật Độ Nội Dung Skill (Universal Skill Validator)
Dùng chung cho cả `playbook-skill-creator` và `playbook-skill-updater`.
Kiểm tra cả VỎ CẤU TRÚC (YAML, giới hạn dòng, lệnh đọc StartLine-EndLine, cú pháp code)
lẫn RUỘT BẢN CHẤT (Tách bạch 3 tầng, không rò rỉ link ngoài, mật độ bảng/ví dụ trong references/, khuôn mẫu sạch).

Cú pháp:
  python .agent/skills/playbook-skill-creator/scripts/validate_skill_structure.py "<duong_dan_thu_muc_skill>"
"""

import ast
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

FORBIDDEN_ROOT_FILES = {"readme.md", "changelog.md", "installation_guide.md", "install.md"}
BANNED_TEMPLATE_PHRASES = [
    "← cố định",
    "← thay đổi",
    "hãy viết ",
    "hãy chọn ",
    "đừng viết ",
    "lưu ý khi điền:",
]


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, "SKILL.md không bắt đầu bằng khối YAML `---`."
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "Khối YAML mở đầu trong SKILL.md chưa được đóng bằng `---`."
    yaml_text = parts[1].strip()
    keys = []
    name_val = ""
    desc_val = ""
    current_key = None
    for line in yaml_text.splitlines():
        m = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            keys.append(key)
            current_key = key
            if key == "name":
                name_val = val.strip("\"'")
            elif key == "description":
                desc_val = val + "\n"
        elif current_key == "description":
            desc_val += line + "\n"
    return {"keys": keys, "name": name_val, "description": desc_val.strip()}, None


def validate_skill(skill_dir: Path) -> int:
    errors = []
    warnings = []

    if not skill_dir.exists() or not skill_dir.is_dir():
        print(f"❌ [FAIL] Thư mục skill không tồn tại: {skill_dir}")
        return 1

    skill_name = skill_dir.name

    # 1. Kiểm tra file thừa bị cấm
    for item in skill_dir.iterdir():
        if item.is_file() and item.name.lower() in FORBIDDEN_ROOT_FILES:
            errors.append(f"Chứa file phụ trợ bị cấm: `{item.name}` (Cần xóa bỏ).")

    # 2. Kiểm tra SKILL.md tồn tại & giới hạn dòng
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ [FAIL] Thiếu file bắt buộc `SKILL.md` trong `{skill_dir}`.")
        return 1

    skill_text = skill_md.read_text(encoding="utf-8")
    skill_lines = skill_text.splitlines()
    if len(skill_lines) > 150:
        errors.append(
            f"`SKILL.md` dài {len(skill_lines)} dòng (Vượt quá giới hạn tối đa 150 dòng của Bộ điều hướng)."
        )

    # 3. Kiểm tra YAML Frontmatter
    fm, fm_err = parse_frontmatter(skill_text)
    if fm_err:
        errors.append(fm_err)
    else:
        allowed_keys = {"name", "description"}
        extra_keys = set(fm["keys"]) - allowed_keys
        if extra_keys:
            errors.append(f"YAML chứa trường thừa bị cấm: {sorted(extra_keys)} (Chỉ được phép có `name` và `description`).")
        if "name" not in fm["keys"] or not fm["name"]:
            errors.append("YAML thiếu trường `name`.")
        else:
            if fm["name"] != skill_name:
                errors.append(f"Trường `name: {fm['name']}` không khớp với tên thư mục `{skill_name}`.")
            if not re.match(r"^[a-z0-9-]+$", fm["name"]) or len(fm["name"]) >= 64:
                errors.append(f"Trường `name: {fm['name']}` phải viết thường gạch ngang (kebab-case) và < 64 ký tự.")
        if "description" not in fm["keys"] or not fm["description"]:
            errors.append("YAML thiếu trường `description`.")
        else:
            desc_lower = fm["description"].lower()
            if "kích hoạt:" not in desc_lower and "trigger:" not in desc_lower:
                errors.append("Trường `description` thiếu dòng từ khóa kích hoạt (`Kích hoạt: /...` hoặc `Trigger: /...`).")

    # 4. Kiểm tra thư mục references/ (Lệnh đọc phẫu thuật, không mồ côi, tự chủ, Ruột Đặc)
    ref_dir = skill_dir / "references"
    if ref_dir.exists() and ref_dir.is_dir():
        ref_files = sorted(ref_dir.rglob("*.md"))
        if ref_files:
            has_line_pointers = ("StartLine" in skill_text and "EndLine" in skill_text) or bool(
                re.search(r"dòng\s+\d+\s*[-–→]\s*\d+", skill_text, re.IGNORECASE)
            )
            if not has_line_pointers:
                errors.append(
                    "`SKILL.md` thiếu Lệnh đọc phẫu thuật chỉ rõ khoảng dòng (`StartLine: ... -> EndLine: ...`) khi trỏ sang `references/`."
                )

        for rf in ref_files:
            rel_path = rf.relative_to(skill_dir).as_posix()
            rf_name = rf.name
            if rel_path not in skill_text and rf_name not in skill_text:
                errors.append(f"File tham chiếu mồ côi: `{rel_path}` không hề được trỏ tới từ `SKILL.md`.")

            rf_text = rf.read_text(encoding="utf-8")
            rf_lines = rf_text.splitlines()

            # Kiểm tra rò rỉ link file:/// thực tế ra ngoài
            ext_links = re.findall(r"file:///[a-zA-Z0-9_:/\\.-]+", rf_text)
            for link in ext_links:
                if skill_name not in link:
                    errors.append(
                        f"File `{rel_path}` chứa đường dẫn `file:///` trỏ ra ngoài thư mục skill: `{link}` (Vi phạm tính tự chủ 100%)."
                    )

            # Kiểm tra cấu trúc Đầu mục (## )
            headings = [line for line in rf_lines if line.startswith("## ")]
            if not headings:
                errors.append(
                    f"File `{rel_path}` không có Đầu mục cấp 2 (`## ...`) để làm mốc neo cho lệnh đọc theo dòng."
                )

            # Kiểm tra mật độ nội dung ("Ruột Đặc"): Phải có bảng Markdown hoặc cặp Đúng/Sai hoặc số liệu
            has_table = "|" in rf_text and "---" in rf_text
            has_examples = ("✅" in rf_text and "❌" in rf_text)
            if not has_table and not has_examples:
                warnings.append(
                    f"File `{rel_path}` có dấu hiệu 'Rỗng Ruột' (Thiếu cả Bảng quyết định `|...|` lẫn cặp đối chứng `✅/❌`)."
                )

    # 5. Kiểm tra thư mục templates/ (Khung dữ liệu sạch, không lẫn hướng dẫn)
    tpl_dir = skill_dir / "templates"
    if tpl_dir.exists() and tpl_dir.is_dir():
        for tf in sorted(tpl_dir.rglob("*.md")):
            rel_path = tf.relative_to(skill_dir).as_posix()
            tf_text = tf.read_text(encoding="utf-8")
            tf_lower = tf_text.lower()
            for phrase in BANNED_TEMPLATE_PHRASES:
                if phrase in tf_lower:
                    errors.append(
                        f"Khuôn mẫu `{rel_path}` chứa cụm từ hướng dẫn/nhãn kỹ thuật bị cấm (`{phrase}`). Khuôn mẫu đầu ra phải sạch 100%."
                    )

    # 6. Kiểm tra thư mục scripts/ (Cú pháp Python hợp lệ, không phải mã giả)
    scr_dir = skill_dir / "scripts"
    if scr_dir.exists() and scr_dir.is_dir():
        for sf in sorted(scr_dir.rglob("*.py")):
            rel_path = sf.relative_to(skill_dir).as_posix()
            try:
                source = sf.read_text(encoding="utf-8")
                ast.parse(source, filename=str(sf))
            except SyntaxError as exc:
                errors.append(f"Script `{rel_path}` bị lỗi cú pháp Python tại dòng {exc.lineno}: {exc.msg}")

    # Xuất báo cáo kết quả
    print("=" * 72)
    print(f"🔍 KẾT QUẢ KIỂM TOÁN CẤU TRÚC & BẢN CHẤT SKILL: `{skill_name}`")
    print("=" * 72)
    print(f"• Độ dài `SKILL.md`: {len(skill_lines)}/150 dòng")
    if ref_dir.exists():
        print(f"• Số file trong `references/`: {len(list(ref_dir.rglob('*.md')))} file")
    if tpl_dir.exists():
        print(f"• Số file trong `templates/`: {len(list(tpl_dir.rglob('*.*')))} file")
    if scr_dir.exists():
        print(f"• Số file trong `scripts/`: {len(list(scr_dir.rglob('*.py')))} script Python")

    if warnings:
        print("\n⚠️ CẢNH BÁO MẬT ĐỘ NỘI DUNG:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ PHÁT HIỆN {len(errors)} LỖI VI PHẠM CHUẨN KIẾN TRÚC:")
        for idx, err in enumerate(errors, 1):
            print(f"  {idx}. [FAIL] {err}")
        print("=" * 72)
        return 1

    print("\n✅ [PASS 100%] Skill đạt chuẩn tuyệt đối cả về Vỏ Cấu Trúc lẫn Ruột Bản Chất!")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python validate_skill_structure.py <duong_dan_thu_muc_skill>")
        sys.exit(1)
    target = Path(sys.argv[1]).resolve()
    sys.exit(validate_skill(target))
