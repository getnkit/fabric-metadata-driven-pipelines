/*
  DEV: Run in sqldb_ingestion_control after the existing Control/Audit Plane.
  Read-only monitoring views. No changes to audit data, watermarks or pipelines.
  SQL Project definitions in fabric/ are the physical source of truth.
*/
CREATE OR ALTER VIEW audit.v_monitor_source_batch
AS
SELECT
    COALESCE(NULLIF(LTRIM(RTRIM(source_system)), N''), N'UNKNOWN') AS source_system,
    CAST(batch_id AS NVARCHAR(36)) AS batch_id,
    COUNT_BIG(*) AS object_count,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_count,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_count,
    SUM(CASE WHEN status = 'SKIPPED' THEN 1 ELSE 0 END) AS skipped_count,
    CASE
        WHEN MAX(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) = 1 THEN 'FAILED'
        WHEN MAX(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) = 1 THEN 'CANCELLED'
        WHEN MAX(CASE WHEN status = 'WARN' THEN 1 ELSE 0 END) = 1 THEN 'WARN'
        WHEN MAX(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) = 1 THEN 'SUCCESS'
        ELSE 'SKIPPED'
    END AS source_status,
    SUM(COALESCE(source_row_count, 0)) AS source_rows,
    SUM(COALESCE(target_row_count, 0)) AS target_rows,
    MIN(start_time) AS batch_start_time,
    MAX(end_time) AS batch_end_time
FROM audit.ingestion_log
GROUP BY
    COALESCE(NULLIF(LTRIM(RTRIM(source_system)), N''), N'UNKNOWN'),
    batch_id;
GO

CREATE OR ALTER VIEW audit.v_monitor_latest_source
AS
WITH ranked_batches AS
(
    SELECT *,
           ROW_NUMBER() OVER
           (
               PARTITION BY source_system
               ORDER BY batch_end_time DESC, batch_id DESC
           ) AS recency_rank
    FROM audit.v_monitor_source_batch
)
SELECT
    source_system,
    batch_id,
    object_count,
    success_count,
    failed_count,
    skipped_count,
    source_rows,
    target_rows,
    batch_start_time,
    batch_end_time,
    source_status
FROM ranked_batches
WHERE recency_rank = 1;
GO

CREATE OR ALTER VIEW audit.v_monitor_object_history
AS
SELECT
    ingestion_log_id,
    COALESCE(NULLIF(LTRIM(RTRIM(source_system)), N''), N'UNKNOWN') AS source_system,
    CASE
        WHEN NULLIF(source_schema, N'') IS NOT NULL
        THEN CONCAT(source_schema, N'.', source_object)
        ELSE source_object
    END AS source_entity,
    ingestion_config_id,
    CAST(batch_id AS NVARCHAR(36)) AS batch_id,
    pipeline_run_id,
    run_type,
    load_strategy,
    status,
    source_row_count,
    target_row_count,
    duration_seconds,
    start_time,
    end_time,
    error_code,
    error_message
FROM audit.ingestion_log;
GO

SELECT source_system, batch_id, source_status, object_count,
       success_count, skipped_count, failed_count, batch_end_time
FROM audit.v_monitor_latest_source
ORDER BY source_system;
GO

SELECT TOP (20) source_system, source_entity, status, end_time,
                error_code
FROM audit.v_monitor_object_history
ORDER BY end_time DESC, ingestion_log_id DESC;
GO
