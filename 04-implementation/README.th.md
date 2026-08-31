# 04 — การพัฒนาระบบ

<!-- lang-switch -->
[English](README.md) · **ภาษาไทย**

สองส่วนที่ deploy แยกกัน ดู [`../tech_stack.th.md`](../tech_stack.th.md) สำหรับ stack ทั้งหมด
และ [`../implementation_plan.th.md`](../implementation_plan.th.md) สำหรับลำดับ sprint

```
engine/      Python — การนำเข้า เชื่อมทักษะ จับคู่ FastAPI
             รันบน gpu-linux-server (ห้องทำงานภาควิชา 24/7)

annotation/  คู่มือผู้ประเมินสำหรับด่านประเมิน Sprint 4

web/         Astro — เว็บผลลัพธ์สาธารณะ + แอปวิเคราะห์ที่จำกัดสิทธิ์
             deploy ไปยัง Cloudflare Workers ที่ vru-ai.com/iris
```

เอนจิน **เผยแพร่** เอกสารผลลัพธ์ที่มีเลขเวอร์ชัน ส่วนชั้นเว็บอ่านผลที่เผยแพร่แล้วอย่างเดียว
ไม่มีอะไรบนเว็บสาธารณะที่แตะเอนจินตอนมีคนเข้าใช้

## สถานะ

**Sprint 1–3 สร้างและวัดผลแล้ว** คำสั่ง `iris link <programme>` ทำงานครบสาย: การนำเข้า
เอกสารจากผู้ผลิต PDF ห้าราย โดยไม่ต้องใช้ GPU, การค้นคืนเชิงคำศัพท์ที่ recall@10 75 %
และการตัดสินด้วย `iris-adjudicator` ที่ใช้หน่วยความจำ 6.6 GB ถัดไปคือ Sprint 4 —
ด่านประเมินผล ซึ่งบล็อกทุกอย่างที่อยู่หลังจากนั้น

ระบบเดิม (backend Rust/Axum, backend Python Celery, sidecar HDBSCAN, scraper เว็บหางาน,
โครง Next.js) ถูกลบเมื่อ 2026-08-27 เพราะสร้างขึ้นรอบการดึงข้อมูลจากเว็บหางานและการจัดกลุ่ม
คลังทักษะที่เกิดขึ้นเอง ซึ่งการเปลี่ยนทิศทางมาใช้มาตรฐาน Skill Mapping แห่งชาติลบทิ้งทั้งคู่
ดู [`../03-solution-design/solution-proposal.th.md`](../03-solution-design/solution-proposal.th.md)

`web/` จะสร้างใน Sprint 8
