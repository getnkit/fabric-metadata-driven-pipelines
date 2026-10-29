<a id="technical-learning-path--metadata-driven-pipelines"></a>

# Technical Learning Path: Metadata-Driven Ingestion Pipelines

Start with a reading route below; follow only the steps relevant to your goal. No Fabric workspace is needed
to inspect the guides and checked-in definitions.

## Choose a reading route

| Goal | Read |
| --- | --- |
| **Portfolio / architecture scan** | [Architecture](../architecture/framework-overview.md) → [Database Copy Performance](../architecture/database-copy-performance.md) for Copy configuration and limited development-workspace observations |
| **Follow an actual ingestion request** | Steps **1–4** below; choose SQL Server or SFTP |
| **Understand production-style safety decisions** | Steps **5–7**: watermark, retry/compensation, audit visibility |
| **Reproduce the DEV demo** | Step **8**, then follow the operator runbooks (not the design documents) |

<a id="1--understand-the-architectural-problem"></a>

## 1: Understand the architectural problem

**Read:** [Architecture & Design Decisions](../architecture/framework-overview.md).

Focus on the **Control & Audit Plane** (config/state/terminal audit), **Orchestration Plane**
(selection/validation/routing), and **Data Plane** (source → Landing/Bronze). These are logical responsibilities
within one Fabric-based framework, not isolated deployed platforms. The Bronze write and Control SQL finalization
are not one distributed transaction.


<a id="2--inspect-the-metadata"></a>

## 2: Inspect the metadata

**Read:** [Control Plane](control-plane.md). Inspect the read-only example queries for
`control.connection_settings`, `control.ingestion_config`, `control.pipeline_watermarks`, and
`audit.ingestion_log`.

**Inspect the definitions:** The [Fabric SQL Database Project](../../fabric/sqldb_ingestion_control.SQLDatabase/)
is the schema source of truth. The [Control schema bootstrap](../../scripts/control/01_create_control_schema.sql)
creates missing objects for a fresh install; it does not migrate an existing schema. The
[connection seed](../../scripts/control/03_seed_connection_settings.sql) and
[ingestion seed](../../scripts/control/04_seed_ingestion_metadata.sql) supply DEV examples: six E-commerce DATABASE
objects and two Logistics FILE objects.


<a id="3--trace-the-request-through-orchestration"></a>

## 3: Trace the request through orchestration

**Read:** [Pipeline Orchestration](pipeline-orchestration.md) and [Run Request Examples](../operations/run-request-examples.md).

Inspect `fabric/pl_ingest_orchestrator.DataPipeline/`, `pl_ingest_config_paginator.DataPipeline/`,
`pl_ingest_config_dispatcher.DataPipeline/`, `pl_ingest_object_controller.DataPipeline/`, and the DATABASE/FILE
router definitions under `fabric/`. Only the top-level Orchestrator is a supported external entry point.


<a id="4--follow-one-physical-ingestion-path"></a>

## 4: Follow one physical ingestion path

**DATABASE:** [SQL Server Guide](sql-server-database-ingestion.md) explains query-mode Copy for `FULL` and timestamp
`INCREMENTAL`; [Copy Performance](../architecture/database-copy-performance.md) explains supported `NONE` and
`DYNAMIC_RANGE` partition settings and benchmark limits.

**FILE:** [SFTP Guide](sftp-file-ingestion.md) traces Binary Copy into execution-scoped Landing and the
`nb_load_file_landing_to_bronze` Notebook; [FILE Design](../architecture/file-ingestion-design.md) records the
connector and parsing decisions. Only `DELIMITED_TEXT` is implemented.


<a id="5--reason-about-incremental-state"></a>

## 5: Reason about incremental state

**Read:** [Generic Incremental Watermark](../architecture/generic-incremental-watermark.md) and [Retry/Rerun/Backfill](../operations/retry-rerun-backfill.md).

Inspect [the SQL finalizer procedure](../../fabric/sqldb_ingestion_control.SQLDatabase/control/StoredProcedures/usp_finalize_ingestion_run.sql).
A normal incremental run derives a LOW/HIGH boundary; an eligible successful `REGULAR` run may advance the
checkpoint with optimistic protection. `BACKFILL` and no-new-data `SKIPPED` do not advance it.


<a id="6--inspect-failure-compensation-and-retries"></a>

## 6: Inspect failure compensation and retries

**Read:** [Bronze Compensating Cleanup](../operations/bronze-compensating-cleanup.md) and the [retry matrix](../operations/retry-rerun-backfill.md#retry-policy-by-side-effect).

Inspect `nb_cleanup_bronze_batch_rows.Notebook`, `nb_cleanup_landing_batch_files.Notebook`, and
`pl_ingest_incremental_finalize_recovery.DataPipeline` in `fabric/`. A failed Copy/Notebook or Finalizer activity
does not prove whether a durable write committed.


<a id="7--understand-what-monitoring-proves"></a>

## 7: Understand what monitoring proves

**Read:** [Operations Monitoring](../operations/monitoring-report.md) and [SQL monitoring views](../../scripts/monitoring/01_create_monitoring_views.sql).

The checked-in Power BI report/semantic model use DirectQuery over terminal **object-level audit**. They cannot show
in-progress runs or failures before an object audit. Optional Activator alert delivery has not been independently
verified.


<a id="8--rebuild-or-benchmark-when-needed"></a>

## 8: Rebuild or benchmark when needed

**For operators:** [Environment Rebuild](../operations/environment-rebuild.md) covers new-workspace bindings and
verification; [SQL Run Order](../../scripts/RUN_ORDER.md) covers the executable Control SQL / demo seed sequence;
[EC2/SFTP source setup](../../infra/source/README.md) handles optional source services. Do not treat Git as a backup
of historic Bronze rows, watermarks, audits, or secrets.

**For reviewers:** [Database Copy Performance](../architecture/database-copy-performance.md) records completed and
partial DEV Copy observations; [Pipeline Orchestration](pipeline-orchestration.md) records the small parallel-dispatch
comparison; and [Monitoring Report](../operations/monitoring-report.md) describes audit-based monitoring and its limits.
[Fabric Data Factory Limits](../architecture/fabric-data-factory-limits.md) documents platform guardrails, while
[Variable Library Bindings](../operations/variable-library-environment-binding.md) documents environment-specific IDs.

Verify results against genuine execution evidence, matching run identifiers before correlating captures.
Distinguish checked-in definitions from observed runtime behavior, and check whether benchmark measurements are
complete and rebuild outcomes have been independently verified. Development-workspace results do not establish
production-scale performance. Remove connection details and other sensitive information before sharing captures.
