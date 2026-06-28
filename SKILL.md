---
name: thai-academic-translator
description: >
  แปลตำราและเอกสารวิชาการต่างประเทศ (อังกฤษ → ไทย) ให้เป็นภาษาวิชาการไทย
  มาตรฐาน ใช้ศัพท์บัญญัติราชบัณฑิตยสภาถูกต้อง เน้นสาขาวิศวกรรมไฟฟ้า/
  อิเล็กทรอนิกส์ พลังงาน AI และวิทยาศาสตร์ประยุกต์ รองรับทุกประเภทเนื้อหา
  ได้แก่ ตำรา/หนังสือ, บทความวิจัย (IEEE/MDPI), สไลด์/เอกสารสอน
  รองรับทั้งโหมดเดี่ยวและ Cowork (subagents ขนาน)

  ใช้ skill นี้ทุกครั้งที่ผู้ใช้ต้องการ:
  - แปลตำราหรือหนังสือต่างประเทศเป็นภาษาไทยวิชาการ
  - แปลบทความ IEEE / MDPI / Springer เป็นไทย
  - แปลสไลด์ PowerPoint หรือเอกสารสอนเป็นไทย
  - ตรวจสอบหรือแก้ไขศัพท์บัญญัติราชบัณฑิตในงานแปล
  - แปลตำราหลายบทพร้อมกันด้วย Cowork / subagents
  - "แปล", "translate", "ศัพท์บัญญัติ", "ภาษาวิชาการ", "ราชบัณฑิต"
  - ต้องการภาษาไทยที่อ่านง่ายแต่ถูกต้องตามมาตรฐานวิชาการไทย
---

# Thai Academic Translator Skill

แปลเอกสารวิชาการต่างประเทศ → ภาษาวิชาการไทย ศัพท์ราชบัณฑิตถูกต้อง
ใช้ Claude API (Anthropic) เป็น AI engine หลัก

---

## หลักการแปล 5 ข้อ (ต้องยึดถือเสมอ)

1. **ศัพท์บัญญัติก่อนเสมอ** — ค้นจาก `references/royal_institute_terms.md` ก่อนแปลทุกครั้ง
2. **คงศัพท์เทคนิคสากล** — คำที่ราชบัณฑิตยังไม่มีบัญญัติ ให้ใช้ทับศัพท์ตามด้วยคำอธิบายในวงเล็บ
3. **รักษาโครงสร้างต้นฉบับ** — สมการ, รูปแบบ, การจัดหน้า ต้องเหมือนเดิมทุกประการ
4. **สมการไม่แปล** — ตัวแปร, สัญลักษณ์, หน่วย SI คงภาษาอังกฤษ/สัญลักษณ์ทั้งหมด
5. **อ่านง่ายแต่เป็นวิชาการ** — ไม่แปลแบบ word-for-word ให้ปรับสำนวนเป็นภาษาไทยที่ไหลลื่น

---

## โหมดการแปล (เลือกตามประเภทเนื้อหา)

### โหมด A — ตำรา/หนังสือ (บทยาว มีสมการ)
→ อ่าน `references/mode_textbook.md`

### โหมด B — บทความวิจัย (IEEE/MDPI/Springer)
→ อ่าน `references/mode_research.md`

### โหมด C — สไลด์/เอกสารสอน
→ อ่าน `references/mode_slides.md`

**วิธีเลือกโหมด:** ถ้าผู้ใช้ไม่ระบุ ให้ดูจากรูปแบบเนื้อหา:
- มี Abstract + Introduction + Conclusion → โหมด B
- มี Chapter/Section ยาว + สมการ + แบบฝึกหัด → โหมด A
- มีหัวข้อสั้น bullet points → โหมด C

---

## ขั้นตอนการแปล — เลือกตาม environment

### โหมดเดี่ยว (Claude.ai / API โดยตรง)
```
1. วิเคราะห์เนื้อหา → ระบุโหมด A/B/C
2. โหลด references/royal_institute_terms.md → สร้าง term map
3. แบ่ง chunk ตาม heading (~1,800 คำ/chunk)
4. แปลทีละ chunk วนซ้ำจนครบ บันทึก checkpoint ทุก chunk
5. ตรวจสอบ QC checklist
6. รวมไฟล์ → ส่งออก
```

### โหมด Cowork (Orchestrator + Subagents)

**Orchestrator ทำ:**
```
1. วิเคราะห์ไฟล์ทั้งหมด → ระบุโหมด A/B/C
2. แบ่งงานเป็น task list: 1 task = 1 บท (หรือ 1 section ใหญ่)
3. Spawn subagent 1 task ต่อ 1 subagent — รันขนานทั้งหมด
4. รอรับผลจากทุก subagent
5. รวมผล → เรียง → QC รวม → ส่งออก
```

**แต่ละ Subagent ทำ (อิสระจากกัน):**
```
1. รับ: ไฟล์บทที่รับผิดชอบ + โหมด + term map ที่ Orchestrator ส่งมา
2. โหลด references/royal_institute_terms.md (ทุก subagent โหลดเองได้)
3. แบ่ง chunk ภายในบท → แปลทีละ chunk
4. ตรวจ QC checklist ทุก chunk
5. ส่งคืน Orchestrator: { chapter_id, translated_text, qc_report }
```

**Prompt ที่ Orchestrator ส่งให้ Subagent:**
```
คุณเป็น subagent แปลบทที่ {N} ของตำราวิชาการ
ใช้ skill: thai-academic-translator โหมด {A/B/C}
ศัพท์สำคัญที่ต้องสม่ำเสมอทั้งเล่ม: {shared_term_map}

เนื้อหา:
{chapter_text}

ส่งคืนในรูปแบบ JSON:
{
  "chapter_id": N,
  "translated_text": "...",
  "qc_report": { "issues": [], "term_inconsistencies": [] }
}
```

**สิ่งที่ต้องส่งให้ subagent ทุกตัว (Shared Context):**
- `shared_term_map` — ตาราง term ที่ตกลงกันไว้ก่อนรัน เช่น `{"impedance": "อิมพีแดนซ์", "bandwidth": "แถบความถี่"}` เพื่อให้ศัพท์สม่ำเสมอทั้งเล่ม
- โหมด A/B/C ที่เลือกไว้
- ชื่อตัวละคร/ชื่อเฉพาะที่ไม่ต้องแปล (ถ้ามี)

---

## การตรวจจับ PDF ที่สมการเป็น Image

ตำราวิศวกรรมหลายเล่ม (โดยเฉพาะที่แปลงจาก eBook) มีสมการเป็น image ไม่ใช่ text
pdftotext จะดึงสมการไม่ได้ — ผลแปลจะมีช่องโหว่ทุกจุดที่มีสมการ

**วิธีตรวจสอบก่อนเริ่มแปล:**
```bash
pdffonts ไฟล์.pdf | grep "Identity-H"
# ถ้าพบ Identity-H → สมการเป็น image → ใช้ image mode
```

**สัญญาณที่บ่งชี้ว่าสมการเป็น image:**
- `pdffonts` แสดง `CID TrueType` + `Identity-H` + `emb: yes`
- `pdftotext` ดึงได้ข้อความบรรยาย แต่สมการหายไปทั้งหมด
- ไฟล์ PDF ผลิตจาก Zamzar, Adobe Export, หรือ eBook converter

**3 โหมดการทำงานของ `translate_textbook_v2.py`:**
```
text mode  — input เป็น .md/.txt ที่มีสมการ LaTeX อยู่แล้ว
image mode — PDF ที่สมการเป็น image: rasterize → Claude อ่านภาพ → LaTeX
auto mode  — ตรวจ PDF อัตโนมัติ เลือก text/image mode ให้เอง (แนะนำ)
```

อ่านรายละเอียดคำสั่งและตัวอย่างการใช้งานใน `references/script_guide.md`

**ความเร็วและต้นทุน:**
```
text mode:  ~5–10 วิ/chunk  (~1,800 คำ)  ต้นทุนต่ำ
image mode: ~20–40 วิ/หน้า (1 หน้า/ครั้ง) ต้นทุนสูงกว่า ~3–4×
```

---

## QC Checklist (ตรวจก่อนส่งเสมอ)

**ภาษาและศัพท์:**
- [ ] ศัพท์บัญญัติถูกต้องตามราชบัณฑิต / glossary ที่กำหนด
- [ ] ไม่มีคำทับศัพท์ที่มีศัพท์บัญญัติแล้ว
- [ ] ชื่อผู้แต่ง, ชื่อเฉพาะ, มาตรฐาน (IEEE, IEC ฯลฯ) ไม่ถูกแปล

**ความครบถ้วน:**
- [ ] จำนวนย่อหน้าเท่ากับต้นฉบับ (±2)
- [ ] สมการ LaTeX ยังอยู่ครบ ($$...$$) ไม่ถูกแปลหรือลบ
- [ ] การอ้างอิง [1], [2] หรือ (Author, Year) คงรูปแบบเดิม
- [ ] หน่วย SI (Hz, W, Ω, V, A, dB) ไม่ถูกแปล
- [ ] ไม่มีเนื้อหาที่ AI เติมเอง (ผลแปลต้องไม่ยาวกว่าต้นฉบับ >1.8×)

**image mode เพิ่มเติม:**
- [ ] สมการทุกตัวในต้นฉบับปรากฏใน output เป็น LaTeX
- [ ] หมายเลขสมการ (1.1), (1.2) ถูกต้องและครบ
- [ ] ไม่มีสมการที่ถูกแปลเป็นข้อความธรรมดาแทน LaTeX

---

## การใช้งาน AI Engine

**โหมดเดี่ยว:** อ่านรายละเอียด API configuration ใน `references/api_config.md`
- Model: `claude-sonnet-4-6` (ค่าเริ่มต้น) หรือ `claude-opus-4-6` (งานซับซ้อน)
- Temperature: 0.2, Max tokens: 8192 ต่อ chunk

**โหมด Cowork:** ไม่ต้องเรียก API ตรง — Cowork จัดการ model และ rate limit ให้อัตโนมัติ
- Orchestrator และ subagent แต่ละตัวใช้ Claude โดยตรงผ่าน Cowork environment
- ไม่ต้องใส่ API key หรือตั้งค่า temperature ใน code

---

## การแบ่งงาน

### โหมดเดี่ยว — แบ่ง chunk ภายใน 1 session
```
ตำรา 1 บท (~5,000–15,000 คำ):
  → แบ่งเป็น sections ตาม heading
  → แปลทีละ section ไม่เกิน ~1,800 คำ/chunk
  → รักษา context ด้วยการส่ง heading ก่อนหน้าไปด้วยเสมอ

บทความวิจัย (~3,000–8,000 คำ):
  → แปลทีละ section (Abstract, Intro, Method, Result, Conclusion)
  → ไม่ต้องแบ่ง chunk ย่อยเพิ่มเติม
```

### Cowork — แบ่งระดับ Orchestrator
```
ตำรา 1,000 หน้า (N บท):
  → Orchestrator แบ่ง: 1 subagent = 1 บท
  → แต่ละ subagent แบ่ง chunk ภายในบทของตัวเอง
  → รันทุก subagent พร้อมกัน

กรณี 1 บทยาวมาก (>15,000 คำ):
  → แบ่งเป็น 2 subagent (ครึ่งแรก / ครึ่งหลัง)
  → ส่ง heading overlap 1 section เพื่อรักษา context
```

---

## การรับประกันความสม่ำเสมอของศัพท์ (Cowork เท่านั้น)

เนื่องจาก subagent แต่ละตัวไม่เห็น output ของกันและกัน Orchestrator ต้องสร้าง `shared_term_map` ก่อนรัน:

```
ขั้นตอน:
1. Orchestrator สแกนหน้าสารบัญ + บทนำ → ดึงศัพท์เทคนิคหลัก ~50 คำ
2. จับคู่กับ royal_institute_terms.md
3. ส่ง shared_term_map ให้ subagent ทุกตัวพร้อมกัน
4. หลังรวมผล: ตรวจ term_inconsistencies ข้ามบท
   → ถ้าพบ: แก้ไขเฉพาะ chunk ที่ผิด ไม่ต้องรันใหม่ทั้งหมด
```
