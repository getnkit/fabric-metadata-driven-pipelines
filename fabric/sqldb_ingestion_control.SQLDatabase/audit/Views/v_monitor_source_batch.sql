CREATE VIEW audit.v_monitor_source_batch
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
