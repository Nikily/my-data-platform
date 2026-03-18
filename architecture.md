# Data Platform Architecture

## Overview

This document describes the architecture of the data platform, the decisions made, and the rationale behind them given the constraints and goals of the project.

**Goals:**
- Ingest data daily from multiple heterogeneous sources
- Perform incremental loads to avoid reprocessing historical data
- Transform raw data into analytics-ready models
- Serve data to Power BI Service and Power BI Desktop
- Keep the solution simple, maintainable, and entirely open source / free

**Constraints:**
- Low data volume (hundreds to low thousands of rows per day)
- Ubuntu server running as a VM on the company's Azure tenant
- No paid tooling beyond existing Azure and Power BI licenses

---

## Architecture Diagram

```
Sources
  ┌─────────────────────────────────────────────────────┐
  │  REST APIs  │  CSV (local)  │  CSV (SFTP)  │  ADLS  │
  └──────┬──────┴───────┬───────┴──────┬───────┴───┬────┘
         │              │              │            │
         └──────────────┴──────────────┘            │
                        │                           │
                  dlt (ingestion)         DuckDB azure+delta
                        │                  extensions (direct)
                        └──────────┬────────────────┘
                                   ▼
                            DuckDB (raw layer)
                                   │
                                  dbt
                                   │
                            DuckDB (transformed layer)
                                   │
                         Parquet export to Azure Blob / OneLake
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
             Power BI Service             Power BI Desktop
             (native connector)           (native connector)

   All steps orchestrated and scheduled by Dagster
```

---

## Component Decisions

### Orchestrator: Dagster

**Decision:** Use Dagster as the pipeline orchestrator and scheduler.

**Rationale:**
- Dagster uses an asset-based paradigm that maps naturally to data pipeline stages (raw ingestion asset → transformed asset → export asset). This makes lineage and dependencies explicit and easy to reason about.
- Dagster has first-class, maintained integrations for both dlt (`dagster-dlt`) and dbt (`dagster-dbt`), meaning the wiring between components requires minimal custom code.
- The Dagster UI (Dagit) provides observability out of the box: run history, asset health, logs, and alerts — important for a production pipeline running unattended on a server.
- Dagster runs as a persistent service (managed via systemd on Ubuntu) and supports cron-style scheduling for daily incremental runs.
- It is fully open source and free.

**Alternatives considered:**
- **Airflow**: More mature but significantly heavier to operate (requires a metadata database, separate scheduler, worker processes). Overkill for this scale.
- **Prefect**: Good alternative but adds a cloud control plane dependency in its most usable form.
- **Cron + shell scripts**: Too fragile. No observability, no dependency management, no retry logic.

---

### Ingestion: dlt (data load tool)

**Decision:** Use dlt for ingesting data from REST APIs, local CSV files, and SFTP CSV files into DuckDB.

**Rationale:**
- dlt handles the full ingestion lifecycle: schema inference, type casting, incremental state tracking, and writing to the destination — with minimal boilerplate.
- It has a native DuckDB destination, so no intermediate storage or connectors are required.
- Incremental loading is built in via `dlt` cursors and state — it tracks the last loaded watermark per source and only fetches new records on subsequent runs.
- The filesystem source covers both local CSV files and SFTP-hosted CSV files without needing a separate tool.
- REST API sources can be configured declaratively or with a small amount of Python.
- The `dagster-dlt` integration wraps dlt pipelines as Dagster assets, making orchestration seamless.

**Alternatives considered:**
- **Airbyte**: More connectors out of the box, but requires Docker and a running server — heavy for this scale and makes the Ubuntu server harder to manage.
- **Singer taps**: Older ecosystem, less actively maintained.
- **Custom Python scripts**: Viable but means reinventing incremental state tracking, schema management, and error handling that dlt provides for free.

---

### Azure Dataverse / OneLake Source

**Decision:** Ingest Dataverse data by reading directly from the underlying ADLS Gen2 / OneLake storage layer (via Delta tables written by Fabric Link or Synapse Link for Dataverse), rather than through the Dataverse Web API.

**Rationale:**
- The Dataverse API imposes rate limits and is designed for transactional access, not bulk analytical extraction.
- When Fabric Link (or Synapse Link) for Dataverse is enabled, the data is continuously replicated to OneLake / ADLS Gen2 as Delta tables in an open format.
- DuckDB can read Delta tables directly from ADLS Gen2 using its `delta` and `azure` extensions, requiring no intermediate ETL step for this source.
- This approach is more efficient, avoids API overhead, and gives access to the full dataset in a format DuckDB is optimized to read.

**Prerequisite:** Fabric Link or Synapse Link for Dataverse must be enabled by your Azure administrator, and the ADLS Gen2 path / OneLake lakehouse path must be provided.

**Fallback:** If the link is not available, a custom dlt source against the Dataverse Web API is a viable alternative at this data volume.

---

### Analytics Storage: DuckDB

**Decision:** Use DuckDB as the internal analytics database for raw staging and dbt transformations.

**Rationale:**
- DuckDB is a columnar, analytical SQL engine optimized for exactly the kind of aggregations and joins that dbt transformation models produce. It significantly outperforms row-based databases for this workload.
- It requires no server, daemon, or infrastructure — it is a single file on disk. This matches the operational simplicity goal of running on a single Ubuntu VM.
- The `dbt-duckdb` adapter is mature and well maintained.
- dlt writes to DuckDB natively as its destination.
- DuckDB can read Parquet, CSV, JSON, and Delta files directly, which is useful when pulling from ADLS.
- It is fully open source and free.
- **Importantly**, in this architecture DuckDB is used purely as an internal transformation engine. Power BI does not connect to it directly (see Serving Layer below), which eliminates the single-writer concurrency limitation as a concern.

**Alternatives considered:**
- **PostgreSQL**: Free and battle-tested, but row-oriented and slower for analytical workloads. Requires a running server process to manage. Would make sense if multi-user concurrent write access were needed, which it is not in a daily batch pipeline.
- **SQLite**: Not suited for analytical workloads.
- **ClickHouse**: Excellent analytical engine but significantly more complex to operate. Overkill for this volume.

---

### Transformation: dbt

**Decision:** Use dbt (with the `dbt-duckdb` adapter) for all data transformations.

**Rationale:**
- dbt is the industry standard for SQL-based transformation in modern data pipelines. It brings software engineering practices to SQL: version control, testing, documentation, and modular models.
- It integrates cleanly with DuckDB via the `dbt-duckdb` adapter.
- The `dagster-dbt` integration wraps dbt models as Dagster assets, giving full lineage visibility in the Dagster UI.
- dbt's layered model convention (staging → intermediate → marts) provides a clean separation between raw ingested data and analytics-ready output.
- It is fully open source and free.

---

### Serving Layer: Parquet on Azure Blob Storage / OneLake

**Decision:** At the end of each pipeline run, export final dbt models as Parquet files to Azure Blob Storage or Microsoft OneLake, and connect Power BI to those files.

**Rationale:**

This decision resolves the Power BI connectivity challenge cleanly:

- Power BI Service and Power BI Desktop both have **native connectors for Azure Blob Storage and OneLake** — no gateway, no ODBC driver, no additional infrastructure required.
- Since the Ubuntu VM is already on the company's Azure tenant, writing Parquet files to Azure Blob Storage is straightforward and incurs only minimal storage cost.
- Parquet is a columnar format that Power BI reads efficiently. Import mode in Power BI will cache the data, so query performance is not dependent on the server.
- This decouples the pipeline execution from Power BI consumption entirely — Power BI reads the last successfully written export, and pipeline runs do not interfere with BI users.
- It avoids the DuckDB concurrent access limitation (single writer) since Power BI never touches the DuckDB file.

**Alternatives considered:**
- **Direct DuckDB ODBC from Power BI**: Requires the on-premises data gateway installed on Ubuntu (or a Windows machine). Adds operational complexity and a gateway dependency. Rejected in favour of the simpler Parquet approach.
- **Azure SQL Database as serving layer**: Reliable and Power BI-native, but introduces a paid Azure resource and an additional sync step.
- **MotherDuck**: Cloud-hosted DuckDB with Power BI connectivity. Adds cost and an external dependency.

---

## Data Flow: Incremental Load Strategy

Each source uses an incremental load pattern to avoid reprocessing historical data:

| Source | Incremental mechanism |
|---|---|
| REST APIs | dlt cursor field (e.g. `updated_at` or `created_at`) stored in dlt state |
| Local CSV files | File modification timestamp or filename date pattern |
| SFTP CSV files | File modification timestamp via dlt filesystem source |
| ADLS / OneLake (Delta) | Delta table transaction log — DuckDB reads only new files/versions |

Dagster schedules all pipelines to run daily, typically during off-peak hours.

---

## Infrastructure Summary

| Component | Technology | Hosting |
|---|---|---|
| Orchestrator | Dagster (systemd service) | Ubuntu VM on Azure |
| Ingestion | dlt | Ubuntu VM on Azure |
| Analytics DB | DuckDB (file) | Ubuntu VM on Azure |
| Transformation | dbt | Ubuntu VM on Azure |
| Serving layer | Parquet files | Azure Blob Storage / OneLake |
| BI consumption | Power BI Service + Desktop | Microsoft cloud / client machines |

---

## What This Architecture Is Not

- **Not real-time**: This is a daily batch pipeline. It is not designed for streaming or sub-hourly freshness.
- **Not multi-tenant**: A single DuckDB file serves a single pipeline. Concurrent write access from multiple processes is not supported and not needed.
- **Not horizontally scalable**: Designed for the current low volume. If data volume grows significantly (tens of millions of rows), the DuckDB file and single-VM approach should be revisited.
