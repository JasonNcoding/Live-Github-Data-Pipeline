import dlt
from pyspark.sql import functions as F

@dlt.table(name="gold_developer_language")
def gold_developer_language():
    return (
        dlt.read("silver_events")
        .filter(F.col("type") == "PushEvent")
        .withColumn("year_month", F.date_format("created_at", "yyyy-MM"))
        .groupBy("language", "year_month")
        .agg(
            F.count("event_id").alias("total_commits"),
            F.countDistinct("actor_id").alias("unique_contributors")
        )
        .orderBy("year_month", F.desc("total_commits"))
    )