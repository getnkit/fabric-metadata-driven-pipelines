CREATE VIEW audit.v_monitor_object_history
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
