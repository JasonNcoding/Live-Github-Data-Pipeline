import dlt
from pyspark.sql import functions as F

@dlt.view(name="extract_actors")
def extract_actors():

    actor_schema = "id LONG, login STRING, url STRING"
    
    return (
        dlt.read_stream("stage")
        .withColumn("parsed_actor", F.from_json(F.col("actor"), schema=actor_schema))
        .select("parsed_actor.*", "created_at") 
    )

dlt.create_streaming_table("silver_actors")

dlt.create_auto_cdc_flow(
    target="silver_actors",
    source="extract_actors",
    keys=["id"], 
    sequence_by=F.col("created_at"),
    stored_as_scd_type=1
)