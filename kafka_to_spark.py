from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaLogReader") \
    .getOrCreate()

# Set log level to WARN to reduce Spark internal logs in the console
spark.sparkContext.setLogLevel("WARN")

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "web-logs") \
    .load()

# Select and cast the value column (log messages)
log_lines = df.selectExpr("CAST(value AS STRING) as log_line")

# Output only the log messages to console
query = log_lines.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()

