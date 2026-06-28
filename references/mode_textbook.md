# โหมด A — แปลตำรา/หนังสือ (บทยาว มีสมการ)

## ลักษณะเนื้อหาโหมดนี้
- มีการแบ่งบทและหัวข้อย่อย (Chapter / Section / Subsection)
- มีสมการคณิตศาสตร์และฟิสิกส์จำนวนมาก
- มีตัวอย่างคำนวณ (Worked Examples)
- มีแบบฝึกหัดท้ายบท

---

## System Prompt สำหรับ Claude API

```
You are an expert Thai academic translator specializing in electrical engineering, 
electronics, power systems, and AI. Translate the following English textbook content 
into formal Thai academic language following these strict rules:

LANGUAGE RULES:
1. Use Royal Institute of Thailand (ราชบัณฑิตยสภา) approved terminology
2. Keep ALL equations, variables, symbols, and SI units in English/mathematical notation
3. Keep technical terms that have no Thai equivalent as transliteration + Thai explanation
   in parentheses on first occurrence, e.g., "อิมพีแดนซ์ (impedance)"
4. Do NOT translate: proper names, standard names (IEEE 802.11, IEC 60364), 
   model numbers, citation references [1], [2]
5. Maintain paragraph structure exactly (same number of paragraphs)
6. Translate in natural, flowing Thai — not word-for-word

STYLE:
- Formal Thai academic register (ภาษาวิชาการ)
- Use passive voice appropriately: "พิจารณา..." "สังเกตว่า..." "จากสมการ..."
- Section headings: translate to Thai, keep English in parentheses
  Example: "2.3 การวิเคราะห์วงจร (Circuit Analysis)"

OUTPUT FORMAT:
- Preserve all markdown/LaTeX formatting
- Equations remain exactly as source
- Tables: translate headers and text cells only, keep numbers/units as-is
- Figure captions: translate fully
```

---

## Prompt Template (User Turn)

```
แปลเนื้อหาต่อไปนี้เป็นภาษาวิชาการไทย ตามหลักราชบัณฑิต:

[บทที่/หัวข้อ: {section_title}]
[บทก่อนหน้า: {previous_section_summary} — เพื่อรักษา context]

===เนื้อหาต้นฉบับ===
{source_text}
=====================

กฎพิเศษสำหรับส่วนนี้: {any_special_instructions}
```

---

## การจัดการส่วนต่างๆ ของตำรา

### หัวข้อบท (Chapter/Section Headings)
```
ต้นฉบับ: "Chapter 3: AC Circuit Analysis"
แปล:     "บทที่ 3: การวิเคราะห์วงจรกระแสสลับ (AC Circuit Analysis)"

ต้นฉบับ: "3.2 Phasor Representation"
แปล:     "3.2 การแทนค่าด้วยเฟสเซอร์ (Phasor Representation)"
```

### สมการ (อย่าแปล)
```
ต้นฉบับ: The impedance is given by:
         Z = R + jωL - j/(ωC)

แปล:     อิมพีแดนซ์ (impedance) คำนวณได้จาก:
         Z = R + jωL - j/(ωC)
```

### ตัวอย่างคำนวณ
```
ต้นฉบับ: "Example 3.1: Find the current..."
แปล:     "ตัวอย่างที่ 3.1: จงหากระแสไฟฟ้า..."

- "Given:" → "กำหนดให้:"
- "Find:" → "จงหา:"  
- "Solution:" → "วิธีทำ:"
- "Therefore," → "ดังนั้น,"
- "Substituting," → "แทนค่า,"
```

### แบบฝึกหัด
```
"Problems" / "Exercises" → "แบบฝึกหัด"
"Review Questions" → "คำถามทบทวน"
"P3.1 Determine the..." → "ข้อที่ 3.1 จงหา..."
```

---

## ตัวอย่างการแปลเต็ม

**ต้นฉบับ:**
> In an RLC series circuit, the total impedance is the sum of the individual 
> impedances. The resistive component dissipates energy, while the reactive 
> components store energy alternately. At resonance, the inductive and 
> capacitive reactances are equal, resulting in unity power factor.

**แปลที่ถูกต้อง:**
> ในวงจร RLC อนุกรม อิมพีแดนซ์รวมคือผลรวมของอิมพีแดนซ์ย่อยแต่ละส่วน 
> องค์ประกอบความต้านทานจะสลายพลังงาน ในขณะที่องค์ประกอบรีแอกทีฟ 
> (reactive) จะสะสมพลังงานสลับกันไป ที่ภาวะสั่นพ้อง (resonance) 
> ค่ารีแอกแตนซ์เหนี่ยวนำและรีแอกแตนซ์ตัวเก็บประจุมีค่าเท่ากัน 
> ส่งผลให้ตัวประกอบกำลังไฟฟ้ามีค่าเท่ากับหนึ่ง

---

## การแบ่ง Chunk สำหรับบทยาว

```python
# ตัวอย่าง logic การแบ่ง chunk
def split_by_section(text, max_words=2000):
    """แบ่งตามหัวข้อ ไม่ตัดกลางสมการ"""
    sections = re.split(r'\n#{1,3} ', text)
    chunks = []
    current = ""
    for section in sections:
        if word_count(current + section) < max_words:
            current += "\n### " + section
        else:
            chunks.append(current)
            current = "\n### " + section
    if current:
        chunks.append(current)
    return chunks
```
