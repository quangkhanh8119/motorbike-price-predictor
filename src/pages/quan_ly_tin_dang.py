import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from src.utils.ui_components import UIComponents # type: ignore
from src.utils.charts import bieu_do_gia_xe, price_range_chart, show_price_suggestion, price_comparison_gauge, price_comparison_bar # type: ignore
from src.utils.data_processor import load_data, load_model, append_to_csv, append_to_csv_with_str, save_data # type: ignore
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
# df_result = pd.concat([data_result_anomaly, data_post_new], join='inner', ignore_index=True)
# model = load_model("./models/model_regression_best.pkl")

# khai báo path
# new_post_file = "./data/results/results_post_new_pending.csv"

# ============================================================
# HÀM MAIN SHOW & INIT
# ============================================================
def show(type=0):
    # Set page layout
    ui.set_page_layout_wide(width=1200, hide_branding=False)
    
    if type == 0:
        quan_ly_tin_dang(data_result_anomaly, type)
    else:
        quan_ly_tin_dang(data_post_new, type)

# ============================================================
# HÀM XỬ LÝ TÌM KIẾM & SO SÁNH
# ============================================================
def quan_ly_tin_dang(df_results, type=0):
    st.markdown("## 🚨 Quản lý và Phê duyệt tin đăng")
    # st.markdown("*Chọn các thông tin đặc tính của xe cần kiểm tra tin đăng và gợi ý từ hệ thống*")

    if type == 0:
        # set trang_thai=1 neu anomaly_flag=1
        df_results.loc[df_results['anomaly_flag'] == 1, 'trang_thai'] = 1    
    
    total = len(df_results)
    anomalies = df_results[df_results["anomaly_flag"] == 1]

    col1, col2 = st.columns(2)
    col1.metric("Tổng tin", total)
    col2.metric("Tổng tin bất thường", len(anomalies))

    ui.divider("solid", "#ddd", "20px")
        
    with st.expander("🔧 *Chọn thương hiệu xe và mức độ chênh lệch giá*", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            ds_thuong_hieu = df_results["thuong_hieu"].dropna().unique().tolist() if "thuong_hieu" in df_results.columns else []
            chon_cac_thuong_hieu = st.multiselect("Thương hiệu", options=ds_thuong_hieu)
        with col2:
            # score_min = st.slider("Mức độ chênh lệch giá (%)", 0, 100, 10)
            loai_anomaly = st.multiselect("Loại bất thường", options=["Rẻ bất thường","Đắt bất thường","Khác"], default=None)
    
    # ========================================
    # HÀM LÝ TÌM KIẾM
    # ========================================
    if "type" not in df_results.columns:
        def _type(r):
            try:
                if r.get("residual",0) < 0: return "Rẻ bất thường"
                if r.get("residual",0) > 0: return "Đắt bất thường"
            except: pass
            return "Khác"
        df_results["type"] = df_results.apply(_type, axis=1)
    
    # filter data
    df_filtered = df_results.copy()
    if chon_cac_thuong_hieu:
        df_filtered = df_filtered[df_filtered["thuong_hieu"].isin(chon_cac_thuong_hieu)]
    # df_filtered = df_filtered[df_filtered["anomaly_score"] >= score_min]
    if loai_anomaly:
        df_filtered = df_filtered[df_filtered["type"].isin(loai_anomaly)]

    # Đếm xe bất thường hoặc tinh_trang != 0
    # tong_so_tin = df_filtered["trang_thai"] = df_filtered.apply(lambda x: 1 if x["anomaly_flag"] == 1 or x["tinh_trang"] != 0 else 0, axis=1)
    # st.write(f"Tin tìm thấy: **{tong_so_tin.sum()}**")

    ui.divider("solid", "#ddd", "20px")

    # ========================================
    # HÀM LIỆU KÊT DANH SÁCH XE BẤT THƯỜNG
    # ========================================
    # Đánh dấu với kết quả bất thường
    df_filtered['ket_qua_bt'] = df_filtered['anomaly_flag'].apply(lambda x: "🚩 Bất Thường" if x == 1 else "")

    # Tính chênh lệch giá
    df_filtered['chenh_lech_gia'] = (df_filtered['residual'] / df_filtered['gia_actual']) * 100

    # Đếm số lượng xe bất thường anomaly_flag=1 hoặc xe có tinh_trang != 0
    tong_so_tin = (df_filtered["anomaly_flag"] == 1).sum()

    # st.write(f"Tin tìm thấy: **{tong_so_tin.sum()}** tin bất thường")

    with st.expander(f"📋 Danh sách {tong_so_tin} tin bất thường", expanded=False):
        st.dataframe(df_filtered)

    for index, row in df_filtered.iterrows():
        # st.write(f"**{index+1}**. {row['thuong_hieu']} {row['dong_xe']} ({row['nam_dang_ky']:.0f})")
        # Nếu xe bất thường anomaly_flag=1 hoặc xe có tinh_trang != 0
        if row['anomaly_flag'] == 1:
            with st.container(border=True):                
                col1, col2, col3  = st.columns([5, 2, 1])
                
                # Khối bên trái (Thông tin xe)
                with col1:
                    title = f"{row['thuong_hieu']} {row['dong_xe']} ({row['nam_dang_ky']:.0f})"
                
                    st.markdown(f"#### {title}")
                    st.markdown(f"🕑 {row['so_km_da_di']:,.0f} km    📅 {row['nam_dang_ky']:.0f}")

                    # Tính chênh lệch giá
                    price_diff_pct = row['chenh_lech_gia']
                    
                with col3:
                    if abs(price_diff_pct) <= 15:
                        st.warning(f"🟡 VỪA", width=98)
                    else:
                        if price_diff_pct > 0:
                            st.error(f"🔴 CAO", width=98)
                        else:
                            st.info(f"🟢 THẤP", width=98)  
                
                # Khối bên phải (Metric giá)
                with col2:

                    # Logic xác định màu và trạng thái
                    if abs(price_diff_pct) <= 15:
                        color = "green"
                        status = "✅ Hợp Lý"                    
                    else:
                        if price_diff_pct > 0:
                            color = "red"
                            status = "⚠️ Cao"                            
                        else:
                            color = "blue"
                            status = "💰 Rẻ"
                    
                    # Hiển thị Metric
                    st.metric(
                        f"Dự đoán: {row['gia_pred']*1000000:,.0f} đ", 
                        f"{row['gia_actual']*1000000:,.0f} đ", 
                        f"{price_diff_pct:.1f}% {status}"
                    )
                ui.divider("dotted", "#ddd", "5px")
                col1, col2, col3, = st.columns(3)
                with col1:
                    btn_duyet_tin = st.button("✅ Phê Duyệt", key=f"btn_duyet_tin_{index}", use_container_width=True)
                with col2:
                    btn_sua_tin = st.button("🔄 Yêu cầu Sửa", key=f"btn_sua_tin_{index}", use_container_width=True)
                with col3:
                    btn_tu_choi = st.button("❌ Từ chối", key=f"btn_tu_choi_{index}", use_container_width=True)  
                                
                output_path = "./data/results/data_motobikes_cleaned.csv"
                if btn_duyet_tin:
                    df_filtered.loc[index, "anomaly_flag"] = 0
                    df_filtered.loc[index, "trang_thai"] = 0                    
                    st.success(" Tin đã được duyệt đăng", icon="✅")                    
                    save_data(df_filtered, output_path)                    
                elif btn_sua_tin:                    
                    df_filtered.loc[index, "trang_thai"] = 4
                    st.success(" Yêu cầu sữa lại thông tin đăng, để được duyệt", icon="🔄")
                    save_data(df_filtered, output_path)
                elif btn_tu_choi:
                    df_filtered.loc[index, "trang_thai"] = 3
                    # Xóa tin có index
                    df_filtered = df_filtered.drop(index)
                    st.error(" Tin đã bị từ chối, Bài đăng sẽ bị xóa", icon="❌")
                    save_data(df_filtered, output_path)

    
                
                
                    

