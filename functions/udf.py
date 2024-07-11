import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType, StructType, StructField
import re
import pandas as pd

def string_to_int(text):
    if text is None:
        return None
    price = re.findall(r"\d[\d\.]*", text)
    if price:
        price = price[0].replace('.', '')
        return int(price)
    return None

def split_name_product(name_column):
    filter_pattern = r"M[1-9]|N[0-9]{4}|i[0-9]|R[0-9]|Ultra|Core"
    filter_chip_pattern = r"[(]"

    start_index = re.search(filter_pattern, name_column).start() if re.search(filter_pattern, name_column) else 0
    name = name_column[0:start_index] if start_index > 0 else name_column
    chip_code = name_column[start_index:]
    start_index_chip = re.search(filter_chip_pattern, chip_code).start() if re.search(filter_chip_pattern, chip_code) else 0
    core = chip_code[0:start_index_chip] if start_index_chip > 0 else chip_code
    code = chip_code[start_index_chip:][1:-1] if start_index_chip > 0 else None

    return name, core, code

def convert_storage(storage_str):
    if pd.isnull(storage_str):
        return None
    match = re.match(r'(RAM|SSD)\s*(\d+)\s*(GB|TB)', storage_str, re.IGNORECASE)
    if match:
        value = int(match.group(2))
        unit = match.group(3).upper()
        
        if unit == 'TB':
            value *= 1024
            
        return value
    return None

schema = StructType([
    StructField("names", StringType(), True),
    StructField("cores", StringType(), True),
    StructField("codes", StringType(), True)
])

string_to_int_udf = udf(string_to_int, IntegerType())
split_name_product_udf = udf(split_name_product, schema)
convert_storage_udf = udf(convert_storage, IntegerType())