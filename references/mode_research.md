# โหมด B — แปลบทความวิจัย (IEEE / MDPI / Springer)

## ลักษณะเนื้อหาโหมดนี้
- มีโครงสร้างมาตรฐาน: Abstract → Introduction → Method → Results → Discussion → Conclusion
- มีการอ้างอิงในรูปแบบ [1] (IEEE) หรือ (Author, Year) (APA/MDPI)
- มีตาราง กราฟ และรูปภาพพร้อม caption
- ความยาว 4–20 หน้า

---

## System Prompt สำหรับ Claude API

```
You are a Thai academic translator for research papers in electrical engineering, 
power systems, and AI. Translate the following research paper section into formal 
Thai academic language.

STRICT RULES:
1. Use Royal Institute terminology (ราชบัณฑิตยสภา) for all technical terms
2. Keep citation markers EXACTLY as-is: [1], [2,3], (Smith, 2023)
3. Keep ALL equations, variables, and symbols in original notation
4. Author names, journal names, conference names: DO NOT translate
5. Acronyms on first occurrence: full Thai term + English acronym in parentheses
   e.g., "การเรียนรู้ของเครื่อง (Machine Learning: ML)"
   After first occurrence: use Thai term only or acronym
6. Paper section titles: use standard Thai equivalents (see below)
7. Numbers + units: keep exactly as source (e.g., 48.5%, 3.7 kW, 0.95 p.u.)

STYLE:
- Formal academic Thai, passive voice preferred
- Use "ผู้วิจัย" for "the authors/we" 
- "งานวิจัยนี้" for "this paper/study"
- "ผลการทดลองแสดงให้เห็นว่า..." for "The results show that..."
```

---

## ชื่อส่วนมาตรฐานของบทความ (Section Title Translations)

| อังกฤษ | ไทยมาตรฐาน |
|--------|-----------|
| Abstract | บทคัดย่อ |
| Keywords | คำสำคัญ |
| Introduction | บทนำ |
| Literature Review | การทบทวนวรรณกรรม |
| Related Work | งานวิจัยที่เกี่ยวข้อง |
| Methodology / Method | วิธีดำเนินการวิจัย |
| Proposed Method | วิธีที่นำเสนอ |
| System Design | การออกแบบระบบ |
| Experimental Setup | การตั้งค่าการทดลอง |
| Results | ผลการวิจัย |
| Results and Discussion | ผลการวิจัยและการอภิปราย |
| Discussion | การอภิปราย |
| Conclusion | บทสรุป |
| Acknowledgment | กิตติกรรมประกาศ |
| References | เอกสารอ้างอิง |
| Appendix | ภาคผนวก |

---

## ตัวอย่างการแปลแต่ละส่วน

### Abstract
```
ต้นฉบับ:
"This paper proposes a novel LSTM-based forecasting model for rooftop photovoltaic 
(PV) power generation under tropical weather conditions. The proposed model achieves 
a mean absolute percentage error (MAPE) of 4.32%, outperforming baseline methods."

แปล:
"บทความนี้นำเสนอแบบจำลองพยากรณ์ชนิดใหม่โดยอาศัย LSTM สำหรับการผลิต
กำลังไฟฟ้าจากเซลล์แสงอาทิตย์บนหลังคาภายใต้สภาพภูมิอากาศเขตร้อน 
แบบจำลองที่นำเสนอบรรลุค่าความคลาดเคลื่อนร้อยละสัมบูรณ์เฉลี่ย 
(Mean Absolute Percentage Error: MAPE) ที่ร้อยละ 4.32 ซึ่งดีกว่า
วิธีการอ้างอิงทั้งหมด"
```

### Introduction (การนำ context ที่ถูกต้อง)
- "Recently, ..." → "ในช่วงไม่กี่ปีที่ผ่านมา ..."
- "However, ..." → "อย่างไรก็ตาม ..."
- "Therefore, ..." → "ด้วยเหตุนี้ ..."
- "To address this, ..." → "เพื่อแก้ไขปัญหาดังกล่าว ..."
- "The main contributions are:" → "ผลงานหลักของงานวิจัยนี้ได้แก่:"

### Results
- "Figure X shows..." → "รูปที่ X แสดง..."
- "Table X summarizes..." → "ตารางที่ X สรุป..."
- "As can be seen..." → "จากผลที่แสดง..."
- "It can be observed that..." → "สังเกตได้ว่า..."
- "outperforms" → "มีสมรรถนะสูงกว่า"
- "significantly better" → "ดีกว่าอย่างมีนัยสำคัญ"

---

## การจัดการ Keywords

```
ต้นฉบับ: "Keywords: photovoltaic, machine learning, LSTM, forecasting, tropical climate"

แปล:
"คำสำคัญ: โฟโตโวลเทอิก, การเรียนรู้ของเครื่อง, LSTM, การพยากรณ์, ภูมิอากาศเขตร้อน"

หมายเหตุ: Keywords แปลเป็นไทย แต่ถ้าเป็นชื่อเฉพาะ (LSTM) คงไว้
```

---

## การจัดการตารางและรูป

```
Caption ตาราง:
"TABLE I: COMPARISON OF FORECASTING METHODS"
→ "ตารางที่ 1: การเปรียบเทียบวิธีการพยากรณ์"

Caption รูป:
"Fig. 2. Proposed system architecture."
→ "รูปที่ 2 สถาปัตยกรรมระบบที่นำเสนอ"

เนื้อในตาราง:
- หัวคอลัมน์: แปลเป็นไทย
- ตัวเลขและหน่วย: คงเดิม
- ชื่อวิธีการ (LSTM, GRU, ARIMA): คงเดิม
```
