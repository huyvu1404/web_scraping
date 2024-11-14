import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType, StructType, StructField
import re
import pandas as pd

def string_to_int(text):
    """Chuyển đổi giá tiền từ kiểu dữ liệu string thành int

    Args:
        text (str): Dữ liệu cần chuyển đổi

    Returns:
        int or None: Dữ liệu sau khi chuyển đổi
    """
    
    if text is None:
        return None
    
    # Tìm tất cả các con số trong chuỗi 
    price = re.findall(r"\d[\d\.]*", text)
    if price:
        
        # Xóa bỏ dấu '.' trong chuỗi số và trả về dưới dạng số nguyên
        price = price[0].replace('.', '')
        return int(price)
    
    return None


def split_name_product(name_column):
    """Trích xuất tên, core và mã code của sản phẩm từ chuỗi đầu vào.


    Args:
        name_column (str): Dữ liệu ban đầu chứa tên, core và mã code của sản phẩm dưới dạng chuỗi.

    Returns:
        tuple: Trả về một tuple chứa ba phần tử:
            - Tên sản phẩm (str)
            - Core của sản phẩm (str)
            - Mã code của sản phẩm (str hoặc None nếu không có mã code)
    """
    
    # Mẫu để tìm kiếm core trong tên sản phẩm
    filter_core_pattern = r"M[1-9]|N[0-9]{4}|i[0-9]|R[0-9]|Ultra|Core"
    
    # Mẫu để tìm kiếm mã code, tìm ký tự "(" để xác định phần bắt đầu của mã code
    filter_code_pattern = r"[(]"

    # Tìm vị trí bắt đầu của core trong tên sản phẩm (nếu có), nếu không có thì sử dụng 0
    start_index = re.search(filter_core_pattern, name_column).start() if re.search(filter_core_pattern, name_column) else 0

    # Tách tên sản phẩm từ đầu đến vị trí của core (nếu có)
    name = name_column[0:start_index] if start_index > 0 else name_column

    # Phần còn lại sau tên sản phẩm (bao gồm cả core và mã code)
    core_and_code = name_column[start_index:]

    # Tìm vị trí bắt đầu của mã code trong phần còn lại (nếu có), nếu không có thì sử dụng 0
    start_index_chip = re.search(filter_code_pattern, core_and_code).start() if re.search(filter_code_pattern, core_and_code) else 0

    # Tách core từ đầu đến vị trí bắt đầu của mã code (nếu có)
    core = core_and_code[0:start_index_chip] if start_index_chip > 0 else core_and_code

    # Nếu có mã code, tách ra từ vị trí sau dấu "(" cho đến dấu ")" (loại bỏ dấu ngoặc)
    code = core_and_code[start_index_chip:][1:-1] if start_index_chip > 0 else None

    return name, core, code


def convert_storage(storage_str):
    """Chuyển đổi chuỗi mô tả dung lượng lưu trữ thành giá trị dung lượng theo GB.


    Args:
        storage_str (str): Chuỗi mô tả dung lượng lưu trữ.

    Returns:
        int or None: Giá trị dung lượng tính bằng GB nếu chuỗi hợp lệ, hoặc None nếu chuỗi không hợp lệ hoặc bị null.
    """
    # Kiểm tra nếu giá trị là null hoặc NaN
    if pd.isnull(storage_str):
        return None
    
    # Tìm kiếm mẫu
    match = re.match(r'(RAM|SSD)\s*(\d+)\s*(GB|TB)', storage_str, re.IGNORECASE)
    
    if match:
        # Lấy giá trị dung lượng và đơn vị 
        value = int(match.group(2)) 
        unit = match.group(3).upper()  
        
        # Nếu đơn vị là TB, chuyển đổi sang GB (1 TB = 1024 GB)
        if unit == 'TB':
            value *= 1024
            
        return value
    
    # Nếu không tìm thấy mẫu hợp lệ, trả về None
    return None

# Tạo schema
schema = StructType([
    StructField("names", StringType(), True),
    StructField("cores", StringType(), True),
    StructField("codes", StringType(), True)
])

# Tạo các udf
string_to_int_udf = udf(string_to_int, IntegerType())
split_name_product_udf = udf(split_name_product, schema)
convert_storage_udf = udf(convert_storage, IntegerType())