# Glossary — RF and Microwave Power Amplifier Design
# Grebennikov, McGraw-Hill 2015 | 1,132 หน้า | 10 บท

> ไฟล์นี้ต้องส่งให้ subagent **ทุกตัว** ก่อนเริ่มแปล
> เพื่อให้ศัพท์สม่ำเสมอทั้งเล่ม
> อัปเดตครั้งล่าสุด: 2026-06-28

---

## กฎใช้งาน (อ่านก่อนแปลทุกครั้ง)

1. **ใช้คำในตารางนี้เท่านั้น** — ห้ามแปลเองถ้ามีคำอยู่แล้ว
2. **ครั้งแรกที่พบในแต่ละบท** → เขียน "ภาษาไทย (English)" เช่น "อิมพีแดนซ์ (impedance)"
3. **ครั้งต่อไปในบทเดียวกัน** → ใช้ภาษาไทยอย่างเดียว
4. **ตัวย่อ/สัญลักษณ์** (S, Z, Y, H, ABCD, Q, K) → คงไว้เหมือนเดิมทั้งหมด
5. **ชื่อเฉพาะ** → ดูหมวด do_not_translate ด้านล่าง

---

## หมวด 1 — วงจรสองพอร์ตและพารามิเตอร์ (บทที่ 1)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| two-port network | วงจรสองพอร์ต | |
| one-port network | วงจรหนึ่งพอร์ต | |
| nonautonomous | ไม่อิสระ | ในบริบทวงจร |
| impedance Z-parameters | Z-พารามิเตอร์อิมพีแดนซ์ | ตัวย่อ Z คงไว้ |
| admittance Y-parameters | Y-พารามิเตอร์แอดมิตแตนซ์ | ตัวย่อ Y คงไว้ |
| hybrid H-parameters | H-พารามิเตอร์ไฮบริด | ตัวย่อ H คงไว้ |
| transmission ABCD-parameters | ABCD-พารามิเตอร์การส่งผ่าน | ตัวย่อ ABCD คงไว้ |
| scattering S-parameters | S-พารามิเตอร์การกระเจิง | ตัวย่อ S คงไว้ |
| open-circuit impedance | อิมพีแดนซ์วงจรเปิด | |
| short-circuit admittance | แอดมิตแตนซ์วงจรลัด | |
| driving-point impedance | อิมพีแดนซ์จุดขับ | |
| transfer impedance | อิมพีแดนซ์การถ่ายโอน | |
| forward current transfer function | ฟังก์ชันถ่ายโอนกระแสไปข้างหน้า | |
| reverse voltage transfer function | ฟังก์ชันถ่ายโอนแรงดันย้อนกลับ | |
| reflection coefficient | สัมประสิทธิ์การสะท้อน | สัญลักษณ์ Γ คงไว้ |
| transmission line | สายส่ง | |
| lumped element | ส่วนประกอบแบบก้อน | |
| distributed circuit | วงจรแบบกระจาย | |
| inductor | ตัวเหนี่ยวนำ | |
| capacitor | ตัวเก็บประจุ | |
| π-network / T-network | วงจร π / วงจร T | ตัวอักษรกรีกคงไว้ |
| phasor | เฟสเซอร์ | ทับศัพท์ยอมรับ |
| immittance | อิมมิตแตนซ์ | ทับศัพท์ (impedance + admittance) |

---

## หมวด 2 — การออกแบบวงจรแบบไม่เชิงเส้น (บทที่ 2)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| nonlinear circuit | วงจรไม่เชิงเส้น | |
| frequency-domain analysis | การวิเคราะห์โดเมนความถี่ | |
| time-domain analysis | การวิเคราะห์โดเมนเวลา | |
| piecewise-linear approximation | การประมาณเชิงเส้นแบบช่วง | |
| conduction angle | มุมการนำกระแส | สัญลักษณ์ θ คงไว้ |
| harmonic balance method | วิธีสมดุลฮาร์มอนิก | |
| harmonic component | องค์ประกอบฮาร์มอนิก | |
| Fourier-series expansion | การกระจายอนุกรมฟูเรียร์ | |
| dc component | องค์ประกอบกระแสตรง | "dc" คงไว้เป็นตัวพิมพ์เล็ก |
| fundamental-frequency component | องค์ประกอบความถี่มูลฐาน | |
| nth-order harmonic | ฮาร์มอนิกอันดับที่ n | |
| current coefficient | สัมประสิทธิ์กระแส | |
| pinch-off voltage | แรงดันหยุดการนำ | สัญลักษณ์ Vp คงไว้ |
| quiescent current | กระแสขณะพัก | |
| Bessel function | ฟังก์ชันเบสเซล | ชื่อเฉพาะ Bessel คงไว้ |
| Newton-Raphson algorithm | ขั้นตอนวิธีนิวตัน-ราฟสัน | ชื่อเฉพาะคงไว้ |
| quasilinear method | วิธีกึ่งเชิงเส้น | |
| X-parameters | X-พารามิเตอร์ | ตัวย่อคงไว้ |
| behavioral model | แบบจำลองพฤติกรรม | |
| memory effect | ผลเชิงความจำ | |

---

## หมวด 3 — การสร้างแบบจำลองอุปกรณ์แอกทีฟ (บทที่ 3)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| active device | อุปกรณ์แอกทีฟ | |
| equivalent circuit | วงจรสมมูล | |
| small-signal equivalent circuit | วงจรสมมูลสัญญาณขนาดเล็ก | |
| nonlinear model | แบบจำลองไม่เชิงเส้น | |
| power MOSFET | power MOSFET | ตัวย่อคงไว้ |
| MESFET | MESFET | ตัวย่อคงไว้ |
| HEMT | HEMT | ตัวย่อคงไว้ |
| BJT (bipolar junction transistor) | BJT (ทรานซิสเตอร์รอยต่อไบโพลาร์) | ครั้งแรกขยาย ครั้งต่อไปใช้ BJT |
| HBT (heterojunction bipolar transistor) | HBT | ตัวย่อคงไว้ |
| MMIC | MMIC | ตัวย่อคงไว้ |
| drain / gate / source | เดรน / เกต / ซอร์ส | ทับศัพท์ยอมรับ |
| collector / base / emitter | คอลเลกเตอร์ / เบส / อีมิตเตอร์ | ทับศัพท์ยอมรับ |
| transconductance | ทรานส์คอนดักแตนซ์ | สัญลักษณ์ gm คงไว้ |
| gate-source resistance | ความต้านทานเกต-ซอร์ส | |
| nonlinear I-V model | แบบจำลอง I-V ไม่เชิงเส้น | |
| nonlinear C-V model | แบบจำลอง C-V ไม่เชิงเส้น | |
| charge conservation | การอนุรักษ์ประจุ | |
| temperature dependence | การขึ้นอยู่กับอุณหภูมิ | |
| saturation current | กระแสอิ่มตัว | |

---

## หมวด 4 — การจับคู่อิมพีแดนซ์ (บทที่ 4)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| impedance matching | การจับคู่อิมพีแดนซ์ | **ห้ามแปลว่า "การแมตชิ่ง"** |
| matching network | วงจรจับคู่ | |
| Smith chart | Smith chart | ชื่อเฉพาะ คงไว้ |
| L-transformer | หม้อแปลง L | |
| VSWR (voltage standing wave ratio) | อัตราส่วนคลื่นนิ่งแรงดัน (VSWR) | ครั้งแรกขยาย |
| return loss | การสูญเสียย้อนกลับ | |
| reflection coefficient | สัมประสิทธิ์การสะท้อน | Γ คงไว้ |
| microstrip line | สายไมโครสตริป | |
| stripline | สายสตริป | |
| coplanar waveguide | ท่อนำคลื่นแบบโคเพลนาร์ | |
| slotline | สายสลอต | |
| coaxial line | สายโคแอกเชียล | |
| electrical length | ความยาวทางไฟฟ้า | สัญลักษณ์ θ คงไว้ |
| wavelength | ความยาวคลื่น | สัญลักษณ์ λ คงไว้ |
| narrowband | แถบความถี่แคบ | |
| broadband | แถบความถี่กว้าง | |
| UHF | UHF | ตัวย่อคงไว้ |
| VHF | VHF | ตัวย่อคงไว้ |
| normalized impedance | อิมพีแดนซ์ทำให้เป็นบรรทัดฐาน | |

---

## หมวด 5 — หม้อแปลง ตัวรวม และตัวเชื่อมต่อ (บทที่ 5)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| power combiner | ตัวรวมกำลัง | |
| power divider | ตัวแบ่งกำลัง | |
| directional coupler | ตัวเชื่อมต่อทิศทาง | |
| balun | บาลัน | ทับศัพท์ยอมรับ |
| Wilkinson power divider | ตัวแบ่งกำลัง Wilkinson | ชื่อเฉพาะ Wilkinson คงไว้ |
| branch-line hybrid coupler | ตัวเชื่อมต่อไฮบริดแบบเส้นแยก | |
| coupled-line directional coupler | ตัวเชื่อมต่อทิศทางสายเชื่อมคู่ | |
| ferrite core | แกนเฟอร์ไรต์ | |
| impedance transformation | การแปลงอิมพีแดนซ์ | |
| three-port network | วงจรสามพอร์ต | |
| four-port network | วงจรสี่พอร์ต | |
| insertion loss | การสูญเสียการแทรก | |
| isolation | การแยกโดด | |

---

## หมวด 6 — พื้นฐานการออกแบบเครื่องขยายกำลัง (บทที่ 6)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| power amplifier | เครื่องขยายกำลัง | **ห้ามใช้ "เพาเวอร์แอมป์"** |
| power gain | อัตราขยายกำลัง | |
| transducer power gain | อัตราขยายกำลังทรานสดิวเซอร์ | |
| operating power gain | อัตราขยายกำลังปฏิบัติการ | |
| available power gain | อัตราขยายกำลังที่รับได้ | |
| stability factor | ตัวประกอบเสถียรภาพ | สัญลักษณ์ K คงไว้ |
| unconditionally stable | เสถียรอย่างไม่มีเงื่อนไข | |
| potentially unstable | อาจไม่เสถียร | |
| parasitic oscillation | การแกว่งปรสิต | |
| stabilization circuit | วงจรทำให้เสถียร | |
| conjugate matching | การจับคู่คอนจูเกต | |
| load line | เส้นโหลด | |
| output impedance | อิมพีแดนซ์เอาต์พุต | |
| Class A operation | การทำงานคลาส A | ตัวอักษร A/B/C/D/E/F คงไว้ |
| Class AB operation | การทำงานคลาส AB | |
| Class B operation | การทำงานคลาส B | |
| Class C operation | การทำงานคลาส C | |
| efficiency | ประสิทธิภาพ | **ห้ามใช้ "เอฟฟิเซียนซี"** |
| collector efficiency | ประสิทธิภาพคอลเลกเตอร์ | |
| drain efficiency | ประสิทธิภาพเดรน | |
| 1-dB gain compression point | จุดคอมเพรสชัน 1 dB | |
| third-order intercept point | จุดตัด IP3 | สัญลักษณ์ IP3 คงไว้ |
| intermodulation distortion | ความเพี้ยนอินเตอร์โมดูเลชัน | IMD คงไว้ |
| linearity | ความเป็นเชิงเส้น | |
| load-pull characterization | การหาคุณลักษณะแบบดึงโหลด | |
| push-pull amplifier | เครื่องขยายแบบผลัก-ดึง | |
| balanced amplifier | เครื่องขยายแบบบาลานซ์ | |
| bias circuit | วงจรไบแอส | |
| quiescent point | จุดพัก (จุดไบแอส) | |

---

## หมวด 7 — เครื่องขยายกำลังประสิทธิภาพสูง (บทที่ 7)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| high-efficiency | ประสิทธิภาพสูง | |
| overdriven Class B | คลาส B แบบขับเกิน | |
| Class-F power amplifier | เครื่องขยายกำลังคลาส F | |
| inverse Class F | คลาส F ผกผัน | |
| Class-E power amplifier | เครื่องขยายกำลังคลาส E | |
| switching operation | การทำงานแบบสวิตช์ | |
| voltage waveform | รูปคลื่นแรงดัน | |
| current waveform | รูปคลื่นกระแส | |
| load network | วงจรโหลด | |
| harmonic termination | การสิ้นสุดที่ฮาร์มอนิก | |
| open-circuit peaking | การยอดวงจรเปิด | |
| short-circuit termination | การสิ้นสุดแบบวงจรลัด | |
| quarterwave transmission line | สายส่งหนึ่งในสี่ความยาวคลื่น | λ/4 คงไว้ |
| saturation resistance | ความต้านทานอิ่มตัว | |
| shunt capacitance | ตัวเก็บประจุแบบขนาน | |
| finite DC-feed inductance | ตัวเหนี่ยวนำป้อนกระแสตรงแบบจำกัด | |
| parallel-circuit Class E | คลาส E วงจรขนาน | |
| collector voltage | แรงดันคอลเลกเตอร์ | |
| supply voltage | แรงดันไฟเลี้ยง | สัญลักษณ์ Vcc/Vdd คงไว้ |

---

## หมวด 8 — เครื่องขยายกำลังแถบกว้าง (บทที่ 8)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| broadband power amplifier | เครื่องขยายกำลังแถบกว้าง | |
| Bode-Fano criterion | เกณฑ์ Bode-Fano | ชื่อเฉพาะคงไว้ |
| lossy compensation network | วงจรชดเชยแบบสูญเสีย | |
| reactance compensation | การชดเชยรีแอกแตนซ์ | |
| gain flatness | ความราบเรียบของอัตราขยาย | |
| multioctave | หลายอ็อกเทฟ | |
| CMOS | CMOS | ตัวย่อคงไว้ |
| GaN | GaN | ตัวย่อคงไว้ |
| GaAs | GaAs | ตัวย่อคงไว้ |
| LDMOS | LDMOS | ตัวย่อคงไว้ |

---

## หมวด 9 — การทำให้เป็นเชิงเส้นและการเพิ่มประสิทธิภาพ (บทที่ 9)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| linearization | การทำให้เป็นเชิงเส้น | |
| feedforward | ฟีดฟอร์เวิร์ด | ทับศัพท์ยอมรับ |
| predistortion | พรีดิสทอร์ชัน | ทับศัพท์ยอมรับ |
| outphasing | เอาต์เฟสซิ่ง | ทับศัพท์ยอมรับ |
| envelope tracking | การติดตามเอนเวโลป | |
| switched-path amplifier | เครื่องขยายแบบสลับเส้นทาง | |
| variable-load amplifier | เครื่องขยายแบบโหลดแปรผัน | |
| handset | โทรศัพท์มือถือ | |
| SiGe HBT | SiGe HBT | ตัวย่อคงไว้ |

---

## หมวด 10 — เครื่องขยายกำลัง Doherty (บทที่ 10)

| อังกฤษ | ไทย | หมายเหตุ |
|--------|-----|---------|
| Doherty power amplifier | เครื่องขยายกำลัง Doherty | ชื่อเฉพาะ Doherty คงไว้ |
| carrier amplifier | เครื่องขยายพาหะ | |
| peaking amplifier | เครื่องขยายยอด | |
| offset line | สายชดเชยเฟส | |
| back-off | แบ็กออฟ | ทับศัพท์ยอมรับ |
| asymmetric Doherty | Doherty แบบไม่สมมาตร | |
| multistage Doherty | Doherty หลายขั้น | |
| inverted Doherty | Doherty แบบผกผัน | |
| dual-band | คู่แถบ | |
| tri-band | สามแถบ | |
| digitally driven | ขับด้วยสัญญาณดิจิทัล | |

---

## หมวด — ห้ามแปล (Do Not Translate)

### ชื่อผู้แต่งและนักวิทยาศาสตร์
Grebennikov, Smith, Wilkinson, Doherty, Bode, Fano, Bessel, Newton, Raphson, Fourier, Chebyshev, Butterworth, Rollett, Friis, Carter, Mizuhashi

### ชื่อเทคโนโลยีและมาตรฐาน
WCDMA, CDMA, LTE, GSM, OFDM, SAR, T/R module, MMIC, RF, IF, PA, LNA, VCO

### ชื่อบริษัทและสถาบัน
Alcatel-Lucent, Bell Labs, Infineon, M/A-COM, Nitronex, McGraw-Hill, IRE, IEEE

### ชื่อซอฟต์แวร์และวิธีการ
ADS, SPICE, MATLAB, load-pull (ใช้ทับศัพท์ "การดึงโหลด" เมื่อใช้เป็นคำนาม แต่คงไว้เมื่อเป็นชื่อวิธีการ)

### สัญลักษณ์และตัวย่อที่คงไว้ทุกกรณี
dB, dBm, W, mW, kW, GHz, MHz, kHz, Hz, Ω, V, A, mA, μA, F, pF, nF, H, nH, pH,
Q-factor, K (stability factor), Γ (reflection coefficient), η (efficiency), θ (angle),
λ (wavelength), ω (angular frequency), π (pi)

---

## style_guide.md — กฎสำนวนเฉพาะเล่มนี้

### สไตล์การเขียนที่ถูกต้อง
- **ประโยคนิยาม:** "... ถูกนิยามโดย..." / "... กำหนดโดยสมการ..."
- **การอ้างอิงรูป:** "รูปที่ X.Y แสดง..." (ไม่ใช่ "FIGURE X.Y แสดง")
- **การอ้างอิงสมการ:** "สมการที่ (X.Y)" (ไม่ใช่ "Eq. (X.Y)")
- **การอ้างอิงบท:** "บทที่ X" (ไม่ใช่ "Chap. X" หรือ "Chapter X")
- **การอ้างอิงหัวข้อ:** "หัวข้อที่ X.Y"

### คำที่มีหลายบริบท — ใช้ตามสถานการณ์
| อังกฤษ | บริบท 1 | บริบท 2 |
|--------|---------|---------|
| performance | สมรรถนะ (เครื่องขยาย) | ผลการดำเนินงาน (ระบบ) |
| power | กำลัง (ไฟฟ้า) | กำลังงาน (ฟิสิกส์) |
| gain | อัตราขยาย (วงจร) | กำไร (ห้ามใช้ในบริบทวิศวกรรม) |
| response | การตอบสนอง (วงจร) | ผลตอบรับ (ห้ามใช้) |
| terminal | ขั้ว (วงจร) | เทอร์มินัล (คอมพิวเตอร์) |

### ห้ามใช้คำเหล่านี้
| ห้ามใช้ | ให้ใช้แทน |
|--------|----------|
| แอมพลิไฟเออร์ | เครื่องขยายกำลัง |
| แมตชิ่ง | การจับคู่อิมพีแดนซ์ |
| เอฟฟิเซียนซี | ประสิทธิภาพ |
| อินพุต / เอาต์พุต | อินพุต/เอาต์พุต ยอมรับได้ (หรือ "สัญญาณเข้า/ออก") |
| เพาเวอร์ | กำลัง |
| ดีไซน์ | การออกแบบ |
