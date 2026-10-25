# Project Handoff — Fabric Metadata-Driven Pipelines Portfolio

> **Initial working snapshot:** 2026-10-25 (Asia/Bangkok); verify live GitHub HEAD before continuing  
> **Purpose:** Preserve the implementation boundary, prior design decisions, evidence inventory, documentation strategy, and next actionable work when continuing in a new ChatGPT conversation.  
> **Scope:** Personal GitHub portfolio only, separate from client delivery work.  
> **Storage:** Temporary public `.project-handoff/` folder. Do not publish credentials or private environment-specific identifiers.  
> **Status at handoff:** Framework and D01/D02 diagrams are complete for the current portfolio scope; 58 original screenshots and 2 SVG diagrams are preserved, with derived composites C10, C11, C12, C13, and O02 now added. **Batches A–G are merged into `main` through `eb4ce0c`. Batch H (finalized D02 environment-binding SVG) is owner-approved and integrated unchanged on `docs/evidence-curation`; its merge and Final Portfolio QA are pending. P05 remains a QUALIFIED descriptive Markdown table, not an image artifact. O01/O05 remain pending additional correlation evidence; O05 also requires privacy-safe presentation.**

## 0. How to use this handoff

1. In a new conversation, read `PROJECT_HANDOFF.md`, `EVIDENCE_INVENTORY.csv`, `SCREENSHOT_IMPLEMENTATION_PLAN.md`, and `CONTINUATION_PROMPT.md` directly from the live GitHub `.project-handoff/` folder rather than relying on old downloaded copies.
2. Inspect the **current** GitHub repository and branch/commit before changing files. The SHAs and counts here describe a snapshot, not a permanent lock.
3. Prioritize a **filename-first, low-effort, batch-by-batch review**. Don't open all 58 screenshots just to re-infer categories already established.
4. Never confuse **a file's presence** with evidence acceptance, nor **a planned/composite artifact** with an artifact that exists.
5. Don't begin redesigning the completed architecture, D01, or D02 unless an actual technical inconsistency is found.
6. The user authorized this sanitized temporary working handoff in the public GitHub repository. Do not commit detailed private evidence logs, credentials, secret values, or private environment-specific IDs. It is working context, not portfolio documentation.

## 1. Project identity and source of truth

- **Repository:** `https://github.com/getnkit/fabric-metadata-driven-pipelines`
- **Branch last checked:** `main`
- **Pre-handoff HEAD:** `9f17c1b2caab2488efbb994cbf085abf21b5c227` (historical baseline, not a permanent HEAD)
- **Most recent organizing commit:** `docs: organize evidence screenshots by scenario and category`
- **Preceding asset-upload commit:** `83d58c3431ac70311998e653c265f46b4596d13b`, `docs: add evidence screenshots and technical diagrams`
- **Owner/account:** Personal GitHub account `getnkit`. Use this personal repository rather than a separate work account.
- **Local synchronization after assistant's direct GitHub commit:** `git pull --ff-only origin main` (only if local worktree is clean/fast-forward is applicable).
- **GitHub is authoritative** for checked-in code, item definitions, docs, and committed assets. This handoff is authoritative for discussion decisions, intended evidence handling, user preferences, and the snapshot status—not a substitute for source-code verification.

**Do not mix projects:** This personal portfolio is separate from client delivery work. Do not introduce client information, credentials, client connection IDs, or unverifiable claims into the public repository.

## 2. Core goal and architecture (checked against current README/design guide)

Goal: Show how to implement **reusable, metadata-driven batch ingestion** in Microsoft Fabric from SQL Server and SFTP sources, with centrally managed configuration, audited object runs, safe incremental checkpoints, failure compensation, and operational monitoring.

### Logical responsibility groups

| Group | Technology | Responsibility |
|---|---|---|
| Control & Audit | Microsoft Fabric SQL Database | `control.connection_settings`, `control.ingestion_config`, `control.pipeline_watermarks`, `audit.ingestion_log`; validation/finalization procedures; read-only monitoring views |
| Orchestration | Microsoft Fabric Data Factory Data Pipelines | Request selection, active-config pagination, dispatcher, per-object validation and DATABASE/FILE routing, physical adapters, recovery |
| Data | Fabric Lakehouse (Bronze Delta), source-specific Copy/Notebook | SQL Server query-mode Copy to Bronze; SFTP Binary Copy to Landing, then Notebook parse/append to Bronze |

The three groups are **logical responsibilities**, not isolated systems. No claim of cross-service distributed transaction. `README.md` already contains an architecture overview illustration (`docs/assets/architecture-overview.svg`) and reviewed navigation; **do not rewrite README wholesale**.

### Implemented pipeline graph (check code for exact behavior)

- Entry: `pl_ingest_orchestrator` (supported external entry point).
- Select active configs: `pl_ingest_config_paginator` → `pl_ingest_config_dispatcher` → `pl_ingest_object_controller`.
- Route DATABASE: `pl_ingest_database_router` → `pl_ingest_sql_server_full_adapter` **or** `pl_ingest_sql_server_incremental_adapter` → `pl_ingest_sql_server_incremental_loader` (for INCREMENTAL).
- Route FILE: `pl_ingest_file_router` → `pl_ingest_sftp_full_adapter` **or** `pl_ingest_sftp_incremental_adapter`.
- Conditional incremental-finalization recovery: `pl_ingest_incremental_finalize_recovery` (not generally attached to FULL paths).
- Notebooks: `nb_load_file_landing_to_bronze`, `nb_cleanup_bronze_batch_rows`, `nb_cleanup_landing_batch_files`.

Source adapters are implemented for **SQL Server** and **SFTP** only. File parsing currently supports **`DELIMITED_TEXT`**; do not imply active JSON/Parquet, Oracle, Kafka/streaming, etc. SQL Server uses Copy rather than forcing Spark for relational extraction. The `p_source_system` optional source filter and `p_run_requests` array are different dispatch modes; combining nonempty explicit requests with nonblank source scope yields `AMBIGUOUS_RUN_SCOPE`.

### Semantics that must not drift

- Two independent dimensions:
  - Configured `load_strategy`: `FULL | INCREMENTAL`
  - Execution `run_type`: `REGULAR | BACKFILL`
- **`RERUN` is not a framework run_type.** Fabric Retry/Rerun is a separate platform execution recovery concept.
- **REGULAR + INCREMENTAL:** obtains committed LOW, determines source/run HIGH, advances the watermark only after eligible successful SQL finalization.
- **BACKFILL + INCREMENTAL:** uses requested historical LOW/HIGH, appends a new Bronze batch, **never advances operational watermark**.
- **FULL (REGULAR or BACKFILL):** appends current full source scope; no incremental checkpoint. BACKFILL FULL is *not* historical point-in-time snapshot.
- **No-new-data SKIPPED:** no Bronze append, no checkpoint advancement.
- **Bronze append-only for successful batches**; an overlapping replay may append a separate batch. Never claim global exactly-once business-record semantics.
- **Compensating cleanup on failure** scopes to **both** `_batch_id` and `_pipeline_run_id`. Distinguish a physical write failure from a possibly committed SQL finalizer whose activity reported failure; recover using durable audit outcome. Don't call it a distributed transaction.
- SQL Server timestamp `_ingestion_timestamp` is typed from source query (`DATETIME2(3)`); FILE reader uses Notebook-generated ingestion metadata. FILE incremental checkpoint based on remote file last-modified timestamp, not CSV payload date.

### Monitoring caveats

- Git-tracked Power BI items: `sm_ingestion_operations` and `rpt_ingestion_operations`, implemented/validated in DEV; omitted intentionally from **D02** because that image scopes to core ingestion environment binding.
- Power BI report reads **terminal object audits** in Fabric SQL Database. It is *not* a master-run audit or live RUNNING monitor. Pre-dispatch failures can have no object audit; inspect Fabric Monitor.
- Optional Fabric Activator DEV experiment observed failure event detection/rule action but **did not independently verify recipient inbox delivery**. Do not claim end-to-end alert delivery.

## 3. Runtime environment and D02 binding decisions

`vl_ingestion_connections` uses five `String` variables in the active workspace Value Set (currently DEV):

1. `ingestion_control_connection_id` — Fabric Control SQL **Connection ID**.
2. `ingestion_control_item_id` — Fabric SQL Database **Item ID**.
3. `ingestion_control_workspace_id` — containing **Workspace ID**.
4. `pipeline_invoke_connection_id` — Invoke Pipeline **Connection ID**.
5. `notebook_execution_connection_id` — Notebook execution **Connection ID**.

Separate source and target logical-resource bindings in `control.connection_settings` (source Connection refs and target Lakehouse Connection / Workspace / Item refs). Permissions and credentials are environment-specific; they are not backed up by Git item definitions. Same-workspace Fabric Pipeline and Notebook item references can use `.platform` logical IDs and matching zero GUID workspace references; **verify correct dependency remapping after sync**. Do not treat Fabric item IDs as Fabric Connection IDs.

**DEV implemented; UAT and PROD are Design only.** There is no proven UAT/PROD deployment, and no need to construct fake UAT/PROD UI screenshots. Variable Library UI screenshot was evaluated and intentionally **excluded from publishable evidence**; D02 plus runbook sufficiently describe the concept.

## 4. D01 and D02 — design decisions closed

Both editable SVGs are committed in `docs/assets/diagrams/`:

- **D01:** `d01-control-audit-er.svg` — title **“Control & Audit Data Model”**, subtitle **“Microsoft Fabric SQL Database”**. Keep two-level heading; don't change to a long one-line title solely to mimic D02. Depicts 4 core tables, FK and logical audit relationship, with design notes.
- **D02:** `d02-environment-binding.svg` — **“Environment Binding Architecture in Microsoft Fabric”**, title only (no platform subtitle). Shows **five scoped shared item definition types**: Data Pipelines, Notebooks, Variable Library, SQL Database, Lakehouse. Power BI was purposefully omitted from both shared-definition chips and per-workspace binding cards for this ingestion-specific architecture image (Power BI **still exists in repository**).
  - Workspace tiles: **DEV Implemented**, **UAT Design only**, **PROD Design only**. UAT/PROD state labels and sidebars styled in neutral gray; the Shared/Environment-specific meaning of other colors remains.
  - Three per-workspace binding cards: **Variable Library Values**, **Source & Target Resource Bindings**, **Permissions & Credentials**. Distinct **Dependency Auto-binding** note explains logical same-workspace item links vs environment-dependent connection IDs.
  - Label: **“Configure or verify per workspace”**. Do not imply rebinding always required after every sync if values already correct.
- D01 and D02 are considered **finalized**; no extra UI screenshots needed to prove D02 conceptual architecture.
- Editable diagrams must remain **real editable SVG**, not raster illustrations from an image generator. If revised later, provide SVG and PNG rendered **from the exact SVG** and visually inspect both.

## 5. Evidence asset snapshot — 58 screenshots + 2 diagrams

**Important:** At handoff, screenshots were **sorted using names and user notes only**. The 58 image bodies were **not** exhaustively inspected. A filename can indicate the intended claim, never prove that the image shows a successful test or contains no sensitive details.

Current structure:

```text
docs/assets/
├── architecture-overview.svg
├── diagrams/
│   ├── d01-control-audit-er.svg
│   └── d02-environment-binding.svg
└── screenshots/
    ├── composites/                          5 derived composites + per-artifact manifests
    ├── core/                                10 screenshots
    ├── performance/                          3 direct screenshots
    │   └── source-config/                    3 PX screenshots
    └── supporting/
        ├── s1-orchestration/                22 CX screenshots
        ├── s2-no-new-data/                   4 CX screenshots
        ├── s3-sql-incremental/               3 CX screenshots
        ├── s4-sftp-incremental/              4 CX screenshots
        ├── s5-backfill/                      3 CX screenshots
        └── optional/
            ├── o01-end-to-end/               1 CX screenshot
            ├── o02-file-row-count/           2 CX screenshots
            └── o05-source-scope/             3 CX screenshots
```

**Counts:** 10 + 3 + 3 + 22 + 4 + 3 + 4 + 3 + 1 + 2 + 3 = **58**. Two SVG diagrams, **60 total committed visual assets**. Every screenshot was moved by Git path only—original PNG filename and Git Blob content preserved. No flat screenshots remain at `docs/assets/screenshots/*.png`.

**Batch C addition:** C11 adds one derived PNG, bringing the curated inventory to **61 visual assets** (58 original screenshots + 2 diagrams + 1 composite). Its public-safe per-artifact manifest is `docs/assets/screenshots/composites/c11-sql-server-incremental.manifest.json`; its reproducible Python/Pillow builder is `scripts/evidence/build_c11_composite.py`. Batch D adds C12 and O02, bringing the curated inventory to **63 visual assets** (58 originals + 2 diagrams + 3 composites). Their adjacent public-safe manifests and `scripts/evidence/build_sftp_composites.py` record reproducible composition. Batch E adds C10 and C13, bringing the curated inventory to **65 visual assets** (58 originals + 2 diagrams + 5 composites). Their adjacent manifests and `scripts/evidence/build_incremental_composites.py` record both identical watermark sources while displaying state only once. The original asset snapshot above remains unchanged.

`EVIDENCE_INVENTORY.csv` records individual current paths, batch/scenario tags, likely candidate, and unreviewed status. Prefer inventory/`git ls-files` over rereading all images to locate things.

### 5.1 Planned candidates and exact user status

**Core — C01 to C16:**

| Candidate | Intended filename | Snapshot status |
|---|---|---|
| C01 | `c01-control-metadata.png` | Batch A reviewed and owner-approved; integrated in Control Plane guide |
| C02 | `c02-logical-connections.png` | Batch A reviewed and owner-approved; integrated in Control Plane guide |
| C03 | `c03-master-orchestration.png` | Batch B reviewed and owner-approved; integrated in Pipeline Orchestration guide |
| C04 | `c04-object-routing.png` | **No single C04 file**; five original CX-S1 images integrated under Pagination, Dispatcher, Controller Routing, and Database Routing; unselected inventory entries unchanged |
| C05 | `c05-sql-server-copy-execution.png` | Batch C reviewed and owner-approved; original integrated in SQL Server guide |
| C06 | `c06-sql-bronze-lineage.png` | Batch C reviewed and owner-approved; original integrated in SQL Server guide |
| C07 | `c07-sftp-ingestion-flow.png` | **No single C07 file**; two owner-approved S1 originals integrated separately in SFTP guide: FILE Router detail 1 and SFTP INCREMENTAL Adapter 2 |
| C08 | `c08-sftp-landing.png` | Batch D reviewed and owner-approved; unchanged original integrated as DEV movement-feed Landing evidence |
| C09 | `c09-sftp-bronze-lineage.png` | Batch D reviewed and owner-approved; unchanged original integrated as visible DEV parsed rows with lineage |
| C10 | `c10-no-new-data-skipped.png` | Batch E composite integrated under Finalization; SKIPPED audits and qualified Bronze/state context; duplicate watermark displayed once |
| C11 | `c11-sql-server-incremental.png` | Batch C composite created from all three S3 originals and integrated with explicit run-type/correlation limitations |
| C12 | `c12-sftp-new-file-incremental.png` | Batch D composite created from all four S4 originals and integrated with explicit run-type/correlation limitations |
| C13 | `c13-incremental-backfill.png` | Batch E composite integrated under Audit semantics; BACKFILL INCREMENTAL SUCCESS audit with explicit bounds/state-observation limitations |
| C14 | `c14-ambiguous-run-scope.png` | Batch E reviewed and owner-approved; unchanged original integrated under Scope and explicit-request validation |
| C15 | `c15-operations-report.png` | Batch G original integrated; DEV latest audited batches show 2 sources / 2 object audit records / 0 failed sources |
| C16 | `c16-operations-filter.png` | Batch G original integrated; LOGISTICS_VENDOR filter shows latest-batch summary and four visible historical executions |

**Performance — P01 to P05:**

| Candidate | Intended filename | Snapshot status |
|---|---|---|
| P01 | `p01-benchmark-config.png` | **No single P01 file**; three owner-approved B1/B2/B3 original metadata snapshots integrated vertically under Permanent benchmark fixture |
| P02 | `p02-query-none.png` | Batch F original integrated; completed AUTO activity with one used parallel copy; resolved partitioning not shown |
| P03 | `p03-query-dynamic-range-auto.png` | Batch F original integrated; completed AUTO activity with four used parallel copies; separate from the 2026-10-12 PoC |
| P04 | `p04-query-dynamic-range-tuned.png` | Batch F original integrated; completed TUNED activity with four used parallel copies; no causal override-benefit claim |
| P05 | No image artifact | **QUALIFIED descriptive Markdown table only**, integrated after P04; per-capture measured values with explicit comparability limitations; no PNG/chart/composite or speedup claim |

**Optional — O01 to O05:**

| Candidate | Intended filename | Snapshot status |
|---|---|---|
| O01 | `o01-end-to-end-trace.png` | Pending additional correlation and Bronze lineage evidence; not integrated or permanently skipped |
| O02 | `o02-file-vs-row-count.png` | Batch D cropped comparison created and integrated under Transfer consistency; files versus parsed rows; no independent Bronze recount or verified end-to-end correlation |
| O03 | `o03-full-append-history.png` | **SKIP / dropped by user** |
| O04 | `o04-copy-performance-details.png` | **SKIP / dropped by user** |
| O05 | `o05-source-scoped-run.png` | Reviewed in Batch E; pending additional exact correlation evidence and privacy-safe presentation; no composite or Markdown integration; not permanently rejected |

**D01 / D02:** real SVGs exist and are finalized. D01 is reviewed, owner-approved, and integrated in the Control Plane guide with its original SVG preserved. D02 is reviewed, owner-approved, and integrated unchanged in the Variable Library environment-binding runbook with a full-size SVG link.

### 5.2 What S1–S5 mean (do not misinterpret duplicates)

- **S1 — orchestration and routing:** S1 CX names capture config pagination, master details, Dispatcher, Object Controller DATABASE/FILE, routers, SFTP incremental adapter, SQL Server FULL adapter. Supports C04/C07 as **several direct images**, not blindly one enormous composite.
- **S2 — SKIPPED audit and state context:** C10 shows two DEV SKIPPED audits with 0/0 counts and a separate Bronze result with `bronze_rows = 0`. Its SQL query/filter is absent, so it does not independently prove no append or total table counts. The audit does not show run type and truncates Run IDs. `cx-s2-watermark-before.png` and `cx-s2-watermark-after.png` have the **exact same Git Blob SHA**; C10 displays the state once and records both sources in its manifest. These are not independently verified before/after observations or exact execution correlation.
- **S3 — SQL Server audit/checkpoint comparison:** four SUCCESS audit rows have LOW/HIGH values consistent with the displayed before/after checkpoints for configs 1, 4, 5, and 6. All four checkpoints advance to `2026-10-24T01:08:00.941Z`. C11 preserves all three screenshots at native resolution. Run type is not visible and audit Run IDs are truncated; this does not independently verify exact execution correlation or a fully correlated REGULAR INCREMENTAL run.
- **S4 — SFTP audit/lineage/checkpoint comparison:** C12 preserves all four originals at native resolution. The DEV audit reports SUCCESS with six processed rows; six visible Bronze rows share the after-state Batch ID. The checkpoint advances from `2026-10-23T12:31:47.787Z` to `2026-10-24T02:04:02.238Z`. Run type and remote Last Modified values are not visible; some Run IDs are truncated. Exact execution correlation and a fully correlated REGULAR INCREMENTAL run are not independently established. C08/C09 are a different DEV execution example.
- **S5 — BACKFILL audit and state context:** C13 shows customers with `run_type = BACKFILL`, `load_strategy = INCREMENTAL`, `status = SUCCESS`, and counts 2/2. LOW/HIGH and audit Batch ID are truncated; do not reconstruct them. Both watermark sources display `2026-10-24T01:08:00.941Z` and are byte-identical; state appears once in C13. This is not independent proof of checkpoint non-advancement, Bronze append, exact execution correlation, or exactly-once business semantics.
- **S8 — configuration snapshots and completed Copy observations:** P01 shows active config 10 for `copy_source_partitioned` and inactive config 9. B1 uses NONE without override; B2 uses DYNAMIC_RANGE on `event_date` without override; B3 requests override 4. P02/P03/P04 show completed AUTO/AUTO/TUNED Copy activities using 1/4/4 parallel copies. Exact snapshot-to-execution linkage and resolved result partition settings are not independently verified. P05 is a qualified descriptive table, not a generated image or controlled speedup comparison.

### 5.3 Screenshot quality contract

1. Screenshot from an actual completed execution or persisted real state; capture master/object Run IDs and Batch IDs where needed.
2. Crop irrelevant UI without changing or inventing outcomes; any composite must use **real** source screenshots and be explicitly labeled a **Composite**.
3. Don't expose credentials, tokens, connection strings, personal IDs, or confidential business data. **Batch A, the six selected Batch B captures, and all five Batch C source screenshots have been visually checked. Batch C retains visible operational identifiers only within original evidence pixels; no credentials, physical connection/workspace/item IDs, or personal information were found. New composite labels and manifest metadata add no environment-specific identifiers. Batch D selected sources were also checked. C08 retains operational Batch/Run IDs and DEV resource names only within the owner-approved unchanged original; C09/C12 retain original lineage pixels. No credentials or confidential client data were found. O02 derived crops exclude operational/environment identifiers. New labels and public manifests contain no environment-specific GUIDs. Batch E approved sources were checked: operational IDs remain only within unchanged original pixels; no credentials or personal information were found. New C10/C13 labels and manifests add no private identifiers. O05 Input contains environment identifiers and remains unpublished as a curated figure. All six Batch F PNGs were checked: no credentials, host addresses, personal information, or Workspace/Connection IDs were found; operational Activity Run IDs remain only in original result pixels. Newly authored captions and tracking add no private environment identifiers. Other assets still require publication-specific privacy review; do not infer acceptance from contact-sheet inclusion.**
4. Caption tells **what an artifact proves** (e.g. final audit and checkpoint non-advancement), not just what UI it shows.
5. `evidence-log.csv` is optional **local/private working metadata**, useful for IDs and provenance; don't backfill unavailable IDs by guessing, and don't commit environment GUIDs unnecessarily.
6. If screenshot A and B support the same claim, use the clearer one. A guide need not include every image in the archive.

## 6. Performance facts and claim guardrails

See `docs/architecture/database-copy-performance.md`; DO NOT rely solely on this summary if interpreting new metrics.

- SQL Server source: SQL Server 2022 Developer on EC2. A separate benchmark database `sql_benchmark_db` includes two 10,000,000-row fixture tables with equal logical data but different **source physical layouts** (unpartitioned vs monthly partitioned); they are distinct from the **Fabric Copy partition execution strategy** (`NONE` or `DYNAMIC_RANGE`).
- SQL Server Copy in this framework uses **query mode**; source metadata `copy_options` may specify `partition_option = NONE | DYNAMIC_RANGE`, explicit partition column for dynamic range, optional positive `parallel_copies` override.
- **AUTO and explicit `parallelCopies = 0` are not equivalent.** AUTO route omits the `parallelCopies` property. A pipeline parameter value of 0 is an internal routing sentinel, **never** a value forwarded to the Copy activity. Positive override uses a tuned branch.
- Existing documented 2026-10-12 DEV PoC: **explicit zero** completed 10M rows, usedParallelCopies=1, CopyDuration=483 s, throughput ≈23.08 MB/s, used DIUs=4; native AUTO was observed **in progress**, usedParallelCopies=4. This observation proves differing parallelism in that test, not a completed comparative AUTO speedup.
- Source CPU/memory, bytes/rows, elapsed time, used parallel copies and DIUs, Fabric Capacity, target pre-run state all matter for controlled comparisons. P05 is owner-approved only as a **QUALIFIED descriptive Markdown table** of completed P02/P03/P04 observations. Resource conditions, resolved Copy inputs, and exact configuration-to-run linkage remain unverified; no speedup/cost or generalized tuning conclusion is supported.
- Do not turn a metadata configuration example such as `parallel_copies=8` into a benchmark-derived recommendation.

## 7. Documentation integration map — user's existing plan

**Do not immediately publish every candidate.** Integrate the selected, reviewed subset:

| Existing Markdown document | Planned image candidates |
|---|---|
| `docs/guides/control-plane.md` | C01, C02, D01 |
| `docs/guides/pipeline-orchestration.md` | C03, C04, O05 |
| `docs/guides/sql-server-database-ingestion.md` | C05, C06, C11 |
| `docs/guides/sftp-file-ingestion.md` | C07, C08, C09, C12 |
| `docs/architecture/generic-incremental-watermark.md` | C10 |
| `docs/operations/retry-rerun-backfill.md` | C13, O03 (but **O03 skipped**, do not publish) |
| `docs/operations/run-request-examples.md` | C14 |
| `docs/operations/monitoring-report.md` | C15, C16 |
| `docs/architecture/database-copy-performance.md` | P01–P05, O04 (but **O04 skipped**, do not publish) |
| `docs/architecture/framework-overview.md` | O01 |
| `docs/architecture/file-ingestion-design.md` | O02 |
| `docs/operations/variable-library-environment-binding.md` | D02 |

**Paths changed after plan was written.** Images are now under **nested screenshot folders**, e.g. from `docs/guides/...` to `../assets/screenshots/core/c01-control-metadata.png`. D01/D02 paths: `../assets/diagrams/d01-control-audit-er.svg` and `../assets/diagrams/d02-environment-binding.svg` when referencing from `docs/guides` or `docs/operations`. From repository-root README, use `docs/assets/...`. Verify all relative Markdown links after insertion.

**README:** Keep current README content/navigation. Add at most **two high-value images** after review: first choice **O01 end-to-end trace** and **C15 Operations Monitoring**; if O01 is not good enough, replace it with **C03 master orchestration**. README acts as landing page; deeper guides hold technical detail.

**Technical QA after integration:** confirm pipeline/activity names from checked-in definitions, paths, environment claims, execution semantics, AUTO-vs-zero language, reproducible performance claims, privacy and run provenance, screenshot captions, readability, and no false impression that UAT/PROD has been tested. Current Markdown had **no references to C/P/CX/PX or D01/D02** when filenames were reorganized, so the path relocation did not break already-inserted screenshot links.

## 8. Current work plan — what to do next and in what order

### Batch A completed — 2026-10-25 (Asia/Bangkok)

- Owner approved the evidence review and implementation. C01, C02, and D01 are integrated at the approved locations in `docs/guides/control-plane.md`, using the approved captions and links to the full-size original assets.
- C01 shows selected DEV configuration columns; C02 is explicitly introduced as a DEV configuration-to-connection mapping, not the exact output of the preceding two-column query or proof of connectivity. Neither screenshot proves execution outcomes or universal configuration values.
- D01 remains the finalized editable SVG. Its selected-field overview and distinction between enforced FKs and the non-FK audit association agree with the SQL Database Project. No PNG/SVG source asset was changed.
- Validation covers relative figure links, unique placement, Markdown structure, preservation of existing guide text and original asset blobs, CSV scope limited to C01/C02/D01, and final Git diff review.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate control plane evidence and data model`. Batch A was subsequently merged into `main` at `30470a6`. No other screenshot batch was inspected or integrated during Batch A.
- Batch B was subsequently reviewed and authorized by the owner; its completed progress is recorded below. Other handoff files retain their original planning context and were not updated in Batch A.

### Batch B completed — 2026-10-25 (Asia/Bangkok)

- Integrated six owner-approved original PNGs at five locations in `docs/guides/pipeline-orchestration.md`: C03 plus C04 Pagination, Dispatcher, Controller Routing, and Database Routing. Controller DATABASE/FILE images remain vertically arranged with one shared caption. All six images link to their full-size originals; existing Mermaid and technical explanations are preserved.
- Selected CX-S1 files: `cx-s1-config-pagination-detail-1.png`, `cx-s1-dispatcher-execution.png`, `cx-s1-object-controller-database.png`, `cx-s1-object-controller-file.png`, and `cx-s1-database-router-detail-1.png`. C04 remains their parent evidence candidate. Inventory changes are limited to these five entries and C03; unselected CX-S1 and O01 rows retain their prior status.
- The guide describes individual DEV observations without claiming a single correlated execution. Pipeline invocation `Succeeded` is explicitly distinct from object audit `SUCCESS`; the Dispatcher capture demonstrates two invocations starting in the same displayed second, not eight simultaneous object executions. The DATABASE route capture demonstrates `SQL_SERVER|FULL` only.
- Rechecked all six selected images for sensitive environment information; no credentials, physical connection/workspace/item IDs, or personal information are visible. Original PNGs are unchanged. Temporary contact sheets cover all 22 CX-S1 inputs plus C03 and remain outside the repository; they are review aids, not publication composites.
- O01 remains pending additional evidence, not permanently skipped. Some master/adapter captures share a Batch ID and adapter Copy input carries the matching controller audit Run ID, but `cx-o01-audit.png` truncates IDs and the reviewed set lacks persisted Bronze lineage results. Do not publish an end-to-end trace until exact audit correlation, child-run linkage, and matching Bronze lineage are established.
- Validation covers all relative guide links, six unique full-size image links at the approved locations, exact approved captions, one shared Controller caption, preservation of existing content/Mermaid and original asset blobs, inventory scope, and final Git diff review.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate orchestration execution evidence`. Batch B was subsequently merged into `main` at `d3f9b17`. FILE Router and SFTP Adapter details remain for Batch D; Batch C progress is recorded below.

### Batch C completed — 2026-10-25 (Asia/Bangkok)

- Owner approved C05/C06 integration and the first C11 composite with the limited audit/checkpoint claim. `docs/guides/sql-server-database-ingestion.md` includes C05 under FULL, C11 under `When does the watermark advance?`, and C06 under DEV result verification. Approved captions, clickable full-size links, original technical explanations, and both Mermaid diagrams are preserved.
- C05 shows a successful DEV FULL Adapter AUTO Copy reporting 20 rows read/written, not independent proof of terminal audit success. C06 shows visible DEV category rows with lineage, not total row count or independently verified correlation with C05.
- C11 is `docs/assets/screenshots/composites/c11-sql-server-incremental.png` (1449x758). Native 1409x124 source panels are vertically ordered Watermark Before, SUCCESS Audit Records, Watermark After, without cropping, resizing, arrows, invented identifiers, or edited data. The image is labeled a composite of DEV evidence and visibly states: "Run type is not visible; exact execution correlation is not independently verified."
- Supported claim: four DEV SUCCESS audit rows contain processing bounds consistent with the displayed before/after checkpoint values, and those checkpoint values advanced. REGULAR and fully correlated execution remain unverified from these captures. These are four object audit rows, not a single-run trace.
- Rebuild with `scripts/evidence/build_c11_composite.py` using Python and `Pillow==11.3.0`; the bundled font avoids workstation-font dependencies. The adjacent `.manifest.json` records ordered original paths, source/output SHA-256 hashes, native panel rectangles, dimensions, supported claim, and limitations without copying operational IDs into metadata.
- Validation covers PNG integrity, exact panel-pixel preservation, unchanged original Git blobs, reproducible output, visual readability/privacy, approved Markdown placements/captions and relative links, preserved explanations/Mermaid, inventory scope, and final Git diff review. Only the five Batch C source entries are updated; the derived C11 row is added separately. Other evidence states remain unchanged.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate SQL Server ingestion evidence`. Batch C was subsequently merged into `main` at `9cb42e3`. O01 remains pending additional evidence. Batch D progress is recorded below.

### Batch D completed — 2026-10-25 (Asia/Bangkok)

- Integrated four owner-approved original PNGs with full-size links in `docs/guides/sftp-file-ingestion.md`: C07 FILE Router detail 1 under run scope; C07 SFTP INCREMENTAL Adapter 2 and C08 under Step B; C09 under terminal audit verification. Existing explanations and both Mermaid diagrams are preserved. Successful activities are not equated with terminal audit SUCCESS; C08 is a Landing result view, not independent Binary/byte-equality proof.
- Created C12 `docs/assets/screenshots/composites/c12-sftp-new-file-incremental.png` (1450x804) from four complete native S4 images, ordered Watermark Before, SUCCESS Audit Record, Bronze Source-File Lineage, Watermark After. Integrated under terminal audit verification with the limited S4 claim above. The guide explicitly distinguishes C08/C09 from C12 as different DEV execution examples.
- C12 visibly states: "Run type is not visible; some run identifiers are truncated. Exact execution correlation is not independently verified." No missing identifiers, values, timestamps, or remote Last Modified observations were invented.
- Created O02 `docs/assets/screenshots/composites/o02-file-vs-row-count.png` (1362x726) and integrated under `Transfer consistency` in `docs/architecture/file-ingestion-design.md`. Two panels retain genuine native Copy details and separated Notebook activity/Output/metric crops. Operational/environment identifiers and intervening metadata are omitted from the derived presentation; both originals remain unchanged. Binary Copy reports 1/1 files and the Notebook reports 6/6 rows. Both row metrics reuse the same parsed DataFrame count, not an independent Bronze recount; exact end-to-end correlation is not independently verified.
- O02 visual follow-up: clipped the complete serialized metrics object line by line while retaining native pixels, original relative positions, and original wrapping. Removed the partial leading token and trailing Run ID text; compacted Notebook context crops. Binary Copy, evidence limitations, original screenshots, published Markdown, and C07/C08/C09/C12 remain unchanged. The updated 1362x726 preview was subsequently owner-approved as part of Batch D, merged into `main` through `d186999`. The manifest records the clipping method and revised crop rectangles; deterministic rebuild and exact pixel preservation were verified.
- Rebuild both with Python and `Pillow==11.3.0` using `scripts/evidence/build_sftp_composites.py`. Adjacent `.manifest.json` files record original paths, SHA-256 hashes, original/output dimensions, crop/destination rectangles, supported claims, and limitations without transcribing operational identifiers into metadata. C12 uses complete screenshots; O02 uses explicitly separated UI crops. Neither resizes or retouches evidence pixels.
- Validation covers PNG integrity, exact native source/crop pixels, unchanged original Git blobs, reproducible PNGs/manifests, visual readability/privacy, relative image and full-size links, approved placements/captions, preserved explanations/Mermaid, inventory scope, and complete Git diff. Only ten processed Batch D source rows are updated; C12/O02 derived rows are added. Unselected CX-S1 and other evidence states remain unchanged.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate SFTP ingestion evidence`. Batch D, including its O02 visual follow-up, was subsequently merged into `main` through `d186999`. O01 still requires additional correlation evidence; Batch E progress is recorded below.

### Batch E completed — 2026-10-25 (Asia/Bangkok)

- Owner approved qualified C10/C13 composites and direct C14 integration. Added full-size-linked figures at the approved locations: `Finalization` in `docs/architecture/generic-incremental-watermark.md`, `Audit semantics` in `docs/operations/retry-rerun-backfill.md`, and `Scope and explicit-request validation` in `docs/operations/run-request-examples.md`. Existing technical explanations and Mermaid diagrams are preserved.
- C10 `docs/assets/screenshots/composites/c10-no-new-data-skipped.png` (1453x664) contains complete native panels for SKIPPED Audit Records, Bronze Count Result with query scope not shown, and one watermark state. The visible limitations state that duplicate watermark files are not independent observations, the zero Bronze count does not independently prove no append, run type is absent, some Run IDs are truncated, and exact execution correlation is not verified.
- C13 `docs/assets/screenshots/composites/c13-incremental-backfill.png` (1453x508) contains the BACKFILL INCREMENTAL SUCCESS audit and one watermark state. Visible limitations cover byte-identical state sources, truncated LOW/HIGH and Batch ID, and the lack of independently verified checkpoint non-advancement, Bronze append, exact execution correlation, or exactly-once business semantics. Both run_type and load_strategy remain visible as separate columns.
- C14 preserves its original PNG. It demonstrates `AMBIGUOUS_RUN_SCOPE` at `fail_ambiguous_run_scope`, consistent with the master dependency chain that validates scope before child dispatch. No new Fabric run or fabricated outcome was introduced.
- Rebuild with Python and `Pillow==11.3.0`: `scripts/evidence/build_incremental_composites.py`. Both public-safe manifests record original source paths, SHA-256 hashes, dimensions, complete-panel placements, supported claims, and limitations. Each pair of watermark files is checked byte for byte; the before source is displayed once, and the identical after source is explicitly recorded without a second placement. The builder stops if the files differ. No source screenshot was changed, cropped, resized, retouched, or supplemented with invented values.
- O05 remains pending additional evidence, not permanently rejected. The source-scoped invocation, paginator selection of configs 7/8, and REGULAR object audits are compatible, but audit Batch IDs are truncated and parent–child linkage is absent. Input exposes environment identifiers. Require full audit correlation and parent/child invocation evidence plus privacy-safe presentation before publication. No O05 composite, Markdown insertion, or inventory status change was made.
- Validation covers eight unchanged original PNGs, exact native composite pixels, single watermark display with both original paths/hashes preserved, deterministic PNG/manifest rebuilds, visual readability/privacy, relative image/full-size links, exact captions/placements, preserved documentation, inventory scope limited to eight approved sources plus two new derived artifacts, and complete Git diff.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate incremental and backfill evidence`. Batch E was subsequently merged into `main` at `86e3e78`. Batches A–E are merged through that commit; Batch F progress is recorded below.

### Batch F completed — 2026-10-25 (Asia/Bangkok)

- Integrated all six owner-approved original PNGs with exact approved captions and clickable full-size links in `docs/architecture/database-copy-performance.md`. P01 B1/B2/B3 remain vertically arranged under `Permanent benchmark fixture`; P02/P03/P04 sit under the new `Completed DEV Copy observations — 2026-10-24` subsection within `Benchmark procedure`. No new raster asset, chart, composite, builder, or manifest was created; the visual-asset inventory remains 65 entries.
- P01 demonstrates DEV metadata, not execution correlation: config 10 is active, config 9 inactive; B1 is NONE with no override; B2 is DYNAMIC_RANGE on event_date with no override; B3 requests override 4. The selector's repeated `requested_parallel_copies` input is explicitly distinguished from observed runtime parallelism. Result filenames do not establish resolved partitioning; no independently correlated B1/P02, B2/P03, or B3/P04 mapping is claimed.
- P02/P03/P04 each report Copy Succeeded, 10,000,000 rows read and written, and 12.552 GB data read. Used parallel copies are 1/4/4. Copy details Total durations are 00:05:16 / 00:04:33 / 00:02:34, retained separately from activity-list durations 5m 25s / 4m 43s / 2m 43s. Reported throughputs are 40.753 / 47.011 / 85.388 MB/s. Data written/files are 565.69 MB/5, 571.46 MB/8, and 571.46 MB/8. Copy success does not independently prove terminal SQL audit SUCCESS.
- P05 is a **QUALIFIED descriptive Markdown table only**, placed after P04 with the owner-specified caption and limitations. It reports observations without speedup percentages, inferred override benefits, or a general tuning recommendation. DIUs, Fabric capacity, EC2 resource utilization, missing Copy inputs, cache/repeat-trial conditions, and target pre-run state are not supplied. No completed comparable unpartitioned-source result is implied.
- Preserved all existing technical content, the illustrative parallel_copies 8 example, and the complete 2026-10-12 explicit-zero versus omitted-AUTO PoC unchanged. Current checked-in FULL and INCREMENTAL AUTO branches omit parallelCopies; internal parameter 0 is a routing sentinel, while TUNED supplies a positive explicit override. The new completed 2026-10-24 captures do not retroactively complete the historical partial AUTO observation.
- Validation covers unchanged original PNG blobs/integrity, native-resolution readability/privacy, six unique relative image/full-size links, exact captions/placements, table values/formatting, preserved technical explanations/fences/PoC, inventory scope limited to six reviewed source entries, no added visual artifact/P05 inventory row, and final Git diff. Other evidence states, including O01/O05, remain unchanged.
- Separate final-QA maintenance finding: the header comment in `scripts/control/05_set_benchmark_scenario.sql` still recommends p_config_id; the supported orchestrator accepts p_run_requests. Record for a later documentation/maintenance change. Runtime scripts and Pipeline JSON were not modified in Batch F.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate database copy performance evidence`. Batch F was subsequently merged into `main` at `a705eb4`. Batches A–F are merged through that commit; Batch G progress is recorded below.

### Batch G completed — 2026-10-25 (Asia/Bangkok)

- Integrated owner-approved original C15/C16 PNGs with evidence-qualified English captions and clickable full-size links under `Report page: Operations` in `docs/operations/monitoring-report.md`. C15 follows the visuals summary table; C16 follows the sorting/filter paragraph, before the separate Activator section. Both originals remain unchanged at 1655x928; no composite or new visual artifact was created. The inventory remains 65 visual assets.
- C15 shows two source systems, two terminal object audit records across the latest audited batches, and zero failed sources. Both latest source summaries are SUCCESS; history also shows earlier SUCCESS/SKIPPED outcomes and REGULAR/BACKFILL run types. C16 selects LOGISTICS_VENDOR with one latest-batch object audit record and four visible historical executions including an earlier SKIPPED outcome. The source_system relationship filters history across batches, not only the latest Batch ID.
- Preserved the earlier acceptance observation of 2 Source Systems / 8 Objects / 0 Failed Sources and explicitly distinguished the later C15 observation of 2 / 2 / 0. Objects sums terminal audit records in each source's latest audited batch, not all configured objects or all history; the count difference does not establish deleted configurations. Latest Activity (UTC) represents audited object end time in the current filter context, not report refresh time or measured refresh latency.
- Monitoring SQL views, finalization logic, PBIR bindings and TMDL measures/relationship agree with the evidence. The audit schema supports SUCCESS, FAILED, SKIPPED, WARN and CANCELLED, but C15/C16 demonstrate only SUCCESS/SKIPPED outcomes. They do not establish live RUNNING coverage, all master executions, failures before object-audit creation, newest-batch failure behavior, propagation latency, or Activator recipient delivery. Pipeline activity success is not substituted for terminal SQL audit success. A latest audited batch may still be partially complete.
- Privacy/readability review found no credentials, connection strings, host/workspace identifiers or personal information in C15/C16. Operational Run IDs remain only within unchanged original screenshot pixels, not captions or tracking. History text benefits from the retained full-size links. No report, model, SQL, procedure, original PNG or unrelated documentation was modified.
- Validation covers original PNG integrity and unchanged Git blobs, native-resolution visual inspection, relative image/full-size links and placements, preserved pre-existing guide content and monitoring caveats, inventory changes limited to C15/C16, public-safe tracking, and complete Git diff review. Other evidence states, including pending O01/O05, remain unchanged.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate operations monitoring evidence`. Batch G was subsequently merged into `main` at `eb4ce0c`. Batches A–G are merged through that commit; Batch H progress is recorded below.

### Batch H completed — 2026-10-25 (Asia/Bangkok)

- Integrated the owner-approved finalized `docs/assets/diagrams/d02-environment-binding.svg` under `Scope and decision` in `docs/operations/variable-library-environment-binding.md`, after the paragraph ending `own active Library bindings to execute.` and before `What is and is not parameterized`. The approved conceptual caption and clickable full-size SVG link are retained. D02 was not modified, regenerated or redesigned; its Git blob remains `becd027b2cd9307c4a617160a32f1c8b64bbd314`. No new visual artifact was created; the inventory remains 65 entries.
- Made only the three approved runbook qualifications: configure or verify IDs per workspace after deployment; the MISSING_RUNTIME_BINDING guard detects missing/empty Library values without validating GUID correctness, permissions, connectivity or target references; UAT/PROD deployment and runtime validation remain designs without independently established success.
- Preserved all five String variable names and ID roles: three Connection IDs (Control SQL, Invoke Pipeline and Notebook execution), one Control SQL Database Item ID and one containing Workspace ID. Runtime Library bindings remain separate from source/target metadata in control.connection_settings, same-workspace logical item references, and environment-specific permissions/credentials. Static definitions and logical-ID matches do not prove automatic environment rebinding or successful runtime execution.
- The Batch H review rendered D02 at its native 1900x1265 dimensions and found no clipping, unsupported relationship or sensitive environment-specific identifier. Validation checks unchanged SVG bytes/Git blob, exact caption/placement and relative image/full-size links, unchanged variable table and implementation references, inventory scope limited to D02, public-safe tracking, and complete Git diff. Pipeline JSON, Variable Library definitions, SQL metadata, original diagrams/screenshots and unrelated documentation are unchanged.
- O01/O05 remain pending additional exact execution-correlation evidence; O05 also needs privacy-safe presentation. Neither is integrated or permanently rejected. Preserve prior audit, watermark, monitoring, performance and deployment limitations during Final Portfolio QA, including unverified Activator recipient delivery and the scenario-script comment maintenance finding.
- Implementation branch: `docs/evidence-curation`; commit message: `docs: integrate environment binding architecture`. Batch H owner review/merge remains pending; do not merge into main without owner direction. **Final Portfolio QA is the next phase**, including any separately authorized README evidence selection and handoff cleanup; no QA expansion or cleanup was performed in this batch.

### Phase A — Filename-first curation (remaining batches)

- Start from `EVIDENCE_INVENTORY.csv` and current GitHub tree, **not** from visual inspection of 58 images at once.
- Evaluate one group at a time, likely **S1**, then S2→S5, performance S8, optional O01/O02/O05, and final direct C/P.
- For each group, map intended claims to its files; choose likely publication images; identify necessary composites and crops; mark `PUBLISH_DIRECT`, `COMPOSITE_SOURCE`, `ARCHIVE_ONLY`, or `SKIP` only after enough evidence to justify it.
- Agree exact naming for composite outputs and whether to use one panel or several separate images. The user explicitly said **C04, C07, P01** should use several screenshots instead of an obligatory single merged image.
- Keep any detailed per-image review *scoped to the current batch*. Use user-supplied status/observations rather than inferring test results from filenames.

### Phase B — Composite production and measured comparison

- C10/C11/C12/C13 and cropped O02 are complete with the qualified claims above. O01/O05 remain pending additional correlation evidence; build only after that evidence supports publication. Composite labeling must be explicit. Preserve traceability to original images and evidence IDs; do not cosmetically alter pass/fail/results or invent before/after timestamps.
- P05 is complete as an owner-approved **QUALIFIED descriptive Markdown table** of real completed observations. No P05 image/chart/composite is planned for this evidence set. A controlled performance comparison still requires verified run inputs, resource/target conditions, and representative repeat trials.
- D01/D02 do not need further conceptual changes.

### Phase C — Markdown integration + QA

- Insert curated diagrams/screenshots in mapped guides **sparingly**, write evidence-based captions, and check relative paths.
- Add selected 1–2 images in README, no full rewrite.
- Validate markdown links/rendering; verify technical statements against current code and collected run evidence; make a commit. Update handoff if important decisions change.

### Living handoff update protocol

- After each completed evidence batch, update `EVIDENCE_INVENTORY.csv` only for assets actually reviewed. A file in Git is **not** equivalent to a visually verified or publish-ready screenshot.
- Update `PROJECT_HANDOFF.md` with verified milestone status, remaining actions and relevant commit references. Update `CONTINUATION_PROMPT.md` if the next task changes. Use `SCREENSHOT_IMPLEMENTATION_PLAN.md` for batch scope, composite rules, Markdown placement and acceptance criteria.
- All `.project-handoff/` files are public. Do not add secrets, credentials, unpublished client artifacts, private run/batch identifiers or environment-specific GUIDs.
- After portfolio QA is complete, remove `.project-handoff/` in a cleanup commit after preserving necessary permanent knowledge in canonical documentation. Deletion does not purge earlier public commits.

### Phase D — final handoff or finish

- When moving conversations, refresh the live GitHub handoff with current milestone, reviewed inventory, completed composites, actual commit and next exact work item. Do not call unfinished images complete.

## 9. Things **not** to redo or quietly change

- No more Variable Library UI screenshot hunt; intentionally excluded.
- Do not reopen D01 title formatting or D02 Power BI/UAT/PROD styling debates absent an evidenced bug.
- Do not invent fake DEV/UAT/PROD deployments for a portfolio screenshot.
- Do not delete exact-equal S2 or S5 watermark before/after evidence just because the file hashes match—unchanged checkpoint is expected in those scenarios.
- Do not transform real engineering evidence with artistic image generation. For architecture diagrams, editable SVG; for evidence composites, use actual screenshots; for P05, measured numbers only.
- Do not assume raw binary screenshot images were reviewed simply because GitHub has them.
- Do not create redundant new Technical Guides if existing canonical guides cover the topic.
- Do not treat planned optional O03/O04 as required; user explicitly dropped them.
- This temporary sanitized handoff was explicitly authorized for the public repository. Never commit detailed private run logs, private environment IDs or secrets. A later delete does not remove prior Git history.

## 10. Key authoritative repository references

- `README.md`
- `docs/architecture/framework-overview.md`
- `docs/architecture/generic-incremental-watermark.md`
- `docs/architecture/database-copy-performance.md`
- `docs/architecture/file-ingestion-design.md`
- `docs/guides/control-plane.md`
- `docs/guides/pipeline-orchestration.md`
- `docs/guides/sql-server-database-ingestion.md`
- `docs/guides/sftp-file-ingestion.md`
- `docs/operations/retry-rerun-backfill.md`
- `docs/operations/run-request-examples.md`
- `docs/operations/monitoring-report.md`
- `docs/operations/variable-library-environment-binding.md`
- `docs/operations/environment-rebuild.md`
- `scripts/control/02_create_control_procedures.sql`
- `scripts/monitoring/01_create_monitoring_views.sql`
- `fabric/` tracked Fabric items
- `docs/assets/diagrams/` finalized SVGs
- `docs/assets/screenshots/` filename-sorted evidence

## 11. Provenance and confidence

- **Checked against GitHub repository on 2026-10-24:** branch head/commit, actual asset paths/counts, README and key technical guides, D01/D02 existence, monitoring and performance guardrails, current environment runbook.
- **User-provided decisions:** exact C/P/O target filenames and `SKIP`/`COMPOSITE`/`multiple screenshots` notes; D01/D02 visual preferences; request for minimum-effort filename-first batch curation; temporary public-repository handoff strategy.
- **Not established by this handoff:** visual content or privacy review of each PNG, completed review of all 26 candidates, availability of original Run IDs or Test SHA for every scenario, exact S3 execution correlation/run type, controlled P05 benchmark comparability, exact configuration-to-run linkage, and per-run resource/target conditions, exact S4 execution correlation/run type or remote Last Modified values, independent O02 Bronze recount/end-to-end correlation, independent S2/S5 before/after state observations, S2 Bronze query scope/run type/exact correlation, complete S5 audit bounds/Batch ID or independent Bronze append, exact O05 execution linkage, existence of planned O01/O05 composites, UAT/PROD deployment success, full Activator alert delivery.

**Next action when continuing:** Review completed Batch H on `docs/evidence-curation`; do not merge into `main` without owner direction. Batches A–G are merged through `eb4ce0c`. **Final Portfolio QA is the next phase** after owner direction. Preserve D02 unchanged and its DEV-implemented/UAT-PROD-design-only qualification; static binding definitions do not prove runtime success. Keep monitoring limited to terminal object audits and P05 as a qualified descriptive Markdown table with the historical PoC preserved. O01/O05 remain pending additional correlation evidence; O05 needs privacy-safe presentation. Track the scenario-script comment finding and separately authorize any README evidence selection or handoff cleanup. No redesign or mass visual scan.
