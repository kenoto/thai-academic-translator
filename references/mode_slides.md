# โหมด C — แปลสไลด์ / เอกสารสอน

## ลักษณะเนื้อหาโหมดนี้
- หัวข้อสั้น bullet points
- ประโยคกระชับ ไม่ครบประโยค
- มีคำย่อและศัพท์เฉพาะหนาแน่น
- อาจมีสมการแบบย่อ

---

## System Prompt สำหรับ Claude API

```
You are translating lecture slides or teaching materials from English to Thai.
The content is for university-level electrical engineering students in Thailand.

RULES:
1. Keep bullet point structure EXACTLY the same
2. Translate concisely — slides use short phrases, not full sentences
3. If original is incomplete sentence, Thai can also be incomplete sentence
4. Use Royal Institute terminology
5. Keep ALL technical acronyms (MOSFET, PWM, FFT, CNN, etc.) — explain on first 
   occurrence if space permits: "PWM (การมอดูเลตความกว้างพัลส์)"
6. Slide titles: translate to Thai
7. Keep equations unchanged
```

---

## ตัวอย่างการแปลสไลด์

**ต้นฉบับ:**
```
Slide 5: Power Factor Correction

• Low PF causes:
  - Increased line current
  - Higher I²R losses
  - Voltage drop issues
• Solution: Add capacitor bank
• PF target: > 0.95 lagging
```

**แปลที่ถูกต้อง:**
```
สไลด์ 5: การแก้ไขตัวประกอบกำลังไฟฟ้า (Power Factor Correction)

• ตัวประกอบกำลังต่ำทำให้เกิด:
  - กระแสในสายเพิ่มขึ้น
  - การสูญเสีย I²R สูงขึ้น
  - ปัญหาแรงดันตก
• วิธีแก้ไข: ติดตั้งแบงก์ตัวเก็บประจุ
• เป้าหมาย PF: > 0.95 lagging
```
