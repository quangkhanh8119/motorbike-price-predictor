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
data_post_new = load_data("./data/results/results_post_new_pending.csv")
data_result_anomaly = load_data("./data/results/results_with_anomalies.csv")
df_result = pd.concat([data_result_anomaly, data_post_new], join='inner', ignore_index=True)
# model = load_model("./models/model_regression_best.pkl")

# khai báo path
# new_post_file = "./data/results/results_post_new_pending.csv"

# ============================================================
# HÀM MAIN SHOW & INIT
# ============================================================
def show():
    # Set page layout
    ui.set_page_layout_wide(width=1200, hide_branding=False)
    
    phan_tich_thi_truong(data_result_anomaly, data_post_new)

# ============================================================
# HÀM XỬ LÝ TÌM KIẾM & SO SÁNH
# ============================================================
def phan_tich_thi_truong(df, df_new):    
    st.markdown("## 🚨 Công cụ thống kê và phân tích")
    # st.markdown("*Chọn các thông tin đặc tính của xe cần tìm kiếm và gợi ý từ hệ thống*")

    df['trang_thai'] = 0

    # set trang_thai=1 neu anomaly_flag=1
    df.loc[df['anomaly_flag'] == 1, 'trang_thai'] = 1    

    df_result = pd.concat([df, df_new], join='inner', ignore_index=True)
    
    df_show = df_result[['thuong_hieu', 'dong_xe', 'xuat_xu', 'nam_dang_ky', 'so_km_da_di', 'gia_actual', 'gia_pred', 'trang_thai']]    
    with st.expander("Biểu đồ phân tích thị trường", expanded=True):
        col1, col2 = st.columns(2)
        with col1:         
            sl_da_duyet = (df_show['trang_thai']==0).sum()
            sl_bat_thuong = (df_show['trang_thai']==1).sum()
            sl_cho_duyet = (df_show['trang_thai']==2).sum()
            sl_tu_choi = (df_show['trang_thai']==3).sum()

            status_data = {
                'Trạng Thái': ['✅ Phê Duyệt', '⏳ Chờ Duyệt', '⚠️ Bất Thường', '❌ Từ chối'],
                'Số Lượng': [
                    int(sl_da_duyet),
                    int(sl_cho_duyet),
                    int(sl_bat_thuong),
                    int(sl_tu_choi),
                ]
            }
            status_df = pd.DataFrame(status_data)
            
            fig = px.pie(
                status_df,
                values='Số Lượng',
                names='Trạng Thái',
                title="Phân Bố Trạng Thái",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Top brands
            brands_data = {
                'Hãng': df_show['thuong_hieu'].unique(),
                'Số Tin': df_show['thuong_hieu'].value_counts().sort_values(ascending=False)
            }
            brands_df = pd.DataFrame(brands_data)
            
            fig = px.bar(
                brands_df,
                x='Số Tin',
                y='Hãng',
                orientation='h',
                title="🏍️ Hãng Xe Phổ Biến Nhất",
                color='Số Tin',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    ui.divider("dotted", "#ddd", "20px")
    # Tạo placeholder
    placeholder_tin_dang = st.empty()
    # Hiển thị nội dung ban đầu
    placeholder_tin_dang.write("### 📋 Danh sách các tin đăng")
    
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            btn_xem_tat_ca = st.button("📋 Xem tất cả tin đăng")
            if btn_xem_tat_ca:
                df_show = df_result[['thuong_hieu', 'dong_xe', 'xuat_xu', 'nam_dang_ky', 'so_km_da_di', 'gia_actual', 'gia_pred', 'trang_thai']]
                placeholder_tin_dang.write("### 📋 Danh sách các tin đăng"
                                           )
        with col2:
            btn_xem_tin_bat_thuong = st.button("⚠️ Xem tin bất thường")
            if btn_xem_tin_bat_thuong:
                list_bat_thuong = df_show[df_show['trang_thai'] == 1].index.tolist()
                df_show = df_show.iloc[list_bat_thuong].reset_index(drop=True)
                placeholder_tin_dang.write("### 📋 Danh sách các tin bất thường")
        
        with col3:
            btn_xem_tin_cho_duyet = st.button("⏳ Xem tin chờ duyệt")
            if btn_xem_tin_cho_duyet:
                list_cho_duyet = df_show[df_show['trang_thai'] == 2].index.tolist()
                df_show = df_show.iloc[list_cho_duyet].reset_index(drop=True)
                placeholder_tin_dang.write("### 📋 Danh sách các tin chờ duyệt")
            
        with col4:
            btn_xem_tin_duyet = st.button("✅ Xem tin đã duyệt")
            if btn_xem_tin_duyet:
                list_duyet = df_show[df_show['trang_thai'] == 0].index.tolist()
                df_show = df_show.iloc[list_duyet].reset_index(drop=True)
                placeholder_tin_dang.write("### 📋 Danh sách các tin được duyệt")
            
        with col5:
            btn_xem_tin_tu_choi = st.button("❌ Xem tin từ chối")
            if btn_xem_tin_tu_choi:
                list_tu_choi = df_show[df_show['trang_thai'] == 3].index.tolist()
                df_show = df_show.iloc[list_tu_choi].reset_index(drop=True)
                placeholder_tin_dang.write("### 📋 Danh sách các tin từ chối gần đây")

    ui.divider("dotted", "#ddd", "20px")
    
    st.markdown("#### Tổng số tin đăng: " + str(len(df_show)))
    df_show.columns = ['Thương Hiệu', 'Dòng Xe', 'Xuất Xứ', 'Năm Đăng Ký', 'Số Km', 'Giá Bán', 'Giá Dự Đoán', 'Trạng Thái']
    st.dataframe(df_show)   
    

