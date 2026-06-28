# คู่มือใช้งาน translate_textbook_v2.py

## ติดตั้ง

```bash
pip install anthropic
# ต้องมี poppler-utils สำหรับ image mode
# macOS: brew install poppler
# Ubuntu: sudo apt install poppler-utils
export ANTHROPIC_API_KEY="sk-ant-xxxx"
```

---

## 3 โหมดและคำสั่ง

### text mode — input เป็น .md หรือ .txt
```bash
python translate_textbook_v2.py text chapter1.md \
  --chapter CH01 \
  --glossary glossary.md
```
ใช้เมื่อ: แปลงจาก PDF เป็น text ไว้แล้ว หรือ PDF ที่ extract สมการได้ปกติ

### image mode — PDF ที่สมการเป็น image (Identity-H font)
```bash
python translate_textbook_v2.py image book.pdf 22 80 \
  --chapter CH01 \
  --glossary glossary.md
```
- `22` = หน้าเริ่มต้น, `80` = หน้าสิ้นสุด
- rasterize ทีละหน้า → Claude อ่านภาพ → แปล

### auto mode — ตรวจสอบและเลือกโหมดอัตโนมัติ (แนะนำ)
```bash
python translate_textbook_v2.py auto book.pdf 22 80 \
  --chapter CH01 \
  --glossary glossary.md
```

---

## ตัวอย่างสำหรับ RF & Microwave Power Amplifier Design (Grebennikov)

หนังสือเล่มนี้มี 10 บท หน้า ~22–1100 (หน้า 1–21 คือ copyright และสารบัญ)
สมการเป็น image ทั้งหมด (Identity-H font) → ใช้ image mode

```bash
# บทที่ 1: หน้า 22–84 (ประมาณ)
python translate_textbook_v2.py image \
  RF_and_Microwave_Power_Amplifier_Design_2.pdf 22 84 \
  --chapter CH01 --glossary rf-pa-glossary/glossary.md

# บทที่ 2: หน้า 85–160
python translate_textbook_v2.py image \
  RF_and_Microwave_Power_Amplifier_Design_2.pdf 85 160 \
  --chapter CH02 --glossary rf-pa-glossary/glossary.md
```

ถ้าสคริปต์หยุดกลางคัน — รันคำสั่งเดิมซ้ำได้เลย จะต่อจาก checkpoint อัตโนมัติ

---

## ไฟล์ที่จะได้หลังรัน

```
translated/
  CH01-P0022.md    ← แต่ละหน้า (image mode)
  CH01-P0023.md
  ...
CH01_translated.md  ← ไฟล์รวมพร้อมใช้
CH01_qc_report.json ← รายงานปัญหา QC (ถ้ามี)
checkpoint.json     ← สำหรับ resume
page_images/        ← ภาพที่ rasterize (ลบได้หลังเสร็จ)
```

---

## ต้นทุนโดยประมาณ (image mode)

| บท | จำนวนหน้า | เวลา | ค่า API (ประมาณ) |
|----|----------|------|----------------|
| 1 บท เฉลี่ย | ~60 หน้า | ~40 นาที | $0.50–1.00 |
| ทั้งเล่ม 10 บท | ~600 หน้า | ~7 ชั่วโมง | $5–10 |

รันค้างคืนได้ — checkpoint บันทึกทุกหน้า
