import dlt

@dlt.table(name="stage")
def stage():
    return dlt.read_stream("bronze")