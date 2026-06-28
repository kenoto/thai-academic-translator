# API Configuration และ Python Script

## การตั้งค่า Claude API

```python
import anthropic
import os

# ตั้งค่า API Key (ใช้ environment variable เสมอ)
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Model ที่แนะนำ
MODEL_TRANSLATE = "claude-sonnet-4-6"   # แปลทั่วไป — เร็ว ราคาสมเหตุ
MODEL_COMPLEX   = "claude-opus-4-6"     # งานซับซ้อน/ยาวมาก — แม่นยำสูงสุด

# Parameter มาตรฐานสำหรับงานแปล
TRANSLATE_PARAMS = {
    "max_tokens": 8192,
    "temperature": 0.2,   # ต่ำ = แม่นยำ สม่ำเสมอ
}
```

---

## ฟังก์ชันแปลหลัก

```python
def translate_chunk(
    source_text: str,
    mode: str = "textbook",        # "textbook" | "research" | "slides"
    section_context: str = "",     # หัวข้อ/บทก่อนหน้า เพื่อ context
    special_rules: str = "",       # กฎพิเศษเพิ่มเติม
    model: str = MODEL_TRANSLATE
) -> str:
    """
    แปลเนื้อหาวิชาการ 1 chunk
    Returns: เนื้อหาภาษาไทย
    """
    
    # โหลด system prompt ตามโหมด
    system_prompt = load_system_prompt(mode)
    
    # สร้าง user prompt
    user_prompt = f"""แปลเนื้อหาต่อไปนี้เป็นภาษาวิชาการไทย ตามหลักราชบัณฑิต:

[บริบท: {section_context}]

===เนื้อหาต้นฉบับ===
{source_text}
=====================

{f"กฎพิเศษ: {special_rules}" if special_rules else ""}

ส่งคืนเฉพาะเนื้อหาที่แปลแล้ว ไม่ต้องมีคำอธิบายเพิ่มเติม"""

    response = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        **TRANSLATE_PARAMS
    )
    
    return response.content[0].text


def load_system_prompt(mode: str) -> str:
    """โหลด system prompt ตามโหมด"""
    prompts = {
        "textbook": SYSTEM_TEXTBOOK,
        "research": SYSTEM_RESEARCH,
        "slides":   SYSTEM_SLIDES,
    }
    return prompts.get(mode, SYSTEM_TEXTBOOK)
```

---

## ฟังก์ชันแปลเอกสารทั้งฉบับ

```python
import re

def translate_document(
    full_text: str,
    mode: str = "textbook",
    max_words_per_chunk: int = 1800
) -> str:
    """
    แปลเอกสารยาว โดยแบ่งตาม heading อัตโนมัติ
    """
    # แบ่งตาม markdown heading
    sections = re.split(r'\n(#{1,3} .+)', full_text)
    
    chunks = []
    current_chunk = ""
    current_heading = ""
    
    for i, part in enumerate(sections):
        if re.match(r'#{1,3} ', part):
            # บันทึก heading ปัจจุบัน
            if current_chunk:
                chunks.append({
                    "heading": current_heading,
                    "text": current_chunk.strip()
                })
            current_heading = part
            current_chunk = part + "\n"
        else:
            current_chunk += part
            # ตรวจสอบความยาว
            if len(current_chunk.split()) > max_words_per_chunk:
                chunks.append({
                    "heading": current_heading,
                    "text": current_chunk.strip()
                })
                current_chunk = ""
    
    if current_chunk:
        chunks.append({"heading": current_heading, "text": current_chunk.strip()})
    
    # แปลทีละ chunk
    translated_parts = []
    prev_heading = ""
    
    for i, chunk in enumerate(chunks):
        print(f"กำลังแปล chunk {i+1}/{len(chunks)}: {chunk['heading'][:50]}...")
        
        translated = translate_chunk(
            source_text=chunk["text"],
            mode=mode,
            section_context=prev_heading,
        )
        translated_parts.append(translated)
        prev_heading = chunk["heading"]
    
    return "\n\n".join(translated_parts)


def validate_translation(source: str, translated: str) -> dict:
    """
    QC อัตโนมัติ — ตรวจสอบปัญหาหลัก
    Returns: dict ของปัญหาที่พบ
    """
    issues = {}
    
    # 1. ตรวจจำนวนย่อหน้า
    src_para = len([p for p in source.split('\n\n') if p.strip()])
    trs_para = len([p for p in translated.split('\n\n') if p.strip()])
    if abs(src_para - trs_para) > 2:
        issues["paragraph_mismatch"] = f"ต้นฉบับ {src_para} ย่อหน้า แต่แปลได้ {trs_para} ย่อหน้า"
    
    # 2. ตรวจสมการ ($ ... $ หรือ $$...$$) ยังอยู่ครบ
    src_eq = re.findall(r'\$[^$]+\$|\$\$[^$]+\$\$', source)
    trs_eq = re.findall(r'\$[^$]+\$|\$\$[^$]+\$\$', translated)
    if len(src_eq) != len(trs_eq):
        issues["equation_count"] = f"สมการในต้นฉบับ {len(src_eq)} แต่แปลได้ {len(trs_eq)}"
    
    # 3. ตรวจ citation ยังอยู่ครบ
    src_cite = re.findall(r'\[\d+\]', source)
    trs_cite = re.findall(r'\[\d+\]', translated)
    if set(src_cite) != set(trs_cite):
        missing = set(src_cite) - set(trs_cite)
        if missing:
            issues["missing_citations"] = f"การอ้างอิงหาย: {missing}"
    
    # 4. ตรวจว่ามีภาษาไทยจริงๆ (ไม่ได้ส่งคืนภาษาอังกฤษมา)
    thai_chars = len(re.findall(r'[\u0e00-\u0e7f]', translated))
    total_chars = len(translated)
    if total_chars > 0 and thai_chars / total_chars < 0.2:
        issues["insufficient_thai"] = "เนื้อหาไม่ได้แปลเป็นไทย (ไทยน้อยกว่า 20%)"
    
    return issues
```

---

## ตัวอย่างการใช้งานจริง

```python
# ตัวอย่าง 1: แปลบทตำรา
with open("chapter3_ac_circuits.md", "r", encoding="utf-8") as f:
    source = f.read()

translated = translate_document(source, mode="textbook")

# ตรวจ QC
issues = validate_translation(source, translated)
if issues:
    print("⚠️ พบปัญหา:", issues)
else:
    print("✅ QC ผ่าน")

with open("chapter3_ac_circuits_TH.md", "w", encoding="utf-8") as f:
    f.write(translated)


# ตัวอย่าง 2: แปลบทความวิจัยทีละส่วน
abstract_en = """This paper presents a comparative analysis..."""

abstract_th = translate_chunk(
    source_text=abstract_en,
    mode="research",
    section_context="Abstract"
)
print(abstract_th)


# ตัวอย่าง 3: ตรวจศัพท์บัญญัติ (Quick Check)
def check_term(term: str) -> str:
    """ถามว่าคำนี้ควรแปลว่าอะไร"""
    response = client.messages.create(
        model=MODEL_TRANSLATE,
        system="""คุณเป็นผู้เชี่ยวชาญศัพท์บัญญัติราชบัณฑิตยสภา สาขาวิศวกรรมไฟฟ้า
        ตอบสั้นๆ: คำบัญญัติ + บริบทการใช้งาน""",
        messages=[{"role": "user", "content": f"คำว่า '{term}' ในวิศวกรรมไฟฟ้าแปลว่าอะไร?"}],
        max_tokens=200,
        temperature=0.1
    )
    return response.content[0].text

# ตัวอย่าง: check_term("impedance matching")
```

---

## หมายเหตุความปลอดภัย

```python
# ✅ ดี — ใช้ environment variable
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# ❌ ห้ามเด็ดขาด — hardcode key
client = anthropic.Anthropic(api_key="sk-ant-xxx...")
```

ตั้งค่าใน terminal:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```
