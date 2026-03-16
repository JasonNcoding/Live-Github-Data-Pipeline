import dlt
from pyspark.sql import functions as F

@dlt.table(name="gold_inactive_repos")
def gold_inactive_repos():
    # 1. Aggregate activity by year
    activity_by_year = (
        dlt.read("silver_events")
        .withColumn("year", F.year("created_at"))
        .groupBy("repo_name", "year")
        .agg(
            F.count("event_id").alias("activity_count"),
            F.max("created_at").alias("last_push_date")
        )
    )

    # 2. Join 2020 stats against 2026 stats
    activity_2020 = activity_by_year.filter(F.col("year") == 2020).alias("a20")
    activity_2026 = activity_by_year.filter(F.col("year") == 2026).alias("a26")

    return (
        activity_2020.join(activity_2026, "repo_name", "left")
        .select(
            "repo_name",
            F.col("a20.activity_count").alias("peak_activity_2020"),
            F.coalesce(F.col("a26.activity_count"), F.lit(0)).alias("current_activity_2026"),
            F.col("a26.last_push_date")
        )
        # Filter for 90% drop
        .filter(F.col("current_activity_2026") <= (F.col("peak_activity_2020") * 0.10))
    )