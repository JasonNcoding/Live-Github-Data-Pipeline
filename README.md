# Live-Github-Data-Pipeline

## Overview
GitHub Archive Data Lakehouse (2020–2026)
A high-scale data engineering pipeline built on Databricks Unity Catalog to ingest, process, and analyze over 1TB of GitHub event data.

## Architecture
The project follows a Medallion Architecture using Spark Structured Streaming and Auto Loader to handle massive JSON backfills efficiently.

Ingestion (Bronze): Python-based parallel downloader (ThreadPoolExecutor) fetching raw .json.gz files from GH Archive.

Storage: Databricks Unity Catalog Volumes for raw landing and Delta Lake for the managed tables.

Stream Processing: Auto Loader (cloudFiles) with availableNow triggers for cost-effective, incremental processing.

Star schema:
Event table (Fact Table)
Actor table (Dimension Table)
Repo Table (Dimension Table)


## Tech Stack
Language: Python, SQL

Engine: Apache Spark (Databricks Serverless)

Storage Format: Delta Lake (with Liquid Clustering)

Orchestration: Databricks Workflows

##  Key Optimizations
1. High-Performance Ingestion
To handle the 1TB backfill, I implemented a parallelized downloader that handles GH Archive's specific URL formatting quirks (non-padded integers for hours/months).

Optimization: Used ThreadPoolExecutor to download multiple hours simultaneously, reducing backfill time by 80%.

Folder Structure: Organized raw data into /YYYY/MM/ subdirectories to prevent directory listing bottlenecks.

2. Auto Loader & Schema Evolution
Used Spark's cloudFiles to handle the semi-structured nature of GitHub events.

Schema Inference: Enabled mergeSchema to automatically adapt the Delta table when GitHub adds new event types or fields.

Checkpointing: Implemented robust checkpointing to ensure "exactly-once" processing, allowing the pipeline to resume safely after any failure.

3. Delta Lake Performance at Scale
Processing 6 years of data (1TB+) requires advanced table management:

Liquid Clustering: Used CLUSTER BY (created_at) instead of traditional partitioning to ensure fast lookups across the entire time range.

Compaction: Enabled autoCompact and optimizeWrite to prevent the "Small File Problem" common with hourly data ingestion.

## Challenges Overcome
404 Handling: Managed the 2-hour delay in GH Archive availability by implementing retry logic and time-offset calculations.

Data Consistency: Used Delta Lake RESTORE and VACUUM features to maintain data integrity during the experimental phase of the backfill.

## How to Run
Configure your Unity Catalog Volume path. As well as S3

Run the Parallel Downloader notebook to fetch historical data.

Execute the Auto Loader stream to move data from Bronze to Managed Delta tables.