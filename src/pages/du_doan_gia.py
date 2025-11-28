import streamlit as st
import pandas as pd
import numpy as np

from src.config import * # type: ignore
from src.utils.ui_components import UIComponents # type: ignore
from src.utils.charts import bieu_do_gia_xe, price_range_chart, show_price_suggestion # type: ignore
from src.utils.data_processor import load_data, load_model, append_to_csv # type: ignore
from src.utils.price_functions import format_vnd, format_trieu_vnd, suggest_price # type: ignore

# Set page config
st.set_page_config(
    page_title="Dự Đoán Giá",
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
    
    st.markdown("## 💰 Công Cụ Dự Đoán Giá Xe Máy")
    st.markdown("*Nhập thông tin xe của bạn để nhận được đề xuất giá hợp lý từ hệ thống*")
    
    # Tab interface
    tab1, tab2 = st.tabs(["🎯 Dự Đoán Giá", "📊 Thị Trường Giá"])
    
    with tab1:
        du_doan_gia_xe(data, model)
    
    with tab2:
        phan_tich_thi_truong(data)

# ============================================================
# HÀM XỬ LÝ DỰ ĐOÁN GIÁ XE 
# ============================================================
def prepare_input(input_dict, features):
    df = pd.DataFrame([{f: input_dict.get(f, np.nan) for f in features}])

    # numeric auto convert
    numeric_cols = ['so_km_da_di','nam_dang_ky']
    for c in numeric_cols:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # categorical auto fill
    cat_cols = ['thuong_hieu','dong_xe','tinh_trang','loai_xe','dung_tich_xe', 'xuat_xu']
    for c in cat_cols:
        df[c] = df[c].fillna('unknown').astype(str)


    # Filll any all-NaN numeric → 0
    for c in df.columns:
        if df[c].dtype.kind in 'fiu' and df[c].isna().all():
            df[c] = df[c].fillna(0)
    
    return df
st
def predict_price(info, model, features=None, inverse_log=True):
    
    if features is None:
        features = [
            'thuong_hieu','dong_xe', 'nam_dang_ky','so_km_da_di',
            'tinh_trang','loai_xe','dung_tich_xe','xuat_xu'
        ]        

    df = prepare_input(info, features)

    try:
        pred = model.predict(df)[0]
    except Exception as e:
        raise RuntimeError(f"Predict failed: {e}\nInput:\n{df}")

    return float(np.expm1(pred) if inverse_log else pred)

def du_doan_gia_xe(df, model_regression_best):    
    
    st.markdown("### 📋 Thông tin xe cần dự đoán giá")

    # Khởi tạo session_state để lưu kết quả
    if 'ket_qua_du_doan' not in st.session_state:
        st.session_state.ket_qua_du_doan = None    

    with st.container(border=True):
        # Input section with columns
        col1, col2, col3 = st.columns(3)
        with col1:
            thuong_hieu = st.selectbox("⚙️ Chọn hãng xe", df['thuong_hieu'].unique(), index=1)
            
            so_km_min = int(df['so_km_da_di'].min())
            so_km_max = int(df['so_km_da_di'].max())
            so_km_da_di = st.number_input("🛣️ Số km đã đi", min_value=so_km_min, max_value=so_km_max, value=50000, step=1000)        

        with col2:
            # Filter cho dong_xe có cùng thuong hieu                        
            df_dong_xe = df[df['thuong_hieu'] == thuong_hieu]['dong_xe'].unique()
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df_dong_xe)
            dung_tich_xi_lanh = st.selectbox("🔧 Dung tích xi lanh (cc)", df['dung_tich_xe'].unique())        

        with col3:
            loai_xe = st.selectbox("🛵 Chọn loại xe", df['loai_xe'].unique())
            tinh_trang = st.selectbox("🛡️ Chọn tình trạng", df['tinh_trang'].unique())
        
        col1_ext, col2_ext = st.columns([1, 2])
        with col1_ext:
            xuat_xu = st.selectbox("🏭️ Xuất xứ", df['xuat_xu'].unique(), index=2)
        
        with col2_ext:
            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky = st.slider("📅 Năm đăng ký", nam_dk_min, nam_dk_max, 2010, label_visibility='visible')
        
        ui.divider_thin(style="dashed", color="#d6d6d9")

        col_a, col_b, col_c = st.columns(3)
        with col_b:
            # Nút Dự đoán và gợi ý giá 
            du_doan_gia_button = st.button(f"💰 **Dự đoán & Gợi ý giá**", type="primary" , width="stretch")
        
    # Xử lý khi nhấn nút dự đoán
    if du_doan_gia_button:
        # Thực hiện dự đoán giá khi nhấn nút    
        input_vehicle = {
            'thuong_hieu': thuong_hieu,
            'dong_xe': dong_xe,
            'loai_xe': loai_xe,
            'dung_tich_xe': dung_tich_xi_lanh,
            'so_km_da_di': so_km_da_di,
            'nam_dang_ky': nam_dang_ky,
            'xuat_xu': xuat_xu,
            'tinh_trang': tinh_trang
        }
        # Dự đoán giá
        try:
            gia_du_doan = predict_price(input_vehicle, model_regression_best)            
        except Exception as e:            
            st.error(f"Lỗi trong quá trình dự đoán: {e}")
            return
        
        # Giá gợi ý
        gia_goi_y = suggest_price(gia_du_doan)
        
        # Lưu kết quả với session_state
        st.session_state.ket_qua_du_doan = {
            'gia_du_doan': gia_du_doan,
            'gia_goi_y': gia_goi_y,
            'input_vehicle': input_vehicle
        }
    
    # HIỂN THỊ KẾT QUẢ NẾU CÓ (dù click button nào cũng vẫn hiển thị)
    if st.session_state.ket_qua_du_doan is not None:
        ket_qua = st.session_state.ket_qua_du_doan
        gia_du_doan = ket_qua['gia_du_doan']
        gia_goi_y = ket_qua['gia_goi_y']
        input_data = ket_qua['input_vehicle']
        
        st.write("")

        col1_kq, col2_kq = st.columns([1, 1])
        
        with col1_kq:
            st.markdown("### ⭐ Kết quả đề xuất giá")
            ui.colored_text(f"{gia_du_doan:,.0f} VND", color="#0d6efd", size="30px", bold=True)            
            
            st.write("##### **✨ Gợi ý giá**")
            st.markdown(f"- Giá bán nhanh: **{format_vnd(gia_goi_y['fast_sell'])}**")            
            st.markdown(f"- Giá bán tối đa lợi nhuận: **{format_vnd(gia_goi_y['max_profit'])}**")
            st.markdown(f"- Khoảng giá hợp lý: **{format_vnd(gia_goi_y['fair_low'])} - {format_vnd(gia_goi_y['fair_high'])}**")

        with col2_kq:            
            ui.styled_table_small(
                headers=["Đặc Trưng", "Giá Trị"],
                rows=[
                    ["Hãng xe", input_data['thuong_hieu']],
                    ["Dòng xe", input_data['dong_xe']],
                    ["Loại xe", input_data['loai_xe']],
                    ["Dung tích xi lanh", input_data['dung_tich_xe']],
                    ["Số km đã đi", input_data['so_km_da_di']],
                    ["Năm đăng ký", input_data['nam_dang_ky']],
                    ["Xuất xứ", input_data['xuat_xu']],
                ],        
                centered=True
            )
               
        st.divider()
        
        # Biểu đồ khoảng giá
        fig_price_range = price_range_chart(gia_goi_y['fast_sell'], gia_du_doan, gia_goi_y['max_profit'], gia_goi_y['fair_low'], gia_goi_y['fair_high'])        
        st.plotly_chart(fig_price_range, use_container_width=True)
        
        # Hiển thị toàn bộ phần gợi ý giá bán
        show_price_suggestion(gia_goi_y['fast_sell'], gia_du_doan, gia_goi_y['max_profit'])
      
        st.divider()
        st.markdown("### 🚀 Đăng tin rao bán xe máy")
        st.write("")
        summary = {
            "Giá bán": f'**{format_vnd(gia_du_doan)}**',
            "Hãng xe": input_data['thuong_hieu'],
            "Dòng xe": input_data['dong_xe'],
            "Loại xe": input_data['loai_xe'],
            "Số Km đã đi": input_data['so_km_da_di'],
            "Năm đăng ký": input_data['nam_dang_ky'],
            "Dung tich xi lanh": input_data['dung_tich_xe'],
            "Tình trạng": input_data['tinh_trang'],
            "Xuất xứ": input_data['xuat_xu'],
        }         

        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                dang_tin_button = st.button("📝 **Đăng Tin Bán**", use_container_width=True)                    
                    # save_new_post(summary)                    
                    # st.success("✅ Tin đăng thành công!")            
            with col2:
                if st.button("✏️ **Sửa Thông Tin**", use_container_width=True):
                    # Xóa kết quả để quay lại form
                    st.session_state.ket_qua_du_doan = None
                    st.rerun()
            
            with col3:
                xem_thi_truong_button = st.button("📊 **Xem Thị Trường**", use_container_width=True)

        if dang_tin_button:
            data = {
                "gia_actual": gia_du_doan/1_000_000,
                "gia_pred": gia_du_doan/1_000_000,
                "thuong_hieu": [input_data['thuong_hieu']],
                "dong_xe": [input_data['dong_xe']],
                "loai_xe": [input_data['loai_xe']],
                "so_km_da_di": [input_data['so_km_da_di']],
                "nam_dang_ky": [input_data['nam_dang_ky']],
                "dung_tich_xe": [input_data['dung_tich_xe']],
                "tinh_trang": [input_data['tinh_trang']],
                "xuat_xu": [input_data['xuat_xu']],
                "mo_ta_chi_tiet": "Đang cập nhật",
                "anomaly_flag": 0,                
                "trang_thai": 0 ,
                'thoi_gian': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            }
             
            df = pd.DataFrame(data)            
            append_to_csv(df, new_post_file)            
            # Load data sau khi lưu và show
            # df_new = load_data(new_post_file)
            # st.write("Dữ liệu sau khi lưu")
            # st.dataframe(df_new)

        if xem_thi_truong_button:
            st.info("Chuyển sang Tab **Thị Trường Giá** để tìm thêm thông tin giá cho các dòng xe")

        st.markdown("#### 📋 Xem trước nội dung tin đăng")

        # Additional notes        
        mo_ta_chi_tiet = st.text_area(
            "Mô tả chi tiết (ví dụ: xe chính chủ, chạy ít, màu nguyên bản, full đò chơi, ...)",
            value="Đang cập nhật",
            key="mo_ta_chi_tiet",
            placeholder="Nhập các thông tin đặc biệt về xe...",
            height=80
        )               
        # st.write(mo_ta_chi_tiet)
        st.table(pd.DataFrame(summary.items(), columns=["Thông Tin", "Giá Trị"]))

        

def phan_tich_thi_truong(df):
    st.markdown("### Phân tích thị trường")    
        
    # Filter cho phân tích thị trường
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            thuong_hieu_filter = st.selectbox("⚙️ Chọn hãng để xem thị trường", df['thuong_hieu'].unique())        

        with col2:
            # Filter cho dong_xe có cùng thuong_hieu
            df_dong_xe_filter = df[df['thuong_hieu'] == thuong_hieu_filter]['dong_xe']
            dong_xe_filter = st.selectbox("🏍️ Chọn dòng xe", df_dong_xe_filter)

        with col3:            
            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky_filter = st.slider("📅 Chọn năm đăng ký", nam_dk_min, nam_dk_max, 2010, label_visibility='visible')
        

    # Market statistics    
    st.markdown(f"### 📈 Thống kê thị trường xe máy {thuong_hieu_filter} {dong_xe_filter} ({nam_dang_ky_filter})")

    with st.container(border=True):    
        col1, col2, col3, col4 = st.columns(4)
        
        # lọc các xe có cùng thuong hieu, cùng dong_xe, cùng  nam_dang_ky
        # sau đó tính trung bình cột 'gia' trên df đã lọc này
        df_filtered = df[(df['thuong_hieu'] == thuong_hieu_filter) & (df['dong_xe'] == dong_xe_filter) & (df['nam_dang_ky'] == nam_dang_ky_filter)]
        gia_tb_thi_truong = df_filtered['gia'].mean()
        gia_thap_nhat = df_filtered['gia'].min()
        gia_cao_nhat = df_filtered['gia'].max()
        so_tin_dang_ban = len(df_filtered)
        
        with col1:            
            st.metric("Giá TB Thị Trường", format_trieu_vnd(gia_tb_thi_truong))
        
        with col2:
            st.metric("Giá Thấp Nhất", format_trieu_vnd(gia_thap_nhat)) 
        
        with col3:
            st.metric("Giá Cao Nhất", format_trieu_vnd(gia_cao_nhat))
        
        with col4:
            st.metric("Tin Đăng Bán", f"{so_tin_dang_ban} tin   ")        
        
    # Price distribution chart
    st.markdown("---")
   
    # lấy cột giá của các xe có cùng thuong hieu, cùng dong_xe, cùng nam_dang_ky
    df_thi_truong = df[(df['thuong_hieu'] == thuong_hieu_filter) & (df['dong_xe'] == dong_xe_filter) & (df['nam_dang_ky'] == nam_dang_ky_filter)][['gia', 'thuong_hieu', 'dong_xe', 'nam_dang_ky']]
    # st.write("So tin:", len(df_gia_thi_truong))
    # st.dataframe(df_gia_thi_truong[['gia','dong_xe']], use_container_width=True)
    fig_thi_truong = bieu_do_gia_xe(thuong_hieu_filter, dong_xe_filter, df_thi_truong[['gia','thuong_hieu','dong_xe']])
    # st.plotly_chart(fig_thi_truong, use_container_width=True)
            
    # Market insights
    st.markdown("---")
    st.markdown("### 💡 Thông Tin Thị Trường")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **⏱️ Thời Gian Bán Trung Bình**
        
        - Giá hợp lý: **7-14 ngày**
        - Giá thấp: **3-7 ngày**
        - Giá cao: **14-30 ngày**
        """)
    
    with col2:
        st.success(f"""
        **📊 Tính Cạnh Tranh**
        
        - Duy trì giá trong ±5% của TB
        - Số tin: 245 chiếc
        - Nhu cầu: **Cao** 📈
        """)
    
    with col3:
        st.warning(f"""
        **🚨 Cơ Hội Giá**
        
        - Giá tăng **0.5%** trong tháng qua
        - Tính thanh khoản: **Tốt**
        - Khuyến nghị: Bán sớm
        """)
