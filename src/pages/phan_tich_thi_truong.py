import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from src.utils.ui_components import UIComponents # type: ignore
from src.utils.charts import bieu_do_gia_xe, price_range_chart, show_price_suggestion, price_comparison_gauge, price_comparison_bar # type: ignore
from src.utils.data_processor import load_data, load_model, append_to_csv, append_to_csv_with_str # type: ignore
from src.utils.price_functions import format_vnd, format_trieu_vnd, suggest_price # type: ignore

# Set page config
st.set_page_config(
    page_title="Phân tích thị trường",
    page_icon="💰",
    layout="wide"
)

# Khởi tạo class
ui = UIComponents()

# khai báo path
new_post_file = "./data/results/results_post_new_pending.csv"

# Load ngay khi import module
data = load_data("./data/processed/data_motobikes_cleaned.csv")
model = load_model("./models/model_regression_best.pkl")

# ============================================================
# HÀM MAIN SHOW & INIT
# ============================================================
def show():
    # Set page layout
    ui.set_page_layout_wide(width=1200, hide_branding=False)
    
    phat_hien_xe_bat_thuong(data, model)

# ============================================================
# HÀM XỬ LÝ PHÁT HIỆN BẤT THƯỜNG
# ============================================================
def detect_anomaly(model, info):
    df = pd.DataFrame([info])
    pred = model.predict(df)[0]
    pred = pred*1_000_000

    residual = info['gia'] - pred

    # Z-score với sigma giả định
    sigma = 0.15 * pred
    z = residual / sigma

    is_anomaly = abs(z) > 2.5

    return {
        'gia_du_doan': pred,
        'residual': residual,
        'z_score': z,
        'is_anomaly': is_anomaly,
        'ket_luan': '🔴 Giá Bất thường' if is_anomaly else '🟡 Giá Bình thường'
    }

def phat_hien_xe_bat_thuong(df, models):
    
    # ===== HEADER =====    
    col_header1, col_header2 = st.columns([7, 1])
    with col_header1:
        st.markdown("## 🚨 Công Cụ Phát Hiện Bất Thường Giá")        
        st.markdown("*Nhập thông tin xe của bạn để kiểm tra tính hợp lý của các thông tin giá từ hệ thống*")
    with col_header2:
        st.metric(
            label="Độ chính xác",
            value="94.2%",
            help="Độ chính xác của mô hình dự đoán"
        )   
    
    # ui.divider_thin(style="dashed", color="#d6d6d9")

    # Khởi tạo session_state để lưu kết quả
    if 'kiem_tra_bat_thuong' not in st.session_state:
        st.session_state.kiem_tra_bat_thuong = None        

    
    # ===== FORM INPUT - Dùng expander để gọn hơn =====
    st.markdown("### 📋 Thông tin xe cần kiểm tra")
    with st.expander("🔧 Thông tin xe cần kiểm tra", expanded=True):    
    # with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            thuong_hieu = st.selectbox(
                "⚙️ Chọn hãng xe",
                df['thuong_hieu'].unique(),
                help="💡 Chọn hãng xe để có kết quả chính xác hơn"
            )
            
            so_km_min = int(df['so_km_da_di'].min())
            so_km_max = int(df['so_km_da_di'].max())
            so_km_da_di = st.number_input(
                "🛣️ Số km đã đi",
                min_value=so_km_min,
                max_value=so_km_max,
                value=50000,
                step=1000
            )
            
            xuat_xu = st.selectbox("🏭️ Xuất xứ", df['xuat_xu'].unique(), index=2)

        with col2:
            df_dong_xe = df[df['thuong_hieu'] == thuong_hieu]['dong_xe'].unique()
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df_dong_xe)
            dung_tich_xi_lanh = st.selectbox(
                "🔧 Dung tích xi lanh (cc)",
                df['dung_tich_xe'].unique()
            )
            gia_ban = st.number_input(
                "💰 Giá bán (VND)",
                min_value=3000000,
                max_value=999000000,
                value=20000000,
                step=1000000,
                help="Giá người bán đưa ra"
            )

        with col3:
            loai_xe = st.selectbox("🛵 Chọn loại xe", df['loai_xe'].unique())
            tinh_trang = st.selectbox("🛡️ Chọn tình trạng", df['tinh_trang'].unique())
            
            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky = st.slider(
                "📅 Năm đăng ký",
                nam_dk_min,
                nam_dk_max,
                2010
            )
        
        st.write("")