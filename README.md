# GitHub Activity Pipeline
A Data Engineering pipeline built on Databricks Delta Live Tables (DLT) and Lakeflow. This pipeline ingests, cleans, and distills half a billion GitHub events into a queryable Star Schema.

## Architecture
The pipeline follows the Medallion Architecture, optimized for high-throughput streaming and automatic schema evolution.

Bronze: Raw JSON ingestion using Auto Loader (cloudFiles).

Silver (Events): Flattened event logs, filtered for bots, and optimized with Liquid Clustering.

Silver (Actors/Repos): Type-1 SCD tables managed via Lakeflow Auto CDC, ensuring unique developer and repository dimensions.

Gold: Materialized Views for Top Engagement Repositories and Top Language Used analytics.

## Performance Milestones
Ingestion Rate: ~23.4 Million rows/minute.

Total Volume: 447,635,830 rows processed in 19m 06s.

## Features
Liquid Clustering: Clustered by event_id, type, and created_at for sub-second query performance on massive datasets.

Bot Filtering: Built-in Regex filters to remove automated/bot GitHub activity.

Data Quality: DLT Expectations ensure NULL IDs or malformed events never reach the Silver layer.

Auto CDC: Uses the 2026 Lakeflow API (create_auto_cdc_flow) for efficient state management of dimension tables.

## Project Structure
Plaintext
├── 1. bronze
│   └── Hourly Data Ingestion.py      
├── 2. silver
│   ├── actors       
│   │   ├── Clean Actors Data.py      
│   ├── events       
│   │   ├── Clean Events Data.py
│   ├── repos       
│   │   ├── Clean Repos Data.py
└── 3. gold
    └── Most Engagement Repos.py
    └── Most Used Programming Language.py
## Getting Started
Add Source: Mount the bronze layer to your GitHub Archive S3 path.

Configure S3: Ensure your bucket permissions are set for Unity Catalog as well as IAM roles. 
Links: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/add-data-external-locations

Create Pipeline: Create a new DLT pipeline in Databricks Jobs and Pipeline.

Run: Select Full Refresh to perform the initial row ingestion.

## Sample Insight Query
SQL
-- Find the fastest growing languages
SELECT 
    language, 
    count(*) as total_events 
FROM workspace.silver_events 
WHERE type = 'PushEvent'
GROUP BY 1 
ORDER BY 2 DESC 
LIMIT 10;