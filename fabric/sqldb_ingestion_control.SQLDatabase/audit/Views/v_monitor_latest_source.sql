CREATE VIEW audit.v_monitor_latest_source
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
