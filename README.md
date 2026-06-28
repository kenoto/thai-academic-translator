# Thai Academic Translator Skill

**แปลตำราและบทความวิชาการต่างประเทศ → ภาษาวิชาการไทย**  
ใช้ศัพท์บัญญัติราชบัณฑิตยสภา · รองรับ PDF ที่สมการเป็น image · มี QC อัตโนมัติ

---

## ทำอะไรได้บ้าง

- แปลตำรา/หนังสือวิศวกรรม วิทยาศาสตร์ AI พลังงาน (1,000+ หน้า)
- แปลบทความวิจัย IEEE / MDPI / Springer พร้อมรักษา citation และสมการ
- แปลสไลด์ PowerPoint และเอกสารสอน
- รองรับ PDF ที่สมการถูก render เป็น image — ดึงสมการออกมาเป็น LaTeX อัตโนมัติ
- ตรวจสอบคุณภาพ (QC) อัตโนมัติทุก chunk: ย่อหน้า, สมการ, citation, ศัพท์บัญญัติ
- รันแบบ batch ค้างคืนได้ — resume ต่อจาก checkpoint ถ้าสคริปต์หยุดกลางคัน
- รองรับ Claude Cowork (subagents ขนาน หลายบทพร้อมกัน)

---

## ตัวอย่างผลลัพธ์

**ต้นฉบับ (อังกฤษ):**
> In an RLC series circuit, the total impedance is the sum of the individual impedances.
> At resonance, the inductive and capacitive reactances are equal, resulting in unity power factor.

**ผลแปล (ไทย):**
> ในวงจร RLC อนุกรม อิมพีแดนซ์รวมคือผลรวมของอิมพีแดนซ์ย่อยแต่ละส่วน
> ที่ภาวะสั่นพ้อง (resonance) ค่ารีแอกแตนซ์เหนี่ยวนำและรีแอกแตนซ์ตัวเก็บประจุมีค่าเท่ากัน
> ส่งผลให้ตัวประกอบกำลังไฟฟ้ามีค่าเท่ากับหนึ่ง

---

## โครงสร้างไฟล์

```
thai-academic-translator/
├── README.md                          ← ไฟล์นี้
├── SKILL.md                           ← คำสั่งหลักสำหรับ Claude
├── references/
│   ├── royal_institute_terms.md       ← ศัพท์บัญญัติราชบัณฑิต ~200 คำ
│   ├── mode_textbook.md               ← คู่มือแปลตำรา (prompt + ตัวอย่าง)
│   ├── mode_research.md               ← คู่มือแปลบทความ IEEE/MDPI
│   ├── mode_slides.md                 ← คู่มือแปลสไลด์/เอกสารสอน
│   ├── api_config.md                  ← ตัวอย่าง Python API config
│   ├── script_guide.md                ← คู่มือใช้งาน script
│   └── translate_textbook_v2.py       ← Script แปลพร้อมใช้
└── glossary/
    └── rf-microwave-pa/
        └── glossary.md                ← ตัวอย่าง glossary สาขา RF/Microwave
```

---

## วิธีติดตั้งและใช้งาน

### ความต้องการ

| รายการ | เวอร์ชันขั้นต่ำ |
|--------|--------------|
| Python | 3.10+ |
| anthropic library | 0.112+ |
| poppler-utils | ใดก็ได้ (สำหรับ PDF image mode) |
| Claude API key | จาก console.anthropic.com |

### ติดตั้ง

```bash
# 1. clone repo
git clone https://github.com/kenoto/thai-academic-translator.git
cd thai-academic-translator

# 2. ติดตั้ง Python library
pip install anthropic

# 3. ติดตั้ง poppler (สำหรับ PDF ที่สมการเป็น image)
# macOS:
brew install poppler
# Ubuntu/Debian:
sudo apt install poppler-utils

# 4. ตั้งค่า API key
export ANTHROPIC_API_KEY="sk-ant-xxxx"
```

### ใช้งานเร็ว — แปลไฟล์ Markdown/Text

```bash
python references/translate_textbook_v2.py text chapter1.md \
  --chapter CH01 \
  --glossary glossary/rf-microwave-pa/glossary.md
```

### ใช้งาน — PDF ที่สมการเป็น image (เช่น eBook ที่ export จาก Zamzar)

```bash
# ตรวจสอบก่อนว่าสมการเป็น image ไหม
pdffonts book.pdf | grep "Identity-H"
# ถ้าพบ Identity-H → ใช้ image mode

# แปล (auto detect)
python references/translate_textbook_v2.py auto book.pdf 22 80 \
  --chapter CH01 \
  --glossary glossary/rf-microwave-pa/glossary.md
```

### ตัวเลือกทั้งหมด

```
โหมด:
  text    — input เป็น .md หรือ .txt
  image   — PDF ที่สมการเป็น image (rasterize ทีละหน้า)
  auto    — ตรวจสอบและเลือกโหมดอัตโนมัติ (แนะนำ)

อาร์กิวเมนต์:
  input           ไฟล์ต้นทาง (.md, .txt, หรือ .pdf)
  start           หน้าเริ่มต้น (image/auto mode)
  end             หน้าสิ้นสุด (image/auto mode)
  --chapter       รหัสบท เช่น CH01, CH02 (default: CH00)
  --glossary      path ไปยัง glossary.md
```

---

## ไฟล์ที่จะได้หลังรัน

```
translated/
  CH01-S001.md        ← แต่ละ chunk (text mode)
  CH01-P0022.md       ← แต่ละหน้า (image mode)
  ...
CH01_translated.md    ← ไฟล์รวมพร้อมใช้
CH01_qc_report.json   ← รายงานปัญหา QC (ถ้ามี)
checkpoint.json       ← สำหรับ resume ถ้าสคริปต์หยุดกลางคัน
page_images/          ← ภาพที่ rasterize (ลบได้หลังเสร็จ)
```

---

## ต้นทุน API โดยประมาณ

| งาน | จำนวน | เวลา | ค่า API |
|-----|-------|------|--------|
| บทความวิจัย 1 ฉบับ | ~8,000 คำ | ~5 นาที | $0.05–0.10 |
| ตำรา 1 บท (text mode) | ~60 chunks | ~20 นาที | $0.30–0.60 |
| ตำรา 1 บท (image mode) | ~60 หน้า | ~40 นาที | $1.00–2.00 |
| ตำรา 10 บท (image mode) | ~600 หน้า | ~7 ชั่วโมง | $10–20 |

ใช้ `claude-sonnet-4-6` เป็นค่าเริ่มต้น — รันค้างคืนได้ checkpoint บันทึกทุก chunk/หน้า

---

## สร้าง Glossary สำหรับสาขาของคุณ

glossary คือหัวใจของระบบนี้ — ทำให้ศัพท์สม่ำเสมอทั้งเล่มเมื่อแปลด้วย subagents ขนาน

ดูตัวอย่างจาก `glossary/rf-microwave-pa/glossary.md` แล้วสร้างสำหรับสาขาของคุณเอง โครงสร้างมี 3 ส่วนหลัก:

```markdown
## หมวด 1 — ศัพท์หลักในสาขา
| อังกฤษ | ไทย (ราชบัณฑิต) | หมายเหตุ |

## ห้ามแปล (Do Not Translate)
ชื่อผู้แต่ง, ชื่อมาตรฐาน, ตัวย่อสากล

## style_guide
กฎสำนวนเฉพาะเล่ม/สาขา
```

---

## ใช้กับ Claude Cowork (subagents ขนาน)

ถ้ามีสิทธิ์เข้า Claude Cowork สั่งงานด้วยภาษาพูดได้เลย:

```
"ใช้ skill thai-academic-translator แปลไฟล์ chapter1.md ถึง chapter5.md
พร้อมกัน โดยใช้ glossary/rf-microwave-pa/glossary.md
แล้ว QC และรวมไฟล์ก่อนส่ง"
```

Cowork จะ spawn subagent แยกต่อบท รันขนาน ประหยัดเวลาได้ ~5 เท่า

---

## ข้อควรระวังด้านลิขสิทธิ์

Script และ skill นี้เป็นเครื่องมือช่วยแปล **ผู้ใช้มีหน้าที่ตรวจสอบสิทธิ์ในการแปลเนื้อหานั้นๆ ด้วยตนเอง**

- ใช้เพื่อศึกษาส่วนตัว: ✅ ทำได้
- ใช้ประกอบการสอนในชั้นเรียน (อ้างอิงแหล่งที่มา): ✅ ทำได้ในขอบเขต fair use
- แจก แปล หรือเผยแพร่ออนไลน์: ⚠️ ต้องขออนุญาตเจ้าของลิขสิทธิ์ก่อน
- ขายงานแปล: ❌ ต้องได้รับ translation rights จากสำนักพิมพ์

---

## License

MIT License — ใช้ได้เสรี แต่ขอให้ระบุแหล่งที่มา

```
Thai Academic Translator Skill
สร้างโดย Kritphon Phanrattanachai · มหาวิทยาลัยราชภัฏเพชรบูรณ์
github.com/kenoto/thai-academic-translator
```

---

## ผู้พัฒนา

**Kritphon Phanrattanachai**  
ผู้อำนวยการสถาบันวิจัยและพัฒนา มหาวิทยาลัยราชภัฏเพชรบูรณ์  
kritphon.ai@pcru.ac.th

---

## มีคำถามหรือต้องการ Custom Glossary สำหรับสาขาของคุณ?

ติดต่อได้ที่ kritphon.ai@pcru.ac.th  
หรือ open issue ใน GitHub repo นี้
