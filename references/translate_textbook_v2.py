"""
translate_textbook_v2.py — แปลตำราขนาดใหญ่ด้วย Claude API
รองรับ: resume จาก checkpoint, rate limiting, QC อัตโนมัติ
รองรับเพิ่ม: PDF ที่สมการเป็น image (detect + rasterize + LaTeX)
"""

try:
    import anthropic
except ModuleNotFoundError:
    anthropic = None
import base64, json, os, re, subprocess, sys, time
from pathlib import Path

# ──────────────────────────────────────────────
# 1. CONFIG
# ──────────────────────────────────────────────
_client = None

def get_client():
    """สร้าง Anthropic client แบบ lazy เพื่อให้ import/help/test ได้แม้ยังไม่ได้ตั้ง API key"""
    global _client
    if _client is not None:
        return _client
    if anthropic is None:
        raise RuntimeError("ไม่พบ package anthropic: ติดตั้งด้วย `pip install anthropic`")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ไม่พบ ANTHROPIC_API_KEY: ตั้งค่าก่อนรัน เช่น export ANTHROPIC_API_KEY='...' ")
    _client = anthropic.Anthropic(api_key=api_key)
    return _client

def is_rate_limit_error(exc: Exception) -> bool:
    return anthropic is not None and isinstance(exc, getattr(anthropic, "RateLimitError", ()))

MODEL_TEXT  = "claude-sonnet-4-6"   # แปลข้อความ — เร็ว คุ้มค่า
MODEL_IMAGE = "claude-sonnet-4-6"   # อ่านสมการจากภาพ (vision)
TEMP        = 0.2
MAX_TOKENS  = 8192
DELAY_SEC   = 1.5
MAX_WORDS   = 1800

CHECKPOINT  = Path("checkpoint.json")
OUT_DIR     = Path("translated")
IMG_DIR     = Path("page_images")   # เก็บภาพหน้าที่ rasterize
OUT_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

# ──────────────────────────────────────────────
# 2. ตรวจสอบ PDF ว่าสมการเป็น image หรือ text
# ──────────────────────────────────────────────
def detect_equation_type(pdf_path: str) -> str:
    """
    คืนค่า 'image' หรือ 'text'
    ตรวจโดยดู encoding ของ font — Identity-H = สมการเป็น image เสมอ
    """
    try:
        result = subprocess.run(
            ["pdffonts", pdf_path],
            capture_output=True, text=True, timeout=30
        )
        if "Identity-H" in result.stdout:
            return "image"
        # ทดสอบเพิ่มเติม: ดึงข้อความหน้าแรก ถ้าสมการหาย → image
        text_result = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "1", pdf_path, "-"],
            capture_output=True, text=True, timeout=30
        )
        # ถ้า extract ได้ text แต่ไม่มีสัญลักษณ์คณิตศาสตร์ → สมการเป็น image
        has_math = bool(re.search(r'[=+\-×÷∑∫√±≤≥αβγδεζηθλμπσωΓΔΩ]', text_result.stdout))
        return "text" if has_math else "image"
    except Exception:
        return "image"  # safe default


# ──────────────────────────────────────────────
# 3. RASTERIZE หน้า PDF → JPEG
# ──────────────────────────────────────────────
def rasterize_page(pdf_path: str, page_num: int, dpi: int = 150) -> Path | None:
    """แปลงหน้า PDF เป็น JPEG สำหรับให้ Claude อ่าน"""
    prefix = IMG_DIR / f"page"
    out_pattern = IMG_DIR / f"page-{page_num:04d}.jpg"

    if out_pattern.exists():
        return out_pattern  # ใช้ cache

    try:
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", str(dpi),
             "-f", str(page_num), "-l", str(page_num),
             pdf_path, str(prefix)],
            capture_output=True, timeout=60, check=True
        )
        # pdftoppm ตั้งชื่อตามจำนวนหน้าทั้งหมด — หาไฟล์จริง
        matches = sorted(IMG_DIR.glob(f"page-*.jpg"))
        # หาไฟล์ที่ตรงกับหน้าที่ต้องการ
        for f in matches:
            num_str = f.stem.replace("page-", "")
            if int(num_str) == page_num:
                return f
        return matches[-1] if matches else None
    except Exception as e:
        print(f"    ⚠️  rasterize หน้า {page_num} ล้มเหลว: {e}")
        return None


# ──────────────────────────────────────────────
# 4. อ่านสมการจากภาพ → LaTeX
# ──────────────────────────────────────────────
def extract_equations_from_image(img_path: Path) -> str:
    """ส่งภาพให้ Claude อ่าน แล้วดึงสมการเป็น LaTeX"""
    img_data = base64.standard_b64encode(img_path.read_bytes()).decode("utf-8")

    response = get_client().messages.create(
        model=MODEL_IMAGE,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": img_data
                    }
                },
                {
                    "type": "text",
                    "text": """จากภาพหน้าหนังสือวิศวกรรมนี้ ให้:
1. ดึงสมการทุกสมการออกมาเป็น LaTeX (ครอบด้วย $...$ หรือ $$...$$)
2. ดึงข้อความบรรยายที่อยู่รอบสมการ (ภาษาอังกฤษ)
3. คงหมายเลขสมการ (1.1), (1.2) ฯลฯ ไว้

รูปแบบที่ต้องการ:
[ข้อความก่อนสมการ]
$$สมการ LaTeX$$ (หมายเลข)
[ข้อความหลังสมการ]

ส่งคืนเฉพาะเนื้อหาที่ดึงได้ ไม่มีคำอธิบายเพิ่มเติม"""
                }
            ]
        }]
    )
    return response.content[0].text


# ──────────────────────────────────────────────
# 5. SYSTEM PROMPT (รวม glossary ถ้ามี)
# ──────────────────────────────────────────────
def build_system_prompt(glossary_path: str = None) -> str:
    base = """คุณเป็นนักแปลวิชาการผู้เชี่ยวชาญ แปลตำราวิศวกรรมไฟฟ้า/อิเล็กทรอนิกส์
ภาษาอังกฤษ → ภาษาวิชาการไทย โดยยึดหลักดังนี้:

1. ใช้ศัพท์บัญญัติราชบัณฑิตยสภาเสมอ ตามรายการใน GLOSSARY ที่ให้ไว้
2. คงสมการ LaTeX ไว้ทุกตัว ($$...$$) ห้ามแปลหรือแก้ไข
3. หัวข้อบท: แปลเป็นไทย + คงอังกฤษในวงเล็บ
4. ครั้งแรกที่พบศัพท์เทคนิค: "ภาษาไทย (English)" ครั้งต่อไปใช้ไทยอย่างเดียว
5. รักษาจำนวนย่อหน้าและโครงสร้างเดิมทุกประการ
6. ตัวอย่างคำนวณ: "Given:" → "กำหนดให้:" | "Solution:" → "วิธีทำ:"
7. อ้างอิงรูป: "Figure X.Y" → "รูปที่ X.Y" | สมการ: "Eq. (X.Y)" → "สมการที่ (X.Y)"
8. ห้ามเพิ่มหรือตัดเนื้อหา — แปลตรงๆ ไม่ตีความเพิ่ม

ส่งคืนเฉพาะเนื้อหาที่แปลแล้ว ไม่มีคำอธิบายเพิ่มเติม"""

    if glossary_path and Path(glossary_path).exists():
        glossary = Path(glossary_path).read_text(encoding="utf-8")
        # ดึงเฉพาะตารางศัพท์ (ไม่เอา style guide ทั้งหมด เพื่อประหยัด token)
        lines = [l for l in glossary.split('\n')
                 if '|' in l and '---' not in l and l.strip()]
        term_table = '\n'.join(lines[:120])  # จำกัด 120 แถว
        base += f"\n\n---\nGLOSSARY (ใช้คำเหล่านี้เท่านั้น):\n{term_table}"

    return base


# ──────────────────────────────────────────────
# 6. SPLIT เนื้อหาเป็น CHUNKS พร้อม ID และ overlap
# ──────────────────────────────────────────────
def split_into_chunks(text: str, chapter_id: str = "CH00",
                      max_words: int = MAX_WORDS) -> list[dict]:
    """
    แบ่งตาม heading, ใส่ Chunk ID (CH01-S001), ใส่ overlap 2 ย่อหน้า
    """
    parts = re.split(r'(\n?#{1,3} [^\n]+)', text)
    raw_chunks, current, heading = [], "", ""

    for part in parts:
        if re.match(r'\n?#{1,3} ', part):
            if current.strip():
                raw_chunks.append({"heading": heading, "text": current.strip()})
            heading, current = part.strip(), part + "\n"
        else:
            current += part
            if len(current.split()) > max_words:
                raw_chunks.append({"heading": heading, "text": current.strip()})
                current = ""
    if current.strip():
        raw_chunks.append({"heading": heading, "text": current.strip()})

    # ใส่ Chunk ID และ overlap (2 ย่อหน้าสุดท้ายของ chunk ก่อนหน้า)
    chunks = []
    for i, rc in enumerate(raw_chunks):
        chunk_id = f"{chapter_id}-S{i+1:03d}"
        overlap = ""
        if i > 0:
            prev_paras = [p for p in raw_chunks[i-1]["text"].split('\n\n') if p.strip()]
            overlap = '\n\n'.join(prev_paras[-2:]) if len(prev_paras) >= 2 else prev_paras[-1] if prev_paras else ""

        chunks.append({
            "id":      chunk_id,
            "seq":     i,
            "heading": rc["heading"],
            "text":    rc["text"],
            "overlap": overlap   # ส่งไปใน prompt เพื่อ context ไม่แปลซ้ำ
        })
    return chunks


# ──────────────────────────────────────────────
# 7. TRANSLATE 1 CHUNK (text mode)
# ──────────────────────────────────────────────
def translate_chunk(chunk: dict, system_prompt: str) -> str:
    overlap_note = ""
    if chunk["overlap"]:
        overlap_note = f"""[บริบทจาก chunk ก่อนหน้า — อ่านเพื่อเข้าใจบริบทเท่านั้น ห้ามแปลซ้ำ]
{chunk['overlap']}
[สิ้นสุดบริบท]

"""

    user_msg = f"""Chunk ID: {chunk['id']}
หัวข้อ: {chunk['heading']}

{overlap_note}===เนื้อหาที่ต้องแปล===
{chunk['text']}
======================"""

    response = get_client().messages.create(
        model=MODEL_TEXT,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=MAX_TOKENS,
        temperature=TEMP,
    )
    return response.content[0].text


# ──────────────────────────────────────────────
# 8. TRANSLATE PAGE (image mode — สำหรับ PDF ที่สมการเป็น image)
# ──────────────────────────────────────────────
def translate_page_with_image(pdf_path: str, page_num: int,
                               system_prompt: str, chunk_id: str,
                               return_raw: bool = False) -> str | tuple[str, str]:
    """
    สำหรับหน้าที่สมการเป็น image:
    1. rasterize หน้า
    2. ดึงสมการ + ข้อความดิบจากภาพ
    3. แปลข้อความ คงสมการ LaTeX ไว้
    """
    print(f"    📸 rasterize หน้า {page_num}...")
    img_path = rasterize_page(pdf_path, page_num)
    if not img_path:
        err = f"[ERROR: ไม่สามารถ rasterize หน้า {page_num}]"
        return (err, "") if return_raw else err

    print(f"    🔢 ดึงสมการจากภาพ...")
    raw_content = extract_equations_from_image(img_path)

    print(f"    🌐 แปลเนื้อหา...")
    user_msg = f"""Chunk ID: {chunk_id}
เนื้อหาต่อไปนี้ดึงมาจากหน้าหนังสือ (มีสมการ LaTeX อยู่แล้ว):

{raw_content}

กฎพิเศษ:
- สมการที่อยู่ใน $$...$$ หรือ $...$ ห้ามแก้ไขเด็ดขาด
- แปลเฉพาะข้อความบรรยายภาษาอังกฤษ → ภาษาไทย
- คงหมายเลขสมการ (X.Y) ไว้"""

    response = get_client().messages.create(
        model=MODEL_TEXT,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=MAX_TOKENS,
        temperature=TEMP,
    )
    translated = response.content[0].text
    return (translated, raw_content) if return_raw else translated


# ──────────────────────────────────────────────
# 9. QC อัตโนมัติ (ขยายจาก v1)
# ──────────────────────────────────────────────
def qc_check(chunk_id: str, src: str, trs: str,
             eq_mode: str = "text") -> list[str]:
    issues = []

    # ตรวจย่อหน้า
    sp = [p for p in src.split('\n\n') if p.strip()]
    tp = [p for p in trs.split('\n\n') if p.strip()]
    if abs(len(sp) - len(tp)) > 2:
        issues.append(f"ย่อหน้าไม่ตรง: ต้นฉบับ {len(sp)} vs แปล {len(tp)}")

    # ตรวจสมการ LaTeX (mode: text)
    if eq_mode == "text":
        for eq in re.findall(r'\$[^$]+\$|\$\$[^$]+\$\$', src):
            if eq not in trs:
                issues.append(f"สมการหาย: {eq[:40]}")

    # ตรวจสมการ LaTeX (mode: image — ตรวจว่ายังมี $$ อยู่)
    if eq_mode == "image":
        src_eq_count = len(re.findall(r'\$\$[^$]+\$\$|\$[^$]+\$', src))
        trs_eq_count = len(re.findall(r'\$\$[^$]+\$\$|\$[^$]+\$', trs))
        if src_eq_count > 0 and trs_eq_count == 0:
            issues.append("สมการ LaTeX หายหมด — อาจถูกแปลหรือลบออก")
        elif trs_eq_count < src_eq_count * 0.7:
            issues.append(f"สมการน้อยกว่าต้นฉบับ: คาด {src_eq_count} พบ {trs_eq_count}")

    # ตรวจ citation
    for cite in re.findall(r'\[\d+\]', src):
        if cite not in trs:
            issues.append(f"citation หาย: {cite}")

    # ตรวจภาษาไทย
    thai = len(re.findall(r'[\u0e00-\u0e7f]', trs))
    if (total := len(trs)) and thai / total < 0.15:
        issues.append("เนื้อหาไม่ได้แปลเป็นไทย (<15%)")

    # ตรวจ AI เติมเอง (ถ้า output ยาวกว่า src มากผิดปกติ)
    src_words = len(src.split())
    trs_words = len(trs.split())
    if trs_words > src_words * 1.8:
        issues.append(f"ผลแปลยาวผิดปกติ ({trs_words} vs {src_words} คำ) — อาจมีเนื้อหาเพิ่ม")

    return issues


# ──────────────────────────────────────────────
# 10. MAIN (text mode)
# ──────────────────────────────────────────────
def translate_text_book(input_file: str, glossary_path: str = None,
                         chapter_id: str = "CH00"):
    """โหมดปกติ — input เป็น .md หรือ .txt"""
    src_text = Path(input_file).read_text(encoding="utf-8")
    system_prompt = build_system_prompt(glossary_path)
    chunks = split_into_chunks(src_text, chapter_id=chapter_id)
    total  = len(chunks)
    print(f"📚 {chapter_id}: {total} chunks จาก {input_file}")

    done: dict = {}
    if CHECKPOINT.exists():
        done = json.loads(CHECKPOINT.read_text()).get("done", {})
        already = sum(1 for c in chunks if c["id"] in done)
        print(f"↪️  resume: {already}/{total} chunks แปลไปแล้ว")

    qc_log = []
    for chunk in chunks:
        cid = chunk["id"]
        out_path = OUT_DIR / f"{cid}.md"

        if cid in done:
            continue

        print(f"  🔄 {cid}: {chunk['heading'][:50]}")
        try:
            translated = translate_chunk(chunk, system_prompt)
        except Exception as e:
            if not is_rate_limit_error(e):
                raise
            print("  ⚠️  Rate limit — รอ 60 วิ")
            time.sleep(60)
            translated = translate_chunk(chunk, system_prompt)

        issues = qc_check(cid, chunk["text"], translated, eq_mode="text")
        if issues:
            qc_log.append({"chunk": cid, "issues": issues})
            print(f"  ⚠️  QC: {issues}")

        out_path.write_text(translated, encoding="utf-8")
        done[cid] = True
        cp = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
        cp["done"] = done
        CHECKPOINT.write_text(json.dumps(cp, ensure_ascii=False, indent=2))
        time.sleep(DELAY_SEC)

    _merge_and_report(chunks, qc_log, chapter_id)


# ──────────────────────────────────────────────
# 11. MAIN (image mode — PDF ที่สมการเป็น image)
# ──────────────────────────────────────────────
def translate_pdf_image_mode(pdf_path: str, start_page: int, end_page: int,
                              glossary_path: str = None, chapter_id: str = "CH00"):
    """
    โหมด image — สำหรับ PDF ที่สมการเป็น image (Identity-H font)
    แปลทีละหน้า: rasterize → extract equations → translate
    """
    system_prompt = build_system_prompt(glossary_path)
    total = end_page - start_page + 1
    print(f"📸 {chapter_id}: image mode หน้า {start_page}–{end_page} ({total} หน้า)")
    page_chunks = [
        {"id": f"{chapter_id}-P{p:04d}", "seq": p - start_page, "heading": "", "text": "", "overlap": ""}
        for p in range(start_page, end_page + 1)
    ]

    done: dict = {}
    if CHECKPOINT.exists():
        done = json.loads(CHECKPOINT.read_text()).get("done", {})
        already = sum(1 for k in done if k.startswith(chapter_id))
        print(f"↪️  resume: {already}/{total} หน้าแปลไปแล้ว")

    qc_log = []
    for page_num in range(start_page, end_page + 1):
        cid = f"{chapter_id}-P{page_num:04d}"
        out_path = OUT_DIR / f"{cid}.md"

        if cid in done:
            print(f"  ⏭  {cid} ข้ามแล้ว")
            continue

        print(f"  🔄 {cid} (หน้า {page_num}/{end_page})")
        try:
            translated, raw_content = translate_page_with_image(pdf_path, page_num,
                                                                 system_prompt, cid,
                                                                 return_raw=True)
        except Exception as e:
            if not is_rate_limit_error(e):
                raise
            print("  ⚠️  Rate limit — รอ 60 วิ")
            time.sleep(60)
            translated, raw_content = translate_page_with_image(pdf_path, page_num,
                                                                 system_prompt, cid,
                                                                 return_raw=True)

        issues = qc_check(cid, raw_content, translated, eq_mode="image")
        if issues:
            qc_log.append({"chunk": cid, "issues": issues})
            print(f"  ⚠️  QC: {issues}")

        out_path.write_text(translated, encoding="utf-8")
        done[cid] = True
        cp = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
        cp["done"] = done
        CHECKPOINT.write_text(json.dumps(cp, ensure_ascii=False, indent=2))
        time.sleep(DELAY_SEC * 2)   # image mode ช้ากว่า — หน่วงเพิ่ม

    _merge_and_report(page_chunks, qc_log, chapter_id)


# ──────────────────────────────────────────────
# 12. MERGE + REPORT
# ──────────────────────────────────────────────
def _merge_and_report(chunks, qc_log, chapter_id):
    print(f"\n✅ รวมไฟล์ {chapter_id}...")
    parts = []
    for chunk in sorted(chunks, key=lambda c: c["seq"]):
        p = OUT_DIR / f"{chunk['id']}.md"
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))

    out_file = Path(f"{chapter_id}_translated.md")
    out_file.write_text("\n\n---\n\n".join(parts), encoding="utf-8")

    if qc_log:
        qc_file = Path(f"{chapter_id}_qc_report.json")
        qc_file.write_text(json.dumps(qc_log, ensure_ascii=False, indent=2))
        print(f"⚠️  พบปัญหา QC ใน {len(qc_log)} chunks → {qc_file}")
    else:
        print("✅ QC ผ่านทุก chunk!")

    print(f"📄 ไฟล์รวม: {out_file}")


# ──────────────────────────────────────────────
# 13. ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    """
    ใช้งาน:
      # Text mode (MD/TXT input):
      python translate_textbook_v2.py text chapter1.md --chapter CH01 --glossary glossary.md

      # Image mode (PDF input ที่สมการเป็น image):
      python translate_textbook_v2.py image book.pdf 22 80 --chapter CH01 --glossary glossary.md

      # Auto detect จาก PDF:
      python translate_textbook_v2.py auto book.pdf 22 80 --chapter CH01 --glossary glossary.md
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",    choices=["text", "image", "auto"])
    parser.add_argument("input",   help="ไฟล์ .md/.txt หรือ .pdf")
    parser.add_argument("start",   nargs="?", type=int, help="หน้าเริ่ม (image/auto mode)")
    parser.add_argument("end",     nargs="?", type=int, help="หน้าสิ้นสุด (image/auto mode)")
    parser.add_argument("--chapter",  default="CH00")
    parser.add_argument("--glossary", default=None)
    args = parser.parse_args()

    if args.mode == "text":
        translate_text_book(args.input, args.glossary, args.chapter)

    elif args.mode == "image":
        if not args.start or not args.end:
            print("image mode ต้องระบุ start และ end page")
            sys.exit(1)
        translate_pdf_image_mode(args.input, args.start, args.end,
                                  args.glossary, args.chapter)

    elif args.mode == "auto":
        if not args.start or not args.end:
            print("auto mode ต้องระบุ start และ end page")
            sys.exit(1)
        eq_type = detect_equation_type(args.input)
        print(f"🔍 ตรวจสอบ PDF: สมการเป็น [{eq_type}]")
        if eq_type == "image":
            translate_pdf_image_mode(args.input, args.start, args.end,
                                      args.glossary, args.chapter)
        else:
            # แปลง PDF เป็น text ก่อน แล้วใช้ text mode
            txt_out = f"{args.chapter}_raw.txt"
            subprocess.run(["pdftotext", "-layout",
                            "-f", str(args.start), "-l", str(args.end),
                            args.input, txt_out])
            translate_text_book(txt_out, args.glossary, args.chapter)
