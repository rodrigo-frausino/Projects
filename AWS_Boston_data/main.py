from pyspark.sql import SparkSession
from pyspark.sql.functions import col,unix_timestamp, when
from pyspark.sql.types import TimestampType
import argparse


# the :str is the type hint for the argument and the -> None is the  type hint for the return value.

def transform_data(database:str, table_source:str, table_target) -> None:

    spark = (SparkSession.builder.appName("Boston 311 Analysis").enableHiveSupport().getOrCreate())
  
    df = spark.read.table(f"`{database}`.`{table_source}`")
    
    df = (df.withColumn("open_dt", col("open_dt").cast(TimestampType()))
    .withColumn("closed_dt", col("closed_dt").cast(TimestampType()))
    .withColumn("target_dt", col("target_dt").cast(TimestampType()))
    )
    
    df = df.withColumn("delay_days", when
    (col("closed_dt") > col("target_dt"),
    (unix_timestamp("closed_dt")-unix_timestamp("target_dt"))/86400, ).otherwise(0),)
    
    columns_to_keep = [
        "case_enquiry_id",
        "open_dt",
        "closed_dt",
        "target_dt",
        "case_status",
        "ontime",
        "closure_reason",
        "case_title",
        "subject",
        "reason",
        "neighborhood",
        "location_street_name",
        "location_zipcode",
        "latitude",
        "longitude",
        "source",
        "delay_days",
    ]
    
    df_selected = df.select(columns_to_keep)

    df_selected.createOrReplaceTempView("boston311")

    query = """
    SELECT * FROM boston311
    WHERE case_status = 'Closed' AND delay_days > 0
    ORDER BY delay_days DESC
    """

    result_df = spark.sql(query)

    result_df.write.mode("overwrite").format("parquet").saveAsTable(f"`{database}`.`{table_target}`")

    spark.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform data from Boston 311 dataset')
    parser.add_argument('--database', type=str, help='Database name')
    parser.add_argument('--table_source', type=str, help='Source table name')
    parser.add_argument('--table_target', type=str, help='Target table name')
    args = parser.parse_args()
    transform_data(args.database, args.table_source, args.table_target)