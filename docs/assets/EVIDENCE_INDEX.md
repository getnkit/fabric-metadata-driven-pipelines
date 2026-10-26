# Evidence Index

The published guides use 30 visual evidence assets: 23 original PNGs, two SVG diagrams and five derived composites. Sixteen original composite inputs are retained separately, for 46 evidence assets in total. The [architecture overview](architecture-overview.svg) is an additional visual outside this inventory (47 visual files overall).

Captions and adjacent paragraphs in the linked guides define the supported claims and evidence limitations. Asset names identify subjects; they do not establish execution correlation.

## Published assets

C04 is a five-image group covering pagination, dispatch and routing; C07 is a two-image group covering FILE routing and the SFTP incremental adapter. P01 contains three metadata snapshots. These groups have no standalone image.

### Core evidence

| ID | Asset | Documentation |
| --- | --- | --- |
| C01 | [c01-control-metadata.png](screenshots/core/c01-control-metadata.png) | [control-plane](../guides/control-plane.md) |
| C02 | [c02-logical-connections.png](screenshots/core/c02-logical-connections.png) | [control-plane](../guides/control-plane.md) |
| C03 | [c03-master-orchestration.png](screenshots/core/c03-master-orchestration.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C04 | [c04-01-pagination.png](screenshots/core/c04-01-pagination.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C04 | [c04-02-dispatcher.png](screenshots/core/c04-02-dispatcher.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C04 | [c04-03-database-controller.png](screenshots/core/c04-03-database-controller.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C04 | [c04-04-file-controller.png](screenshots/core/c04-04-file-controller.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C04 | [c04-05-database-router.png](screenshots/core/c04-05-database-router.png) | [pipeline-orchestration](../guides/pipeline-orchestration.md) |
| C05 | [c05-sql-server-copy-execution.png](screenshots/core/c05-sql-server-copy-execution.png) | [sql-server-database-ingestion](../guides/sql-server-database-ingestion.md) |
| C06 | [c06-sql-bronze-lineage.png](screenshots/core/c06-sql-bronze-lineage.png) | [sql-server-database-ingestion](../guides/sql-server-database-ingestion.md) |
| C07 | [c07-01-file-router.png](screenshots/core/c07-01-file-router.png) | [sftp-file-ingestion](../guides/sftp-file-ingestion.md) |
| C07 | [c07-02-sftp-incremental-adapter.png](screenshots/core/c07-02-sftp-incremental-adapter.png) | [sftp-file-ingestion](../guides/sftp-file-ingestion.md) |
| C08 | [c08-sftp-landing.png](screenshots/core/c08-sftp-landing.png) | [sftp-file-ingestion](../guides/sftp-file-ingestion.md) |
| C09 | [c09-sftp-bronze-lineage.png](screenshots/core/c09-sftp-bronze-lineage.png) | [sftp-file-ingestion](../guides/sftp-file-ingestion.md) |
| C10 | [c10-no-new-data-skipped.png](screenshots/composites/c10-no-new-data-skipped.png) | [generic-incremental-watermark](../architecture/generic-incremental-watermark.md) |
| C11 | [c11-sql-server-incremental.png](screenshots/composites/c11-sql-server-incremental.png) | [sql-server-database-ingestion](../guides/sql-server-database-ingestion.md) |
| C12 | [c12-sftp-new-file-incremental.png](screenshots/composites/c12-sftp-new-file-incremental.png) | [sftp-file-ingestion](../guides/sftp-file-ingestion.md) |
| C13 | [c13-incremental-backfill.png](screenshots/composites/c13-incremental-backfill.png) | [retry-rerun-backfill](../operations/retry-rerun-backfill.md) |
| C14 | [c14-ambiguous-run-scope.png](screenshots/core/c14-ambiguous-run-scope.png) | [run-request-examples](../operations/run-request-examples.md) |
| C15 | [c15-operations-report.png](screenshots/core/c15-operations-report.png) | [monitoring-report](../operations/monitoring-report.md) |
| C16 | [c16-operations-filter.png](screenshots/core/c16-operations-filter.png) | [monitoring-report](../operations/monitoring-report.md) |

### Performance evidence

| ID | Asset | Documentation |
| --- | --- | --- |
| P01 | [p01-b1-none-no-override.png](screenshots/performance/source-config/p01-b1-none-no-override.png) | [database-copy-performance](../architecture/database-copy-performance.md) |
| P01 | [p01-b2-dynamic-range-no-override.png](screenshots/performance/source-config/p01-b2-dynamic-range-no-override.png) | [database-copy-performance](../architecture/database-copy-performance.md) |
| P01 | [p01-b3-dynamic-range-override-4.png](screenshots/performance/source-config/p01-b3-dynamic-range-override-4.png) | [database-copy-performance](../architecture/database-copy-performance.md) |
| P02 | [p02-auto-used-1-copy.png](screenshots/performance/p02-auto-used-1-copy.png) | [database-copy-performance](../architecture/database-copy-performance.md) |
| P03 | [p03-auto-used-4-copies.png](screenshots/performance/p03-auto-used-4-copies.png) | [database-copy-performance](../architecture/database-copy-performance.md) |
| P04 | [p04-tuned-used-4-copies.png](screenshots/performance/p04-tuned-used-4-copies.png) | [database-copy-performance](../architecture/database-copy-performance.md) |

P01 records configuration, not completed execution linkage. P02–P04 filenames describe the visible AUTO/TUNED branch and observed used parallel copies, not independently verified partition settings. [P05](../architecture/database-copy-performance.md#completed-dev-copy-observations--2026-10-24) is a **qualified descriptive Markdown table**, not an image or controlled speedup comparison. Configuration-to-run linkage, resource conditions and target pre-run state are not independently established; no causal performance gain or general tuning recommendation is inferred.

### Architecture diagrams

| ID | Asset | Documentation |
| --- | --- | --- |
| D01 | [d01-control-audit-er.svg](diagrams/d01-control-audit-er.svg) | [control-plane](../guides/control-plane.md) |
| D02 | [d02-environment-binding.svg](diagrams/d02-environment-binding.svg) | [variable-library-environment-binding](../operations/variable-library-environment-binding.md) |

### Optional evidence

| ID | Asset | Documentation |
| --- | --- | --- |
| O02 | [o02-file-vs-row-count.png](screenshots/composites/o02-file-vs-row-count.png) | [file-ingestion-design](../architecture/file-ingestion-design.md) |

## Composite sources and reproduction

All 16 source PNGs below retain their original names and bytes. Adjacent manifests record source paths, SHA-256 hashes, dimensions, placements, transformations, supported claims and limitations. C10/C13 retain both byte-identical watermark inputs and display state once; duplicate files do not establish independent before/after observations.

Use Python with `Pillow==11.3.0` from the repository root. Run the linked builders with `python scripts/evidence/<builder>.py`; they regenerate the five PNGs and their manifests.

| Composite | Retained original sources | Builder / manifest |
| --- | --- | --- |
| C10 (4 inputs) | [cx-s2-no-bronze-append.png](screenshots/supporting/s2-no-new-data/cx-s2-no-bronze-append.png)<br>[cx-s2-skipped-audit.png](screenshots/supporting/s2-no-new-data/cx-s2-skipped-audit.png)<br>[cx-s2-watermark-after.png](screenshots/supporting/s2-no-new-data/cx-s2-watermark-after.png)<br>[cx-s2-watermark-before.png](screenshots/supporting/s2-no-new-data/cx-s2-watermark-before.png) | [build_incremental_composites.py](../../scripts/evidence/build_incremental_composites.py)<br>[Manifest](screenshots/composites/c10-no-new-data-skipped.manifest.json) |
| C11 (3 inputs) | [cx-s3-audit-success.png](screenshots/supporting/s3-sql-incremental/cx-s3-audit-success.png)<br>[cx-s3-watermark-after.png](screenshots/supporting/s3-sql-incremental/cx-s3-watermark-after.png)<br>[cx-s3-watermark-before.png](screenshots/supporting/s3-sql-incremental/cx-s3-watermark-before.png) | [build_c11_composite.py](../../scripts/evidence/build_c11_composite.py)<br>[Manifest](screenshots/composites/c11-sql-server-incremental.manifest.json) |
| C12 (4 inputs) | [cx-s4-audit-success.png](screenshots/supporting/s4-sftp-incremental/cx-s4-audit-success.png)<br>[cx-s4-bronze-new-file-lineage.png](screenshots/supporting/s4-sftp-incremental/cx-s4-bronze-new-file-lineage.png)<br>[cx-s4-watermark-after.png](screenshots/supporting/s4-sftp-incremental/cx-s4-watermark-after.png)<br>[cx-s4-watermark-before.png](screenshots/supporting/s4-sftp-incremental/cx-s4-watermark-before.png) | [build_sftp_composites.py](../../scripts/evidence/build_sftp_composites.py)<br>[Manifest](screenshots/composites/c12-sftp-new-file-incremental.manifest.json) |
| C13 (3 inputs) | [cx-s5-audit-backfill.png](screenshots/supporting/s5-backfill/cx-s5-audit-backfill.png)<br>[cx-s5-watermark-after.png](screenshots/supporting/s5-backfill/cx-s5-watermark-after.png)<br>[cx-s5-watermark-before.png](screenshots/supporting/s5-backfill/cx-s5-watermark-before.png) | [build_incremental_composites.py](../../scripts/evidence/build_incremental_composites.py)<br>[Manifest](screenshots/composites/c13-incremental-backfill.manifest.json) |
| O02 (2 inputs) | [cx-o02-binary-copy.png](screenshots/supporting/optional/o02-file-row-count/cx-o02-binary-copy.png)<br>[cx-o02-notebook-parse.png](screenshots/supporting/optional/o02-file-row-count/cx-o02-notebook-parse.png) | [build_sftp_composites.py](../../scripts/evidence/build_sftp_composites.py)<br>[Manifest](screenshots/composites/o02-file-vs-row-count.manifest.json) |

O02 preserves genuine UI crops at native scale without resizing, retaining original line wrapping. Both Notebook row metrics reuse one parsed DataFrame count, not an independent Bronze recount. Exact end-to-end execution linkage is unverified.

## Omitted candidates

- O01 and O05 are omitted from the published evidence set because exact execution linkage was not independently established. Their unpublished captures were removed; publishing either scenario would require additional correlation evidence.
- O03 and O04 were excluded from the final publication scope.

## Removed capture ledger

The owner authorized removal after confirming independent backups. The following 19 historical filenames are plain text, not links to current assets.

**Optional S1 details (12):** distinct details outside the approved publication scope.

- `cx-s1-config-pagination-detail-2.png`
- `cx-s1-database-router-detail-2.png`
- `cx-s1-dispatcher-execution-detail.png`
- `cx-s1-file-router-detail-2.png`
- `cx-s1-master-orchestration-detail.png`
- `cx-s1-object-controller-database-detail.png`
- `cx-s1-object-controller-file-detail.png`
- `cx-s1-sftp-incremental-adapter-1.png`
- `cx-s1-sftp-incremental-adapter-detail-1.png`
- `cx-s1-sftp-incremental-adapter-detail-2.png`
- `cx-s1-sql-server-full-adapter-detail.png`
- `cx-s1-sql-server-full-adapter.png`

**Redundant S1 overviews (3):** the selected published detail captures provide clearer evidence.

- `cx-s1-config-pagination.png`
- `cx-s1-database-router.png`
- `cx-s1-file-router.png`

**Unpublished O01/O05 captures (4):** insufficient independently verified exact execution linkage.

- `cx-o01-audit.png`
- `cx-o05-batch-audit.png`
- `cx-o05-paginator-selection.png`
- `cx-o05-source-scope-input.png`
