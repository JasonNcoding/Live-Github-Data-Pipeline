import dlt
from pyspark.sql import functions as F

@dlt.table(name="gold_engage_repos")
def gold_engage_repos():
    return (
        dlt.read("silver_events")
        .filter(F.col("type") == "WatchEvent") # Stars are 'WatchEvent'
        .withColumn("is_24h", F.col("created_at") >= F.date_sub(F.current_date(), 1))
        .withColumn("is_30d", F.col("created_at") >= F.date_sub(F.current_date(), 30))
        .groupBy("repo_name", "language")
        .agg(
            F.sum(F.when(F.col("is_24h"), 1).otherwise(0)).alias("star_count_24h"),
            F.sum(F.when(F.col("is_30d"), 1).otherwise(0)).alias("star_count_30d")
        )
        .withColumn("growth_percentage", 
            (F.col("star_count_24h") / F.col("star_count_30d")) * 100)
        .orderBy(F.desc("star_count_30d"))
    )