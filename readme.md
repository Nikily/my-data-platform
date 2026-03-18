# My Data Platform

This repository contains all components needed to run robust data pipelines on an Ubuntu server.

See [architecture.md](architecture.md) for a full explanation of every design decision.

## Stack

| Layer | Tool |
|---|---|
| Orchestration | Dagster |
| Ingestion | dlt |
| Transformation | dbt (dbt-duckdb) |
| Analytics storage | DuckDB |
| Serving layer | Parquet → Azure Blob Storage |
| BI | Power BI Service + Desktop |

## Project structure

```
.
├── pipeline/                  # Dagster project
│   ├── definitions.py         # Dagster Definitions entry point
│   ├── assets/
│   │   ├── sources/           # Ingestion assets (REST API, CSV, SFTP, ADLS Delta)
│   │   └── export/            # Parquet export to Azure Blob
│   └── schedules/             # Daily cron schedule
├── dbt_project/               # dbt project (staging → marts)
│   └── models/
│       ├── staging/           # One model per raw source
│       └── marts/             # Analytics-ready tables exported to Power BI
├── scripts/                   # One-off utility scripts
├── systemd/                   # systemd service files for Dagster
├── setup.sh                   # Bootstrap script for the Ubuntu server
├── pyproject.toml             # Python dependencies
├── dagster.yaml               # Dagster instance configuration
└── .env.example               # All required environment variables
```

## Server setup (Ubuntu)

Run these commands on the Ubuntu server after cloning the repo.

```bash
git clone https://github.com/Nikily/my-data-platform.git /opt/my_data_platform
cd /opt/my_data_platform
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Install Python 3.12 and system dependencies
- Create a virtual environment and install all Python packages
- Install DuckDB extensions (azure, delta)
- Install dbt packages
- Create data directories
- Copy `.env.example` → `.env`
- Install and enable the Dagster systemd services

After setup, fill in your credentials:

```bash
nano /opt/my_data_platform/.env
```

Then start the services:

```bash
sudo systemctl start dagster-webserver dagster-daemon
sudo systemctl status dagster-webserver dagster-daemon
```

## Accessing the Dagster UI

The webserver runs on `localhost:3000` (bound to loopback for security).
Use an SSH tunnel from your local machine:

```bash
ssh -L 3000:localhost:3000 <user>@<server-ip>
```

Then open `http://localhost:3000` in your browser.

## Customising the pipelines

### Adding a REST API endpoint

Edit `pipeline/assets/sources/rest_api.py`:
1. Add a new `@dlt.resource` function for the endpoint.
2. Add it to `rest_api_source()`.

### Adding a Dataverse entity (ADLS Delta)

Edit `pipeline/assets/sources/adls_delta.py`:
1. Uncomment or duplicate the `ingest_delta_table(...)` call.
2. Set the correct `delta_path`, `target_schema`, and `target_table`.

### Adding a dbt model

1. Create a staging model in `dbt_project/models/staging/stg_<name>.sql`.
2. Create a mart model in `dbt_project/models/marts/mart_<name>.sql`.
3. Add the mart model name to `MART_TABLES` in `pipeline/assets/export/parquet_export.py`.

### Connecting Power BI

1. In Power BI Desktop or Service, choose **Get Data → Azure Blob Storage**.
2. Enter your storage account name (`AZURE_STORAGE_ACCOUNT_NAME`).
3. Navigate to the container set in `EXPORT_CONTAINER` and load the Parquet files from `EXPORT_PATH`.

## Viewing logs

```bash
# Webserver logs
journalctl -u dagster-webserver -f

# Daemon (scheduler) logs
journalctl -u dagster-daemon -f
```
