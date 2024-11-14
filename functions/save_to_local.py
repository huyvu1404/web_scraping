import os
import pandas as pd
import shutil

def save_data_to_local(path, file_name, products_details):
    """Lưu dữ liệu vào file csv

    Args:
        path (str): Đường dẫn thư mục nơi tệp sẽ được lưu.
        file_name (str): Tên tệp (bao gồm phần mở rộng, ví dụ: 'products.csv').
        products_details (DataFrame): Dữ liệu cần lưu dưới dạng DataFrame.
    """
    try:    
        product_details_df = pd.DataFrame(products_details)
        
        # Nếu file đã tồn tại, di chuyển file chứa dữ liệu cũ vào đường dẫn mới và tạo các file chứa dữ liệu mới ở đường dẫn ở đầu vào
        if os.path.exists(f'{path}/{file_name}.csv'):
            backup_folder = os.path.join(path, 'last_run')
            
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            shutil.move(f'{path}/{file_name}.csv', backup_folder)
            
        product_details_df.to_csv(f'{path}/{file_name}.csv', index=False)
    except Exception as e:
        print("Error occured:", e)