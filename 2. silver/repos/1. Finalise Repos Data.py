import dlt
from pyspark.sql import functions as F

@dlt.view(name="extract_repos")
def extract_repos():

    repo_schema = "id LONG, name STRING, url STRING"

    return (
        dlt.read_stream("stage")
        .withColumn("parsed_repo", F.from_json(F.col("repo"), schema=repo_schema))
        .select("parsed_repo.*", "created_at") 
    )

dlt.create_streaming_table("silver_repos")

dlt.create_auto_cdc_flow(
    target="silver_repos",
    source="extract_repos",
    keys=["id"],
    sequence_by=F.col("created_at"),
    stored_as_scd_type=1
)