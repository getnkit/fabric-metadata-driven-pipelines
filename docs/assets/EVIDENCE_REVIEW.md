# Evidence Presentation Review

ตรวจจาก baseline `ea5eed1` บน `docs/evidence-curation` รอบนี้เป็น visual/editorial curation ไม่ใช่การรับรอง Fabric deployment หรือ broad privacy audit

## Asset accounting

ตรวจครบ 65 inventory assets: 58 original PNGs + 2 finalized SVGs + 5 derived composites และตรวจ `architecture-overview.svg` เพิ่มอีกหนึ่งไฟล์ รวม 66 visuals ทั้งหมดคง path เดิม ไม่มี deletion หรือ rename

Baseline inventory ยืนยัน 30 `approved_and_integrated`, 16 `approved_composite_source`, 19 `pending_curation` และ 19 `not_yet_verified` สถานะเดิมไม่ถูกใช้แทน visual review รอบนี้

| Classification | Count | Disposition |
| --- | ---: | --- |
| `DIRECT_USE` | 30 | เก็บ ณ path เดิม |
| `COMPOSITE_SOURCE_KEEP` | 16 | เก็บ ณ path เดิม |
| `UNIQUE_SUPPORTING_EVIDENCE_KEEP` | 12 | เก็บ ณ path เดิม |
| `REDUNDANT_ARCHIVE_CANDIDATE` | 3 | เก็บ ณ path เดิม; ยังไม่ลบ |
| `SAFE_REMOVE_CANDIDATE` | 0 | เก็บ ณ path เดิม; ยังไม่ลบ |
| `PENDING_ADDITIONAL_EVIDENCE` | 4 | เก็บ ณ path เดิม |

Architecture overview เพิ่มอีกหนึ่ง `DIRECT_USE` นอก inventory; มี 32 image placements ใน 12 Markdown pages ใช้ 31 unique assets รวม overview และการ reuse C15 ใน README

## Complete utilization matrix

ทุก row ด้านล่างคงชื่อเดิม: C/P/D names ใช้นำทางตาม subject ได้ ส่วน CX names ใช้ provenance; detail-number filenames แยกกันด้วยตารางนี้แทน arbitrary rename ชื่อ performance และ no-bronze-append ไม่ถูกใช้เป็นหลักฐานยืนยันสิ่งที่ capture ไม่แสดง Image links ในตารางเป็น asset navigation ไม่ใช่การ integrate raw supporting evidence เป็น figures เพิ่ม


### core

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [c01-control-metadata.png](screenshots/core/c01-control-metadata.png)<br>1405x220 | DEV config แปดรายการ: DATABASE หกและ FILE สอง พร้อม strategy/target; ไม่ใช่ผล execution | `docs/guides/control-plane.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c02-logical-connections.png](screenshots/core/c02-logical-connections.png)<br>1409x220 | logical source/target mapping ร่วมกัน; ไม่แสดง physical settings หรือพิสูจน์ connectivity | `docs/guides/control-plane.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c03-master-orchestration.png](screenshots/core/c03-master-orchestration.png)<br>1733x918 | Paginator invocation ใน master สำเร็จ; Mermaid อธิบายโครงสร้าง ส่วนภาพแสดง activity observation | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c05-sql-server-copy-execution.png](screenshots/core/c05-sql-server-copy-execution.png)<br>1733x914 | FULL AUTO Copy Succeeded และ 20/20 rows; ไม่ใช่หลักฐาน terminal SQL audit | `docs/guides/sql-server-database-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c06-sql-bronze-lineage.png](screenshots/core/c06-sql-bronze-lineage.png)<br>1395x465 | category rows พร้อม batch/run/timestamp lineage; ไม่พิสูจน์จำนวนทั้งตารางหรือ correlation กับ C05 | `docs/guides/sql-server-database-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c08-sftp-landing.png](screenshots/core/c08-sftp-landing.png)<br>1725x832 | ไฟล์ movement ใน execution-scoped Landing และโฟลเดอร์ปี/เดือน; ไม่พิสูจน์ Binary/byte equality | `docs/guides/sftp-file-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c09-sftp-bronze-lineage.png](screenshots/core/c09-sftp-bronze-lineage.png)<br>1613x460 | parsed business rows และ source-file lineage; IDs ถูกตัดและเป็นคนละ DEV example กับ C12 | `docs/guides/sftp-file-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c14-ambiguous-run-scope.png](screenshots/core/c14-ambiguous-run-scope.png)<br>1733x893 | AMBIGUOUS_RUN_SCOPE ที่ fail_ambiguous_run_scope; validation error ชัดและตรง master definition | `docs/operations/run-request-examples.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c15-operations-report.png](screenshots/core/c15-operations-report.png)<br>1655x928 | terminal object audits: 2 sources / 2 objects / 0 failed sources; history SUCCESS/SKIPPED และ REGULAR/BACKFILL | `README.md`; `docs/operations/monitoring-report.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c16-operations-filter.png](screenshots/core/c16-operations-filter.png)<br>1655x928 | LOGISTICS_VENDOR filter: latest batch หนึ่ง object และ history สี่รายการ; เพิ่ม evidence ด้าน filter ที่ C15 ไม่มี | `docs/operations/monitoring-report.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |

### performance

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [p02-query-none.png](screenshots/performance/p02-query-none.png)<br>1721x913 | AUTO Copy Succeeded, 10M rows, Total 00:05:16, 40.753 MB/s, used copies 1; resolved partitioning ไม่ปรากฏ | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [p03-query-dynamic-range-auto.png](screenshots/performance/p03-query-dynamic-range-auto.png)<br>1721x913 | AUTO Copy Succeeded, 10M rows, Total 00:04:33, 47.011 MB/s, used copies 4; ไม่ใช่ completed result ของ PoC เก่า | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [p04-query-dynamic-range-tuned.png](screenshots/performance/p04-query-dynamic-range-tuned.png)<br>1721x913 | TUNED Copy Succeeded, 10M rows, Total 00:02:34, 85.388 MB/s, used copies 4; ไม่พิสูจน์สาเหตุความเร็วต่าง | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |

### performance/source-config

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [px-s8-b1-config.png](screenshots/performance/source-config/px-s8-b1-config.png)<br>1412x76 | config 10 active / 9 inactive, NONE และไม่มี override; เป็น metadata snapshot | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [px-s8-b2-config.png](screenshots/performance/source-config/px-s8-b2-config.png)<br>1414x76 | DYNAMIC_RANGE บน event_date และไม่มี override; AUTO interpretation มาจาก routing implementation | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [px-s8-b3-config.png](screenshots/performance/source-config/px-s8-b3-config.png)<br>1414x76 | DYNAMIC_RANGE บน event_date พร้อม requested override 4; ไม่ใช่ observed runtime parallelism | `docs/architecture/database-copy-performance.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |

### supporting/s1-orchestration

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-s1-config-pagination-detail-1.png](screenshots/supporting/s1-orchestration/cx-s1-config-pagination-detail-1.png)<br>1733x918 | Lookup แสดง active configs 8 / pages 4 และ repeated dispatch; ชัดกว่า overview เปล่า | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-config-pagination-detail-2.png](screenshots/supporting/s1-orchestration/cx-s1-config-pagination-detail-2.png)<br>1733x918 | Dispatcher input แสดง page requests config 7/8 แบบ REGULAR; เพิ่ม payload detail จาก pagination figure | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-config-pagination.png](screenshots/supporting/s1-orchestration/cx-s1-config-pagination.png)<br>1733x918 | overview และ activity list ทับกับ detail-1 ที่เผยแพร่; ไม่มี payload ใหม่ แต่เก็บไว้รอ owner ตัดสิน archive | ไม่มี published embed | `REDUNDANT_ARCHIVE_CANDIDATE` — ซ้ำเชิง presentation; คงไฟล์ไว้รอ owner ตัดสิน |
| [cx-s1-database-router-detail-1.png](screenshots/supporting/s1-orchestration/cx-s1-database-router-detail-1.png)<br>1733x918 | route expression SQL_SERVER/FULL และ FULL adapter invocation; ไม่ได้แสดง INCREMENTAL execution | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-database-router-detail-2.png](screenshots/supporting/s1-orchestration/cx-s1-database-router-detail-2.png)<br>1733x918 | FULL adapter input มี config/run context; useful correlation lead แต่ไม่ใช่ independent full trace | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-database-router.png](screenshots/supporting/s1-orchestration/cx-s1-database-router.png)<br>1733x918 | switch และ FULL invocation ทับกับ detail-1; ไม่มี expression popup เพิ่มเติม จึงไม่เพิ่มเป็น figure | ไม่มี published embed | `REDUNDANT_ARCHIVE_CANDIDATE` — ซ้ำเชิง presentation; คงไฟล์ไว้รอ owner ตัดสิน |
| [cx-s1-dispatcher-execution-detail.png](screenshots/supporting/s1-orchestration/cx-s1-dispatcher-execution-detail.png)<br>1733x918 | Controller invocation input แสดง config 8 / REGULAR / optional bounds; overview ไม่มี payload นี้ | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-dispatcher-execution.png](screenshots/supporting/s1-orchestration/cx-s1-dispatcher-execution.png)<br>1733x918 | Object Controller สอง invocations เริ่มวินาทีเดียวกัน; ไม่พิสูจน์ eight-way concurrency | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-file-router-detail-1.png](screenshots/supporting/s1-orchestration/cx-s1-file-router-detail-1.png)<br>1733x918 | SFTP/INCREMENTAL route หลัง file-format check; ไม่ได้แสดง FULL execution | `docs/guides/sftp-file-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-file-router-detail-2.png](screenshots/supporting/s1-orchestration/cx-s1-file-router-detail-2.png)<br>1733x918 | SFTP adapter input ให้ config/run context ที่ route-output figure ไม่มี; ยังไม่ใช้ยืนยัน end-to-end linkage | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-file-router.png](screenshots/supporting/s1-orchestration/cx-s1-file-router.png)<br>1733x918 | route graph/activity list ทับกับ detail-1; selected figure แสดง expression เพิ่มจึงชัดกว่า | ไม่มี published embed | `REDUNDANT_ARCHIVE_CANDIDATE` — ซ้ำเชิง presentation; คงไฟล์ไว้รอ owner ตัดสิน |
| [cx-s1-master-orchestration-detail.png](screenshots/supporting/s1-orchestration/cx-s1-master-orchestration-detail.png)<br>1733x918 | Paginator invocation input แสดง page-size 2 และ blank source scope; มี physical bindings จึงไม่เพิ่มเป็น public figure | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-object-controller-database-detail.png](screenshots/supporting/s1-orchestration/cx-s1-object-controller-database-detail.png)<br>1733x918 | Lookup output แสดง DATABASE config และ physical connection binding; เก็บเพื่อ source interpretation ไม่เผยแพร่เพิ่ม | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-object-controller-database.png](screenshots/supporting/s1-orchestration/cx-s1-object-controller-database.png)<br>1733x918 | lookup/request checks ตามด้วย DATABASE Router; คู่กับ FILE เป็น routing alternatives | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-object-controller-file-detail.png](screenshots/supporting/s1-orchestration/cx-s1-object-controller-file-detail.png)<br>1733x918 | Lookup output แสดง FILE config และ physical connection binding; เพิ่ม metadata-resolution detail แต่ไม่เพิ่ม figure | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-object-controller-file.png](screenshots/supporting/s1-orchestration/cx-s1-object-controller-file.png)<br>1733x918 | lookup/request checks ตามด้วย FILE Router; ไม่ใช่ขั้นต่อจาก DATABASE ใน execution เดียว | `docs/guides/pipeline-orchestration.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-sftp-incremental-adapter-1.png](screenshots/supporting/s1-orchestration/cx-s1-sftp-incremental-adapter-1.png)<br>1733x918 | graph ช่วง watermark support/state/boundary checks ชัดกว่าช่วง Copy ของ adapter-2; เก็บ supporting view | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-sftp-incremental-adapter-2.png](screenshots/supporting/s1-orchestration/cx-s1-sftp-incremental-adapter-2.png)<br>1733x918 | Copy/file-count gate/Notebook/finalizer activities สำเร็จ; activity success ไม่เท่ากับ terminal audit SUCCESS | `docs/guides/sftp-file-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [cx-s1-sftp-incremental-adapter-detail-1.png](screenshots/supporting/s1-orchestration/cx-s1-sftp-incremental-adapter-detail-1.png)<br>1733x918 | Lookup output แสดง initial watermark และ null success references; ไม่ใช่ S4 before capture | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-sftp-incremental-adapter-detail-2.png](screenshots/supporting/s1-orchestration/cx-s1-sftp-incremental-adapter-detail-2.png)<br>1733x918 | Notebook input แสดง file pattern/delimiter/encoding/target schema; เป็น parser options ไม่ใช่ runtime row result | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-sql-server-full-adapter-detail.png](screenshots/supporting/s1-orchestration/cx-s1-sql-server-full-adapter-detail.png)<br>1733x918 | Copy input แสดง query และ CAST lineage/timestamp; ไม่จำเป็นต้องเพิ่มเมื่อ C05 สรุปผลอยู่แล้ว | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |
| [cx-s1-sql-server-full-adapter.png](screenshots/supporting/s1-orchestration/cx-s1-sql-server-full-adapter.png)<br>1733x918 | graph finalizer/compensation ไม่ถูก Copy drawer บังเหมือน C05; เก็บโดยไม่อ้างว่า failure branches ถูก execute | ไม่มี published embed | `UNIQUE_SUPPORTING_EVIDENCE_KEEP` — มี detail เฉพาะ แต่ยังไม่จำเป็นต้องเพิ่ม figure |

### supporting/s2-no-new-data

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-s2-no-bronze-append.png](screenshots/supporting/s2-no-new-data/cx-s2-no-bronze-append.png)<br>1413x76 | Bronze result ศูนย์สอง objects แต่ query/filter ไม่เห็น; ชื่อไฟล์เป็น intent ไม่ใช่ proof of no append | ไม่มี published embed; source: C10 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s2-skipped-audit.png](screenshots/supporting/s2-no-new-data/cx-s2-skipped-audit.png)<br>1409x76 | SKIPPED สองแถว 0/0 และ processing bounds; run type ไม่เห็นและ Run IDs ถูกตัด | ไม่มี published embed; source: C10 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s2-watermark-after.png](screenshots/supporting/s2-no-new-data/cx-s2-watermark-after.png)<br>1409x76 | duplicate ของ before; ไม่แสดงซ้ำแต่ manifest/build ต้องตรวจ equality และเก็บ provenance | ไม่มี published embed; source: C10 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s2-watermark-before.png](screenshots/supporting/s2-no-new-data/cx-s2-watermark-before.png)<br>1409x76 | watermark สอง configs; bytes เหมือน after จึงแสดง state ครั้งเดียวใน C10 | ไม่มี published embed; source: C10 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |

### supporting/s3-sql-incremental

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-s3-audit-success.png](screenshots/supporting/s3-sql-incremental/cx-s3-audit-success.png)<br>1409x124 | SUCCESS สี่แถวพร้อม LOW/HIGH และ counts; run_type ไม่อยู่ในภาพ | ไม่มี published embed; source: C11 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s3-watermark-after.png](screenshots/supporting/s3-sql-incremental/cx-s3-watermark-after.png)<br>1409x124 | later checkpoint values สี่ configs advance ตรง audit HIGH; ไม่ใช่ independent REGULAR proof | ไม่มี published embed; source: C11 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s3-watermark-before.png](screenshots/supporting/s3-sql-incremental/cx-s3-watermark-before.png)<br>1409x124 | earlier checkpoint values สี่ configs สอดคล้อง audit LOW; exact run linkage ไม่ยืนยัน | ไม่มี published embed; source: C11 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |

### supporting/s4-sftp-incremental

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-s4-audit-success.png](screenshots/supporting/s4-sftp-incremental/cx-s4-audit-success.png)<br>1409x52 | inventory_movement SUCCESS 6/6 และ processing bounds; Run ID ถูกตัด | ไม่มี published embed; source: C12 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s4-bronze-new-file-lineage.png](screenshots/supporting/s4-sftp-incremental/cx-s4-bronze-new-file-lineage.png)<br>1410x172 | Bronze หกแถวพร้อม source-file และ run lineage; Batch ID ตรง after-state ที่แสดง | ไม่มี published embed; source: C12 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s4-watermark-after.png](screenshots/supporting/s4-sftp-incremental/cx-s4-watermark-after.png)<br>1409x52 | later FILE checkpoint advance; remote file Last Modified ไม่ปรากฏในชุดภาพ | ไม่มี published embed; source: C12 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s4-watermark-before.png](screenshots/supporting/s4-sftp-incremental/cx-s4-watermark-before.png)<br>1409x52 | earlier FILE last_modified_time checkpoint ของ config 8 | ไม่มี published embed; source: C12 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |

### supporting/s5-backfill

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-s5-audit-backfill.png](screenshots/supporting/s5-backfill/cx-s5-audit-backfill.png)<br>1413x52 | BACKFILL / INCREMENTAL / SUCCESS 2/2; LOW/HIGH และ Batch ID ถูกตัด | ไม่มี published embed; source: C13 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s5-watermark-after.png](screenshots/supporting/s5-backfill/cx-s5-watermark-after.png)<br>1409x52 | duplicate provenance ที่ builder ต้องตรวจ; ไม่ใช่ independent non-advancement observation | ไม่มี published embed; source: C13 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-s5-watermark-before.png](screenshots/supporting/s5-backfill/cx-s5-watermark-before.png)<br>1409x52 | checkpoint state หนึ่งแถว; before/after bytes เท่ากัน แสดงเพียงครั้งเดียว | ไม่มี published embed; source: C13 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |

### supporting/optional/o01-end-to-end

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-o01-audit.png](screenshots/supporting/optional/o01-end-to-end/cx-o01-audit.png)<br>1409x52 | REGULAR category SUCCESS audit 20/20; IDs ถูกตัด จึงยังไม่มี audit-to-Bronze และ parent/child linkage ครบ | ไม่มี published embed | `PENDING_ADDITIONAL_EVIDENCE` — ยังไม่ integrate และไม่สร้าง composite |

### supporting/optional/o02-file-row-count

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-o02-binary-copy.png](screenshots/supporting/optional/o02-file-row-count/cx-o02-binary-copy.png)<br>1731x913 | Copy detail มี filesRead/filesWritten 1/1; crop เก็บชื่อ activity/source/sink/metrics โดยไม่เก็บ activity ID | ไม่มี published embed; source: O02 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |
| [cx-o02-notebook-parse.png](screenshots/supporting/optional/o02-file-row-count/cx-o02-notebook-parse.png)<br>1731x913 | Notebook Output มี source/target counts 6/6; genuine strips จำเป็นต่อ O02 ที่ขยาย 2x โดยไม่ reflow | ไม่มี published embed; source: O02 | `COMPOSITE_SOURCE_KEEP` — จำเป็นต่อ reproducibility/provenance; ห้ามลบ |

### supporting/optional/o05-source-scope

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [cx-o05-batch-audit.png](screenshots/supporting/optional/o05-source-scope/cx-o05-batch-audit.png)<br>1409x76 | REGULAR SUCCESS 12/12 และ SKIPPED 0/0; Batch/Run IDs ถูกตัด จึงยังเชื่อม input ไม่ครบ | ไม่มี published embed | `PENDING_ADDITIONAL_EVIDENCE` — ยังไม่ integrate และไม่สร้าง composite |
| [cx-o05-paginator-selection.png](screenshots/supporting/optional/o05-source-scope/cx-o05-paginator-selection.png)<br>1733x918 | page selection count 2 และ REGULAR configs 7/8; source scope สอดคล้องแต่ไม่ยืนยัน exact execution linkage | ไม่มี published embed | `PENDING_ADDITIONAL_EVIDENCE` — ยังไม่ integrate และไม่สร้าง composite |
| [cx-o05-source-scope-input.png](screenshots/supporting/optional/o05-source-scope/cx-o05-source-scope-input.png)<br>1733x918 | input ระบุ LOGISTICS_VENDOR และ page size 1000; มี physical bindings และยังขาด exact child/audit linkage | ไม่มี published embed | `PENDING_ADDITIONAL_EVIDENCE` — ยังไม่ integrate และไม่สร้าง composite |

### diagrams

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [d01-control-audit-er.svg](diagrams/d01-control-audit-er.svg)<br>1840x1326 | selected fields ของสี่ตาราง, enforced FK และ logical non-FK audit association; คง finalized SVG | `docs/guides/control-plane.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [d02-environment-binding.svg](diagrams/d02-environment-binding.svg)<br>1900x1265 | five runtime String IDs แยกจาก metadata bindings และ permissions; UAT/PROD เป็น design only | `docs/operations/variable-library-environment-binding.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |

### composites

| Asset / pixels | Evidence / limitation | Published figure / composite dependency | Decision / justification |
| --- | --- | --- | --- |
| [c11-sql-server-incremental.png](screenshots/composites/c11-sql-server-incremental.png)<br>1449x758 | SUCCESS audits สี่แถวมี bounds สอดคล้องกับ checkpoint captures ที่ advance; run type/exact correlation ไม่ยืนยัน | `docs/guides/sql-server-database-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c12-sftp-new-file-incremental.png](screenshots/composites/c12-sftp-new-file-incremental.png)<br>1450x804 | SUCCESS 6/6 audit, Bronze lineage หกแถว และ checkpoint values ต่างกัน; exact correlation ไม่ยืนยัน | `docs/guides/sftp-file-ingestion.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [o02-file-vs-row-count.png](screenshots/composites/o02-file-vs-row-count.png)<br>1362x680 | Copy files 1/1 เทียบ Notebook rows 6/6; shared DataFrame count ไม่ใช่ independent Bronze recount | `docs/architecture/file-ingestion-design.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c10-no-new-data-skipped.png](screenshots/composites/c10-no-new-data-skipped.png)<br>1453x664 | SKIPPED 0/0 audits พร้อม Bronze count ที่ไม่เห็น query และ duplicate watermark state หนึ่ง panel | `docs/architecture/generic-incremental-watermark.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |
| [c13-incremental-backfill.png](screenshots/composites/c13-incremental-backfill.png)<br>1453x508 | BACKFILL run_type / INCREMENTAL load_strategy / SUCCESS 2/2; duplicate state ไม่พิสูจน์ non-advancement | `docs/operations/retry-rerun-backfill.md` | `DIRECT_USE` — ให้ evidence ต่างจาก prose/diagram; คงตำแหน่งและ full-size link |


### Architecture overview — outside the 65-row inventory

[`architecture-overview.svg`](architecture-overview.svg), 1440x1220: `DIRECT_USE`; README ใช้อธิบาย logical responsibilities และ SQL/SFTP paths ชื่อไฟล์ชัดเจน คง original SVG และเพิ่ม explicit full-size link ภาพนี้เสริม C15 ซึ่งแสดง persisted audit report ไม่ซ้ำกัน

## Composite presentation: before / after

ทั้งห้าภาพเปลี่ยน generic main title เป็น subject; ย้าย candidate ID ไป subtitle ขนาดเล็กที่ระบุ DEV evidence composite ชัดเจน ใช้ heading 30 px / panels 23 px / notes 18 px พร้อมเส้นแบ่งบางแทนกล่องเทาหนัก คง source pixels, native sizes และ spacing สำหรับ C10–C13 ไม่เติม timeline arrows เลือก ASCII separators เพื่อไม่เกิด missing glyph ใน bundled font


### C10

- Title BEFORE: `C10 | Composite of DEV evidence`
- Title AFTER: `No New Data - SKIPPED Audit and Checkpoint Context`
- Subtitle BEFORE: `SKIPPED audit and checkpoint context - not a verified execution trace.`
- Subtitle AFTER: `C10 · DEV evidence composite`
- Panel labels BEFORE: `1. SKIPPED Audit Records`, `2. Bronze Count Result | Query Scope Not Shown`, `3. Watermark State | Identical Before/After Source Files`
- Numbering: ตัดเลขลำดับทั้งหมด; panels เป็น evidence context ไม่ใช่ proven correlated timeline
- Panel labels AFTER: audit และ `Watermark state - duplicate source files shown once`; C10 มี `Bronze count result - query scope not shown` เพิ่ม คง duplicate state ครั้งเดียว
- Notes BEFORE: `Watermark before/after source files are byte-identical; independent state observations are not verified.` / `The Bronze query/filter is not visible; its zero count does not independently prove no append.` / `Run type is not shown and some Run IDs are truncated; exact execution correlation is not verified.`
- Notes AFTER: `Byte-identical watermark source files do not establish independent before/after observations.` / `Bronze query/filter is not visible; the zero count does not independently prove no append.` / `Run type is not shown; some Run IDs are truncated. Exact execution correlation is unverified.`
- Output: `1453x664`; full-size link เดิมยังใช้ได้


### C11

- Title BEFORE: `C11 | Composite of DEV evidence`
- Title AFTER: `SQL Server Incremental - Audit and Watermark Evidence`
- Subtitle BEFORE: `Audit and checkpoint comparison - not a single-run execution trace.`
- Subtitle AFTER: `C11 · DEV evidence composite`
- Panel labels BEFORE: `1. Watermark Before`, `2. SUCCESS Audit Records`, `3. Watermark After`
- Numbering: ตัดเลขลำดับทั้งหมด; panels เป็น evidence context ไม่ใช่ proven correlated timeline
- Panel labels AFTER: `Earlier checkpoint capture`, `SUCCESS audit records`, `Later checkpoint capture`; คง order และ timestamps เดิม แต่ไม่ผูกเป็น execution เดียว
- Notes BEFORE: `Run type is not visible; exact execution correlation is not independently verified.`
- Notes AFTER: `Run type is not visible; exact execution correlation is not independently verified.`
- Output: `1449x758`; full-size link เดิมยังใช้ได้


### C12

- Title BEFORE: `C12 | Composite of DEV evidence`
- Title AFTER: `SFTP Incremental - Bronze Lineage and Checkpoint Context`
- Subtitle BEFORE: `Audit, Bronze lineage and checkpoint comparison - not a single-run trace.`
- Subtitle AFTER: `C12 · DEV evidence composite`
- Panel labels BEFORE: `1. Watermark Before`, `2. SUCCESS Audit Record`, `3. Bronze Source-File Lineage`, `4. Watermark After`
- Numbering: ตัดเลขลำดับทั้งหมด; panels เป็น evidence context ไม่ใช่ proven correlated timeline
- Panel labels AFTER: `Earlier checkpoint capture`, audit/lineage, `Later checkpoint capture`; คง order และ timestamps เดิม แต่ไม่ผูกเป็น execution เดียว
- Notes BEFORE: `Run type is not visible; some run identifiers are truncated. Exact execution correlation is not independently verified.` / `Remote file Last Modified values are not visible.` / `C08/C09 depict a different DEV execution example.`
- Notes AFTER: `Run type is not visible; some run identifiers are truncated. Exact execution correlation is not independently verified.` / `Remote file Last Modified values are not visible.` / `C08/C09 depict a different DEV execution example.`
- C12 แสดง run-type/truncation/correlation note บนภาพ ส่วน remote Last Modified ไม่ปรากฏและ C08/C09 เป็นอีก example เก็บใน manifest และ surrounding guide context
- Output: `1450x804`; full-size link เดิมยังใช้ได้


### C13

- Title BEFORE: `C13 | Composite of DEV evidence`
- Title AFTER: `BACKFILL - Audit and Checkpoint Evidence`
- Subtitle BEFORE: `BACKFILL audit and checkpoint context - not independent before/after evidence.`
- Subtitle AFTER: `C13 · DEV evidence composite`
- Panel labels BEFORE: `1. BACKFILL INCREMENTAL SUCCESS Audit Record`, `2. Watermark State | Identical Before/After Source Files`
- Numbering: ตัดเลขลำดับทั้งหมด; panels เป็น evidence context ไม่ใช่ proven correlated timeline
- Panel labels AFTER: audit และ `Watermark state - duplicate source files shown once`; คง duplicate state ครั้งเดียว
- Notes BEFORE: `Watermark source files are byte-identical; independent before/after observations are not verified.` / `Audit LOW/HIGH and Batch ID are truncated; missing values and identifiers have not been reconstructed.` / `Checkpoint non-advancement, Bronze append and exact execution correlation are not independently verified.` / `This evidence does not establish exactly-once business semantics.`
- Notes AFTER: `Byte-identical watermark source files do not establish independent before/after observations.` / `Audit LOW/HIGH and Batch ID are truncated; the complete processing window is unavailable.` / `Checkpoint non-advancement, Bronze append and exact execution correlation are unverified.` / `Exactly-once business semantics are not established.`
- Output: `1453x508`; full-size link เดิมยังใช้ได้


### O02

- Title BEFORE: `O02 | Composite of DEV evidence`
- Title AFTER: `SFTP Ingestion - Files Transferred vs Rows Parsed`
- Subtitle BEFORE: `File-transfer metrics and parsed-row metrics from selected source UI crops.`
- Subtitle AFTER: `O02 · DEV evidence composite · selected UI excerpts`
- Numbering: เดิมไม่มี และยังไม่มี; เป็น comparison สองหน่วยวัด
- Layout: Binary Copy crop เดิมทุก pixel; Notebook metrics ใช้ crop boxes เดิมและ shared 2x NEAREST transform เพื่ออ่านง่าย ไม่ reflow หรือ reconstruct tokens; activity/Output context ยังคงเป็น separate crops ลดความสูงจาก 726 เป็น 680 px และย่อ explanatory labels สองบรรทัดเหลือหนึ่งบรรทัด
- Notes BEFORE: `Both Notebook row metrics reuse the same parsed DataFrame count.` / `They are not an independent Bronze recount.` / `End-to-end execution correlation is not independently verified.`
- Notes AFTER: `Notebook row metrics share one parsed DataFrame count; no independent Bronze recount.` / `Exact end-to-end execution correlation is not independently verified.`
- Output: `1362x680`; full-size link เดิมยังใช้ได้

## Markdown figure review

ตรวจ subject, preceding text, captions, technical scope, duplication และ full-size access ของทุก figure ตำแหน่งเดิมเหมาะสมจึงไม่มีการย้าย figure

| Page | Figures reviewed | Result |
| --- | --- | --- |
| `README.md` | Architecture overview, C15 | คงสองภาพ; เพิ่ม intro และ explicit overview link; C15 reuse เหมาะกับ landing page |
| `docs/guides/control-plane.md` | D01, C01, C02 | selected-field model และ DEV mapping แยกจาก execution proof; unchanged |
| `docs/guides/pipeline-orchestration.md` | C03, C04 Pagination/Dispatcher/Controller DATABASE+FILE/Database Routing | คง original images; controller คู่ใช้ shared caption; Mermaid เป็น concept ภาพเป็น observed activities |
| `docs/guides/sql-server-database-ingestion.md` | C05, C11, C06 | คง FULL/advance/result placement; เพิ่ม figure introduction และตัดคำ Composite ที่ซ้ำจาก C11 caption |
| `docs/guides/sftp-file-ingestion.md` | C07 Router, C08, C07 Adapter, C09, C12 | คง route/Copy/lineage placement และคำอธิบาย different DEV examples; ย่อ C12 caption prefix |
| `docs/architecture/generic-incremental-watermark.md` | C10 | คง Finalization placement และ caveats; เพิ่ม figure introduction และย่อ caption prefix |
| `docs/operations/retry-rerun-backfill.md` | C13 | คง Audit semantics placement และ run_type/load_strategy distinction; เพิ่ม figure introduction และย่อ caption prefix |
| `docs/operations/run-request-examples.md` | C14 | error ชัดเจนและตรง validation section; unchanged |
| `docs/architecture/database-copy-performance.md` | P01 B1/B2/B3, P02/P03/P04 | คง original vertical images, full-size links และ P05 QUALIFIED Markdown table; no speedup claim |
| `docs/operations/monitoring-report.md` | C15, C16 | overview/filter ให้ independent value; terminal audits และ acceptance snapshots แยกชัด; unchanged |
| `docs/operations/variable-library-environment-binding.md` | D02 | scope/runtime bindings ไม่ปะปน metadata; design-only qualification คงเดิม |
| `docs/architecture/file-ingestion-design.md` | O02 | caption ระบุ source/target 6/6 ชัดขึ้น; อธิบาย 2x excerpt และ no exact correlation |

## Readability and evidence boundaries

Original DIRECT screenshots ยังต้องใช้ full-size links เพื่ออ่าน activity names/columns บน GitHub; การลดขนาดหน้าเว็บไม่เพิ่มข้อมูล source ที่ถูกตัด C08 มีพื้นที่ว่างมาก แต่ tree/file context จำเป็นและยังใช้ original ตาม prior approval C06/C09 เป็น visible row samples ไม่ใช่ total counts P01 เป็น narrow metadata tables จึงไม่รวมเป็น collage

ไม่พบเหตุให้แก้ D01/D02: selected-field relationships และ design-only labels ถูกต้อง SVG render ใช้ตรวจ full extent โดยไม่แก้ original bytes Screenshot review พบ operational IDs และบาง supporting input มี physical bindings; ไม่ถอด identifiers เหล่านั้นลงรายงาน ไม่ได้ทำ broad privacy re-audit และไม่มีข้ออ้างว่า current tree/history ถูก sanitize แล้ว

Implementation cross-check ใช้ current Pipeline activity names/routing, AUTO property omission, finalizer optimistic watermark update และ Notebook shared DataFrame count ไม่มีการอ้าง runtime success ใหม่ Audit SUCCESS ไม่แทนด้วย Pipeline Succeeded; no-new-data และ BACKFILL screenshots ไม่ถูกใช้ยืนยัน unseen Bronze operations หรือ exactly-once semantics

## Retention and owner decisions

เก็บครบทุกไฟล์ใน matrix และ overview; removed = 0, renamed = 0 ไม่มี builder/source/manifest ถูก orphan O01/O05 คง pending ไม่สร้างภาพใหม่ O03/O04 ยัง excluded และไม่มีการเพิ่มกลับ ทั้งสาม archive candidates เป็นข้อเสนอเชิง presentation เท่านั้น ยังเก็บ raw sources ไว้ทั้งหมดและไม่ย้าย path จน owner ตัดสิน

Owner review ที่เหลือ: approve รูปแบบ composites ทั้งห้า โดยเฉพาะ O02 ที่ยังเห็น escaped serialized JSON และ original line wrap (หากต้องการ UI ที่ไม่มี escaping ต้อง capture ใหม่ ไม่ควรจัด token ใหม่); ตัดสิน archive candidates สามไฟล์; จัดหา exact correlation/Bronze evidence สำหรับ O01/O05 หากต้องการ publish ในอนาคต Final handoff cleanup และ canonical privacy remediation ไม่อยู่ในรอบนี้

## Reproduction and validation

ใช้ Python/Pillow 11.3.0 กับ `scripts/evidence/build_c11_composite.py`, `scripts/evidence/build_sftp_composites.py`, `scripts/evidence/build_incremental_composites.py` ครบห้า outputs Adjacent manifests เก็บ source hashes/dimensions/placements และ limitations; O02 เพิ่ม scale/resampling metadata C10/C13 ยังตรวจ duplicate bytes และเก็บ source paths ทั้งสอง

Validation: run builders สองรอบและเทียบ PNG/manifest SHA-256, ตรวจ source hashes/dimensions และ placement pixels (รวม NEAREST 2x ของ O02), ตรวจ originals กับ baseline, Markdown image/full-size links และ local anchors, ตรวจ exact Git diff scope ไม่มี Fabric/SQL/Notebook/Library implementation changes Static checks ไม่รับรอง fresh runtime deployment


ผล validation ที่ดำเนินการแล้ว:

| Check | Result |
| --- | --- |
| Five PNGs + five manifests, rebuild two rounds | SHA-256 byte-identical |
| Source placements | 17 exact pixel comparisons รวม O02 2x NEAREST |
| Original visuals | 61 files byte-identical to baseline (58 PNGs + D01/D02 + overview) |
| Fabric/SQL implementation files | 98 files unchanged |
| Markdown local destinations and anchors | 284 checked |
| Published image/full-size links | 32 placements / 31 unique assets / 12 pages |
| Deletion / rename | 0 / 0 |
| Final visual acceptance | Pending owner review |
