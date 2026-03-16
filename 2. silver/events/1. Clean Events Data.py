import dlt
from pyspark.sql import functions as F

rules = {"rule1": "event_id IS NOT NULL",
         "rule2": "type IS NOT NULL",
         "rule3": "created_at IS NOT NULL",
         "rule4": "actor_id IS NOT NULL",
         "rule5": "repo_id IS NOT NULL"}

@dlt.view(name="extract_events")
def extract_events():
    return (dlt.read_stream("stage") 
        .withColumn("a", F.from_json("actor", "id LONG, login STRING")) 
        .withColumn("r", F.from_json("repo", "id LONG, name STRING")) 
        .withColumn("language", F.get_json_object("payload", "$.language")))

@dlt.table(name="silver_events",
           cluster_by=["event_id", "type", "created_at"])
@dlt.expect_all_or_drop(rules)
def silver_events():
    # Read from the view above
    return (dlt.read_stream("extract_events")
        .select(
            F.col("id").alias("event_id"),
            "type",
            "created_at",
            F.to_date("created_at").alias("created_date"),
            F.col("a.id").alias("actor_id"),
            F.col("a.login").alias("actor_login"),
            F.col("r.id").alias("repo_id"),
            F.col("r.name").alias("repo_name"),
            "language",
            "payload"
        )
        .filter(~F.col("actor_login").rlike(r"(?i).*(\[bot\]|-bot$)"))
        # Apply the bot filter login
    )