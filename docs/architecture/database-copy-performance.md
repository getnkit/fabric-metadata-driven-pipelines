# Database Copy Performance Strategy

This document describes the SQL Server Copy settings and their DEV evidence.
The [SQL Server ingestion guide](../guides/sql-server-database-ingestion.md) follows the corresponding execution path.

## Implemented scope

The SQL Server adapter uses Copy activities in Fabric Data Pipelines to ingest data into Bronze.
The tested source environment is SQL Server 2022 Developer running on EC2.

Official references:

- https://learn.microsoft.com/en-us/fabric/data-factory/connector-sql-server-copy-activity
- https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-performance-features

## Metadata model

`control.ingestion_config.copy_options` holds optional connector-native tuning settings. It is separate from
`source_options`, which controls source reading and parsing. A JSON envelope keeps connector-specific hints out
of the shared table's column structure.

### Supported Copy configuration

`copy_options = NULL` selects `NONE` partitioning and service-managed `AUTO` parallelism.

Dynamic range example:

```json
{
  "partition_option": "DYNAMIC_RANGE",
  "partition_column": "order_item_id"
}
```

Optional explicit override:

```json
{
  "partition_option": "DYNAMIC_RANGE",
  "partition_column": "order_item_id",
  "parallel_copies": 8
}
```

The value `8` illustrates syntax; it is not a measured recommendation.

Supported partitioning for `FULL` and `INCREMENTAL`:

```text
partition_option = NONE | DYNAMIC_RANGE
```

All SQL Server ingestion uses **query-mode Copy**. `_ingestion_timestamp` is
CAST to `DATETIME2(6)` in the source query, so newly created Bronze Delta
tables receive a timestamp technical column rather than a String. Physical
source table layout is independent of this connector execution strategy.

`DYNAMIC_RANGE` requires an explicit `partition_column`. The current adapter
does not silently auto-select a PK/index because an explicit column makes the
per-object execution policy reviewable and deterministic.

`parallel_copies` is optional. Do not populate it from row count alone. Omitted
means Fabric chooses the parallel-copy degree. A positive integer is an explicit
operator override and should be retained only after representative performance
testing shows a measurable benefit or a source-load constraint requires it.

The pipeline normalizes an omitted `parallel_copies` to parameter value `0`
solely for routing. This sentinel is never passed to Copy.

## Runtime flow

The ingestion pipeline maps the configured Copy options to these execution parameters:

```text
p_copy_partition_option
p_copy_partition_column
p_copy_parallel_copies
```

After validating the settings, execution selects one of two query-mode Copy branches:

```text
p_copy_parallel_copies = 0
  -> copy_source_to_bronze_auto
     (parallelCopies omitted)

p_copy_parallel_copies > 0
  -> copy_source_to_bronze_tuned
     (parallelCopies = configured override)
```

Both modes use the same partition strategy.

For `NONE`:

```text
partitionOption = None
```

For `DYNAMIC_RANGE`:

```text
partitionOption = DynamicRange
partitionColumnName = configured partition_column
```

The query contains Fabric's required range placeholder:

```sql
?DfDynamicRangePartitionCondition
```

### FULL query shape

```sql
SELECT
    *,
    <technical metadata columns>
FROM <schema>.<table>
WHERE ?DfDynamicRangePartitionCondition
```

The `WHERE` clause is added only for `DYNAMIC_RANGE`.

### INCREMENTAL query shape

```sql
SELECT
    *,
    <technical metadata columns>
FROM <schema>.<table>
WHERE ?DfDynamicRangePartitionCondition
  AND <watermark_field> > LOW
  AND <watermark_field> <= HIGH
```

For `NONE`, only the normal watermark predicate is generated.

The custom-query templates deliberately omit a terminal semicolon. For
`DYNAMIC_RANGE`, Fabric can wrap the source query as a derived table while
discovering partition bounds. A terminal `;` inside that wrapper can make the
wrapped SQL invalid even though the same standalone query is valid SQL.

Fabric can derive dynamic-range bounds for the configured partition column. They are
not stored as permanent metadata because static bounds age as source data grows.
Explicit bounds would require evidence that range discovery is a material cost.

## Seeded example

The seed enables dynamic range on the largest relational demo object:

```text
sales.order_items
partition_option = DYNAMIC_RANGE
partition_column = order_item_id
parallel_copies  = AUTO
```

The default fixture has only 60,000 rows, so this proves routing/functionality,
not a large-scale performance gain. Production tuning claims require a larger
representative dataset and measured run metrics.

Other DATABASE seed objects remain `copy_options = NULL`, providing a baseline
for the normal non-partitioned path.

## Query-only choice and performance benchmark

The framework deliberately does **not** expose the SQL Server connector's
`PhysicalPartitionsOfTable` / `PHYSICAL_PARTITIONS` Table-mode strategy.
Table mode may help for some SQL Server physical layouts. However, its `additionalColumns` path creates
`_ingestion_timestamp` as String unless destination mapping is set explicitly.
A DEV PoC confirmed that a manual `timestamp` mapping works on a newly
created Bronze table (SQL endpoint: `datetime2(6)`), but manually maintained
per-source mappings conflict with schema-agnostic metadata-driven ingestion.
Generating per-source mapping JSON would add maintenance and runtime coupling.

Instead, query-mode `SELECT *, CAST(... AS DATETIME2(6))` preserves the
Bronze timestamp contract and still supports `DYNAMIC_RANGE` with
`?DfDynamicRangePartitionCondition` for connector-native parallel Copy.
It is **not** assumed to be equal in throughput to native physical partition
scanning; performance depends on source table layout, indexes, partition-key
distribution, and measured bottlenecks.

`PHYSICAL_PARTITIONS` is **unsupported** and fails
`INVALID_COPY_OPTIONS` in the `FULL` adapter. Do not silently change an
existing production config to `NONE`; review its intended policy. The
DEV benchmark scenario selector replaces the retired
`PARTITIONED_PHYSICAL` case with `PARTITIONED_DYNAMIC` and can normalize
legacy **BENCHMARK** metadata during scenario selection.

### Permanent benchmark fixture

The benchmark remains a separate **database on the same EC2 SQL Server
2022 Developer instance**:

```text
sql_benchmark_db
```

Two 10,000,000-row source tables retain the **same logical data** and
`CHAR(512)` payload but have different SQL Server physical layouts:

```text
benchmark.copy_source_unpartitioned
benchmark.copy_source_partitioned
```

The partitioned source uses monthly `event_date` partitions in 2026,
which are a **source SQL Server** characteristic, not a Fabric Copy option.
Both tables have `event_date`; for a focused 2x2
comparison, the two `DYNAMIC_RANGE` scenarios both partition connector reads
by this date column, aligned with the partitioned table's physical key.
This can allow SQL Server partition elimination but does not guarantee a speedup;
the physical tables also differ in clustered-index layout. Four benchmark
scenarios vary source layout versus connector execution strategy:

```text
UNPARTITIONED_NONE        (query, NONE)
UNPARTITIONED_DYNAMIC     (query, DYNAMIC_RANGE on event_date)
PARTITIONED_NONE          (query, NONE)
PARTITIONED_DYNAMIC       (query, DYNAMIC_RANGE on event_date)
```

The same fixture data supports all four scenarios without regeneration.

The following DEV configuration snapshots show config 10 as active and config 9 as inactive.
The `requested_parallel_copies` column is a scenario-selector input repeated across output rows, not an observed
runtime parallelism measurement. These snapshots demonstrate metadata configuration, not completed execution
results or independently verified configuration-to-run linkage.

[![B1 benchmark metadata with NONE and no parallel override](../assets/screenshots/performance/source-config/p01-b1-none-no-override.png)](../assets/screenshots/performance/source-config/p01-b1-none-no-override.png)

*P01-B1: Metadata for `copy_source_partitioned` sets `partition_option = NONE` with no `parallel_copies` override; `requested_parallel_copies` is `NULL`.*

[![B2 benchmark metadata with DYNAMIC_RANGE on event_date and no override](../assets/screenshots/performance/source-config/p01-b2-dynamic-range-no-override.png)](../assets/screenshots/performance/source-config/p01-b2-dynamic-range-no-override.png)

*P01-B2: Metadata for `copy_source_partitioned` sets `DYNAMIC_RANGE` on `event_date` with no override. Checked-in routing selects service-managed `AUTO`.*

[![B3 benchmark metadata with DYNAMIC_RANGE on event_date and explicit override 4](../assets/screenshots/performance/source-config/p01-b3-dynamic-range-override-4.png)](../assets/screenshots/performance/source-config/p01-b3-dynamic-range-override-4.png)

*P01-B3: Metadata for `copy_source_partitioned` requests `DYNAMIC_RANGE` on `event_date` with an explicit `parallel_copies` override of `4`.*

## Observed AUTO vs explicit zero (DEV, 2026-10-12)

A separate temporary Copy Activity tested the same **10,000,000-row**
`benchmark.copy_source_partitioned` using query-mode `DYNAMIC_RANGE`
on `event_date`. With the Copy payload explicitly setting
`"parallelCopies": 0`, the run **succeeded**, copying 10,000,000 rows;
`usedParallelCopies = 1`, `copyDuration = 483` seconds, reported
throughput approximately **23.08 MB/s**, and `usedDataIntegrationUnits = 4`.

With the property **omitted** (the native `AUTO` mode), the run was
observed **in progress** using `usedParallelCopies = 4`. This is direct
evidence of **different runtime parallelism** between omitted vs zero in
this workload; it does **not** establish a completed `AUTO` elapsed-time
or representative throughput benchmark. Do not promote the partial `AUTO`
result into a performance-speedup claim.

**Design consequence:** keep `if_parallel_copy_override` and two Copy
branches (`AUTO` omits the property; `TUNED` supplies a positive override).
The pipeline parameter `0` is strictly a routing sentinel and must
not be forwarded as a numeric `parallelCopies` value. This is a
behavioral guardrail, not an instruction to tune every source manually.

## Benchmark procedure

Use representative data volume and compare the same source/sink path.

Recommended sequence:

```text
1. AUTO parallelism + NONE or DYNAMIC_RANGE baseline
2. Record rows, bytes, duration, throughput, and source DB load
3. If needed, test a small explicit parallel_copies override
4. Increase gradually only while throughput materially improves
5. Stop when source/sink pressure rises without meaningful throughput gain
6. Persist the override in copy_options only when evidence supports it
```

Do not infer the number from row count alone. Row width, source indexes, skew,
database compute, network capacity, sink throughput, concurrent workloads, and
the selected partition column all affect the useful parallelism.

<a id="completed-dev-copy-observations--2026-10-24"></a>

### Completed DEV Copy observations (2026-10-24)

These completed observations are separate from the explicit-zero versus omitted-`AUTO` test above.
The visible activity names identify `AUTO` or `TUNED` branches; `AUTO` omits
`parallelCopies`, while `TUNED` supplies a positive explicit override. A successful Copy activity does not
independently prove terminal SQL audit `SUCCESS`.

[![Completed AUTO Copy reporting one used parallel copy](../assets/screenshots/performance/p02-auto-used-1-copy.png)](../assets/screenshots/performance/p02-auto-used-1-copy.png)

*P02: `copy_source_to_bronze_auto` reports `Succeeded`, with 10,000,000 rows read/written and one used parallel copy.*

Partition settings are not shown in P02.

[![Completed AUTO Copy reporting four used parallel copies](../assets/screenshots/performance/p03-auto-used-4-copies.png)](../assets/screenshots/performance/p03-auto-used-4-copies.png)

*P03: `copy_source_to_bronze_auto` reports `Succeeded`, with 10,000,000 rows read/written and four used parallel copies.*

[![Completed TUNED Copy reporting four used parallel copies](../assets/screenshots/performance/p04-tuned-used-4-copies.png)](../assets/screenshots/performance/p04-tuned-used-4-copies.png)

*P04: `copy_source_to_bronze_tuned` reports `Succeeded`, with 10,000,000 rows read/written and four used parallel copies.*

The cause of the duration difference is unverified.

All three Copy captures report `Succeeded`, **10,000,000 rows read and written**, and **12.552 GB data read**.
The descriptive table retains the Copy details **Total duration** and the activity-list **Duration** as separate
observations; neither is substituted for the other. Times are recorded as displayed, without assuming a timezone.

| Capture | Copy branch | Used parallel copies | Copy Total duration | Activity duration | Throughput | Data written / files |
| --- | --- | ---: | --- | --- | ---: | --- |
| P02 | `AUTO` | 1 | 00:05:16 | 5m 25s | 40.753 MB/s | 565.69 MB / 5 |
| P03 | `AUTO` | 4 | 00:04:33 | 4m 43s | 47.011 MB/s | 571.46 MB / 8 |
| P04 | `TUNED` | 4 | 00:02:34 | 2m 43s | 85.388 MB/s | 571.46 MB / 8 |

*P05: Descriptive summary of three completed Copy captures.*

Configuration-to-run linkage, resource conditions and target pre-run state are unverified.
No controlled speedup or general tuning recommendation is inferred.

Result filenames do not prove resolved partition settings. P03 and P04 both report four used parallel copies;
their duration difference does not
independently establish an explicit-override performance benefit. DIUs, Fabric capacity, EC2 resource utilization,
Copy inputs, cache state, and repeated-trial conditions are not established by these captures. The reviewed set
does not provide a completed comparable result for the unpartitioned source layout.

## Extension boundary

Supported `copy_options` keys are connector-specific. The DATABASE router must not
assume that other connectors support SQL Server's partition mechanisms.

### EC2 SQL Server Developer sizing note

The [benchmark setup guide](../../scripts/source/benchmark-db/README.md#storage-safety) covers EBS space, SQL
data/log growth and test costs. Its 80 GiB EBS assumption is not a sizing guarantee. Retest `SqlServerSource`
query-mode and partition options in Fabric DEV; repository validation alone does not establish runtime acceptance.
