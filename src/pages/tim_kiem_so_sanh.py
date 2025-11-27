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
    page_title="Tìm kiếm & So sánh",
    page_icon="🔍",
    layout="wide"
)

# Khởi tạo class
ui = UIComponents()

# Load ngay khi import module
# data = load_data("./data/processed/data_motobikes_cleaned.csv")
data_result_anomaly = load_data("./data/results/results_with_anomalies.csv")
model = load_model("./models/model_regression_best.pkl")

# khai báo path
# new_post_file = "./data/results/results_post_new_pending.csv"

# ============================================================
# HÀM MAIN SHOW & INIT
# ============================================================
def show():
    # Set page layout
    ui.set_page_layout_wide(width=1200, hide_branding=False)
    
    tim_kiem_va_so_sanh(data_result_anomaly, model)

# ============================================================
# HÀM XỬ LÝ TÌM KIẾM & SO SÁNH
# ============================================================
# Hàm get thông tin từ df cho các ô nhập liệu trên giao diện
def get_info(df, thuong_hieu, dong_xe, xuat_xu, nam_dang_ky, so_km_da_di, cb_xuat_xu, cb_so_km, cb_nam_dk, khoang_gia):
        
        cols = ['thuong_hieu','dong_xe', 'xuat_xu', 'nam_dang_ky', 'so_km_da_di', 'gia_actual', 'gia_pred', 'residual', 'anomaly_score', 'anomaly_flag']
        if cb_xuat_xu:
            filter_xuat_xu = df['xuat_xu'] == xuat_xu
            df = df[filter_xuat_xu]
            
        if cb_nam_dk:            
            filter_nam_dk = df['nam_dang_ky'].between(nam_dang_ky[0], nam_dang_ky[1])            
            df = df[filter_nam_dk]
            
        if cb_so_km:
            filter_km = df['so_km_da_di'].between(so_km_da_di[0], so_km_da_di[1])
            df = df[filter_km]
                    
        # tạo df với điều kiện xe cùng thuong_hieu và cùng dong_xe
        df = df[(df['thuong_hieu'] == thuong_hieu) & (df['dong_xe'] == dong_xe)][cols].drop_duplicates().reset_index(drop=True)
        
        return df
        

def tim_kiem_va_so_sanh(df, models):
    
    # ===== HEADER =====    
    st.markdown("## 🚨 Công cụ Tìm kiếm & So sánh")        
    st.markdown("*Chọn các thông tin đặc tính của xe cần tìm kiếm và gợi ý từ hệ thống*")
        
    # ui.divider_thin(style="dashed", color="#d6d6d9")

    # Khởi tạo session_state để lưu kết quả
    if 'kiem_tra_bat_thuong' not in st.session_state:
        st.session_state.kiem_tra_bat_thuong = None        

    
    # ===== FORM INPUT - Dùng expander để gọn hơn =====
    # st.markdown("### 📋 Thông tin xe cần tìm kiếm")
    with st.expander("🔧 hông tin xe cần tìm kiếm", expanded=True):    
    # with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            thuong_hieu = st.selectbox(
                "⚙️ Chọn hãng xe",
                df['thuong_hieu'].unique(),
                help="💡 Chọn hãng xe để có kết quả chính xác hơn", index=1
            )
            
            price_min = 3
            price_max = 150
            khoang_gia = st.slider("💰 Giá (Triệu VNĐ):",
                        price_min, price_max, # Tham số 2 và 3: Giá trị Min và Max
                        (15, 35), # Tham số 4: Giá trị mặc định (Default)
                        step=1,                 # Tham số Step (Keyword argument)
                        help="Khoảng giá người bán đưa ra")
           
            so_km_min = 100 # int(df['so_km_da_di'].min())
            so_km_max = 200000# int(df['so_km_da_di'].max())
            so_km_da_di = st.slider(
                "🛣️ Số KM tối đa",
                so_km_min, so_km_max,                
                (25000,50000), step=200
            )

        with col2:
            df_dong_xe = df[df['thuong_hieu'] == thuong_hieu]['dong_xe'].unique()
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df_dong_xe)

            xuat_xu = st.selectbox("🏭️ Xuất xứ", df['xuat_xu'].unique(), index=2)

            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky = st.slider(
                "📅 Năm đăng ký",
                nam_dk_min, nam_dk_max,
                (2010, 2022)
            )
        
        ui.divider("dotted", "#ddd", "10px")

        # Checkbox với giá trị mặc định
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            cb_tin_bat_thuong = st.checkbox('🚩 Chỉ hiện tin Bất Thường', value=False)
        with c2:
            cb_xuat_xu = st.checkbox('Lọc theo Xuất xứ', value=False)
        with c3:
            cb_so_km = st.checkbox('Lọc theo số KM đã đi', value=False)
        with c4:
            cb_nam_dk = st.checkbox('Lọc theo Năm đăng ký', value=False)

    # ===== HÀM XỬ LÝ TÌM KIẾM =====    
    st.markdown("### 🎯 Kết quả tìm kiếm")
    
    df_result = get_info(df, thuong_hieu, dong_xe, xuat_xu, nam_dang_ky, so_km_da_di, cb_xuat_xu, cb_so_km, cb_nam_dk, khoang_gia)
    
    
    
    # Đánh dấu với kết quả bất thường
    df_result['chenh_lech_gia'] = (df_result['residual'] / df_result['gia_actual']) * 100

    # Đánh dấu với kết quả bất thường
    df_result['ket_qua_bt'] = df_result['anomaly_flag'].apply(lambda x: "🚩 Bất Thường" if x == 1 else "")

    if cb_tin_bat_thuong:
        df_result = df_result[df_result['anomaly_flag'] == 1]
    
    with st.expander("Xem tìm kiếm", expanded=False):
        st.dataframe(df_result, height=200)
    # ui.divider("solid", "#ddd", "10px")

    show_result(df_result)    

# ===== HÀM SHOW KẾT QUẢ =====

def show_result(df_result):    
    ui.divider("dotted", "#ddd", "5px")
    col_1, col_2, col_3, col_4, col_5 = st.columns(5)
    with col_1:
        st.markdown(f"##### Tổng số tin: **{len(df_result)}**")
    
        # Đếm số kết quả bất thường trong df_result
        so_ket_qua_bt = len(df_result[df_result['anomaly_flag'] == 1])
        st.markdown(f"🚩 Tin **Bất Thường**: **{so_ket_qua_bt}**")
   
    with col_3:
        # Menu Sắp xếp theo giá tố tập
        sort_by = st.radio("### Sắp Xếp Theo:", ["Giá từ thấp đến cao", "Giá từ cao đến thấp"])## Giá từ cao đến thấp") 

        if sort_by == "Giá từ thấp đến cao":
            df_result = df_result.sort_values('gia_actual', ascending=True)
        elif sort_by == "Giá từ cao đến thấp":
            df_result = df_result.sort_values('gia_actual', ascending=False)

    with col_5:
        st.markdown(f"""
                    - **Giá TB**: {df_result['gia_actual'].mean().round(0)*1000000:,.0f} đ
                    - **Cao Nhất**: {df_result['gia_actual'].max().round(0)*1000000:,.0f} đ
                    - **Thấp Nhất**: {df_result['gia_actual'].min().round(0)*1000000:,.0f} đ
                    """)        
    ui.divider("dotted", "#ddd", "10px")

    # In các dòng xe trong df_result
    for i in range(0, len(df_result), 2):    
        # 1. Lấy hai hàng liên tiếp
        # Hàng thứ nhất
        row1 = df_result.iloc[i] 
        
        # Hàng thứ hai (Cần kiểm tra xem chỉ mục i+1 có tồn tại không)
        # Nếu i+1 vượt quá độ dài DataFrame, gán row2 là None
        row2 = df_result.iloc[i+1] if i + 1 < len(df_result) else None
        
        # 2. Tạo hai cột song song để hiển thị
        colA, colB = st.columns(2)
        
        # --- Xử lý Hàng 1 (luôn hiển thị trong colA) ---
        with colA:
            with st.container(border=True):
                col1, col2 = st.columns([3, 2])
                
                # Khối bên trái (Thông tin xe)
                with col1:
                    title = f"{row1['thuong_hieu']} {row1['dong_xe']} ({row1['nam_dang_ky']:.0f})"
                    st.markdown(f"#### {title} {row1['ket_qua_bt']}")
                    st.markdown(f"🕑 {row1['so_km_da_di']:,.0f} km    📅 {row1['nam_dang_ky']:.0f}")
                
                # Khối bên phải (Metric giá)
                with col2:
                    price_diff_pct = row1['chenh_lech_gia']
                    
                    # Logic xác định màu và trạng thái
                    if abs(price_diff_pct) <= 15:
                        color = "green"
                        status = "✅ Hợp Lý"
                    else:
                        color = "red" if price_diff_pct > 0 else "blue"
                        status = "⚠️ Cao" if price_diff_pct > 0 else "💰 Rẻ"
                    
                    # Hiển thị Metric
                    st.metric(
                        f"Dự đoán: {row1['gia_pred']*1000000:,.0f} đ", 
                        f"{row1['gia_actual']*1000000:,.0f} đ", 
                        f"{price_diff_pct:.1f}% {status}"
                    )
        
        # --- Xử lý Hàng 2 (chỉ hiển thị trong colB nếu tồn tại) ---
        if row2 is not None:
            with colB:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 2])
                    
                    # Khối bên trái (Thông tin xe)
                    with col1:
                        title = f"{row2['thuong_hieu']} {row2['dong_xe']} ({row2['nam_dang_ky']:.0f})"
                        st.markdown(f"#### {title} {row2['ket_qua_bt']}")
                        st.markdown(f"🕑 {row2['so_km_da_di']:,.0f} km    📅 {row2['nam_dang_ky']:.0f}")
                    
                    # Khối bên phải (Metric giá)
                    with col2:
                        price_diff_pct = row2['chenh_lech_gia']
                        
                        # Logic xác định màu và trạng thái
                        if abs(price_diff_pct) <= 15:
                            color = "green"
                            status = "✅ Hợp Lý"
                        else:
                            color = "red" if price_diff_pct > 0 else "blue"
                            status = "⚠️ Cao" if price_diff_pct > 0 else "💰 Rẻ"
                        
                        # Hiển thị Metric
                        st.metric(
                            f"Dự đoán: {row2['gia_pred']*1000000:,.0f} đ", 
                            f"{row2['gia_actual']*1000000:,.0f} đ", 
                            f"{price_diff_pct:.1f}% {status}"
                        )
    """
    for index, row in df_result.iterrows():
        colA, colB = st.columns(2)
        with colA:
            with st.container(border=True):
                col1, col2 = st.columns([3, 2])
                with col1:
                    title = f"{row['thuong_hieu']} {row['dong_xe']} ({row['nam_dang_ky']:.0f})"
                    st.markdown(f"#### {title} {row['ket_qua_bt']}")
                    st.markdown(f"🕑 {row['so_km_da_di']:,.0f} km    📅 {row['nam_dang_ky']:.0f}")                    
                    # st.caption(f"📉 Tiết kiệm được đ so với thị trường")
                
                with col2:
                    # price_diff = row['gia_actual'] - row['gia_pred']
                    # price_diff_pct = (price_diff / row['gia_pred'] * 100) if row['gia_pred'] > 0 else 0
                    price_diff_pct = row['chenh_lech_gia']
                    
                    if abs(price_diff_pct) <= 15:
                        color = "green"
                        status = "✅ Hợp Lý"
                    else:
                        color = "red" if price_diff_pct > 0 else "blue"
                        status = "⚠️ Cao" if price_diff_pct > 0 else "💰 Rẻ"
                    
                    st.metric(f"Dự đoán: {row['gia_pred']*1000000:,.0f} đ", f"{row['gia_actual']*1000000:,.0f} đ", f"{price_diff_pct:.1f}% {status}")
    """ 
                
    # ui.divider("dashed", "#ddd", "6px")