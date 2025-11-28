import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ============================================================
# HÀM LOAD DATA VÀ MODELS
# ============================================================

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
        
    df = pd.read_csv(file_path)
    return df

def save_data(df, file_path):
   
    df.to_csv(file_path, index=False)

@st.cache_resource
def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def append_to_csv(new_data_df, output_path):    
    # Kiểm tra sự tồn tại của file
    file_exists = os.path.exists(output_path)

    # Xử lý ghi file
    try:
        if file_exists:
            # Nếu file TỒN TẠI:
            # - mode='a' (append): Thêm vào cuối.
            # - header=False: KHÔNG ghi lại tên cột.
            new_data_df.to_csv(
                output_path,
                mode='a',
                index=False,
                header=False,
                encoding="utf-8-sig"
            )
            st.success(f"✅ Tin đăng thành công!")            
        else:
            # Nếu file CHƯA TỒN TẠI:
            # - mode='w' (write) hoặc 'a' đều sẽ tạo file.
            # - header=True: Ghi tên cột (header).
            new_data_df.to_csv(
                output_path,
                mode='w',
                index=False,
                header=True,
                encoding="utf-8-sig"
            )
            st.success(f"⭐ File **{output_path}** chưa tồn tại. Đã **tạo mới** và lưu **{len(new_data_df)}** dòng dữ liệu.")
            
        return True # Trả về True nếu thành công

    except Exception as e:
        st.error(f"❌ Lỗi trong quá trình lưu file: {e}")
        return False # Trả về False nếu thất bại

def append_to_csv_with_str(new_data_df, output_path, str):    
    # Kiểm tra sự tồn tại của file
    file_exists = os.path.exists(output_path)

    # Xử lý ghi file
    try:
        if file_exists:
            # Nếu file TỒN TẠI:
            # - mode='a' (append): Thêm vào cuối.
            # - header=False: KHÔNG ghi lại tên cột.
            new_data_df.to_csv(
                output_path,
                mode='a',
                index=False,
                header=False,
                encoding="utf-8-sig"
            )
            st.success(f"✅ {str}")            
        else:
            # Nếu file CHƯA TỒN TẠI:
            # - mode='w' (write) hoặc 'a' đều sẽ tạo file.
            # - header=True: Ghi tên cột (header).
            new_data_df.to_csv(
                output_path,
                mode='w',
                index=False,
                header=True,
                encoding="utf-8-sig"
            )
            st.success(f"⭐ File **{output_path}** chưa tồn tại. Đã **tạo mới** và lưu **{len(new_data_df)}** dòng dữ liệu.")
            
        return True # Trả về True nếu thành công

    except Exception as e:
        st.error(f"❌ Lỗi trong quá trình lưu file: {e}")
        return False # Trả về False nếu thất bại

# Hàm save df to csv
def save_df_to_csv(df, file_path):
    df.to_csv(file_path, index=False)