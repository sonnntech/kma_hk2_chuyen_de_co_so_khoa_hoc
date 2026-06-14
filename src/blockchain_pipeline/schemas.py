"""PySpark schemas used by the source transaction dataset."""

from pyspark.sql.types import (
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

TRANSACTION_SCHEMA: StructType = StructType(
    [
        StructField("transaction_id", StringType(), nullable=False),
        StructField("customer_id", StringType(), nullable=False),
        StructField("transaction_time", TimestampType(), nullable=False),
        StructField("product", StringType(), nullable=False),
        StructField("quantity", IntegerType(), nullable=False),
        StructField("unit_price", DecimalType(18, 2), nullable=False),
        StructField("amount", DecimalType(18, 2), nullable=False),
        StructField("source_system", StringType(), nullable=False),
    ]
)
