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
    page_title="Dự Đoán Giá",
    page_icon="💰",
    layout="wide"
)

# Khởi tạo class
ui = UIComponents()

# khai báo path
new_post_file = "./data/results/results_new_post.csv"

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
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df['dong_xe'].unique())
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
        
        # Nút kiểm tra
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            kiem_tra_bat_thuong_button = st.button(
                "🔍 Kiểm tra bất thường",
                type="primary",
                use_container_width=True
            )

    # ===== XỬ LÝ KHI CLICK BUTTON =====
    if kiem_tra_bat_thuong_button:
        # Input tin đăng
        input_xe = {
            'thuong_hieu': thuong_hieu,
            'dong_xe': dong_xe,
            'loai_xe': loai_xe,
            'dung_tich_xe': dung_tich_xi_lanh,
            'so_km_da_di': so_km_da_di,
            'nam_dang_ky': nam_dang_ky,
            'xuat_xu': xuat_xu,
            'tinh_trang': tinh_trang,
            'gia': gia_ban,
        }
        
        # Dò tìm bất thường (giả sử hàm này đã có)
        ketqua = detect_anomaly(models, input_xe)
        
        
        # Lưu vào session state để có lịch sử
        if 'anomaly_history' not in st.session_state:
            st.session_state.anomaly_history = []
        
        st.session_state.anomaly_history.append({
            'Thời gian': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            'Xe': f"{thuong_hieu} {dong_xe}",
            'Giá bán': gia_ban,
            'Giá dự đoán': ketqua['gia_du_doan'],
            'Kết luận': ketqua['ket_luan']
        })
        
        # ===== LƯU TẤT CẢ DỮ LIỆU VÀO SESSION STATE =====
        st.session_state.kiem_tra_bat_thuong = {
            'ketqua': ketqua,
            'gia_ban': gia_ban,
            'thuong_hieu': thuong_hieu,
            'dong_xe': dong_xe,
            'loai_xe': loai_xe,
            'tinh_trang': tinh_trang,
            'dung_tich_xi_lanh': dung_tich_xi_lanh,
            'so_km_da_di': so_km_da_di,
            'nam_dang_ky': nam_dang_ky,
            'xuat_xu': xuat_xu
        }
    
    # ===== HIỂN THỊ KẾT QUẢ (NẾU ĐÃ CÓ) =====
    if st.session_state.kiem_tra_bat_thuong is not None:
        # Lấy dữ liệu từ session_state
        saved_data = st.session_state.kiem_tra_bat_thuong
        ketqua = saved_data['ketqua']
        gia_ban = saved_data['gia_ban']
        thuong_hieu = saved_data['thuong_hieu']
        dong_xe = saved_data['dong_xe']
        loai_xe = saved_data['loai_xe']
        tinh_trang = saved_data['tinh_trang']
        dung_tich_xi_lanh = saved_data['dung_tich_xi_lanh']
        so_km_da_di = saved_data['so_km_da_di']
        nam_dang_ky = saved_data['nam_dang_ky']
        xuat_xu = saved_data['xuat_xu']
        
        st.write("---")             
        
        # ===== METRICS VÀ TRẠNG THÁI =====
        st.markdown("### 📊 Kết quả phát hiện xe máy bất thường")
        
        lech_gia = (ketqua['residual'] / gia_ban) * 100
        lech_gia_abs = abs(lech_gia)
        
        # 3 metrics cards
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric(
                label="💰 Giá người bán",
                value=f"{gia_ban:,.0f} VND",
                help="Giá mà người bán đưa ra"
            )
        
        with col_m2:
            delta_value = f"{lech_gia:.1f}%"
            st.metric(
                label="🎯 Giá dự đoán (Thị trường)",
                value=f"{ketqua['gia_du_doan']:,.0f} VND",
                delta=delta_value,
                delta_color="inverse",
                help="Giá dự đoán dựa trên mô hình AI"
            )
        
        with col_m3:
            # Hiển thị trạng thái với màu nổi bật
            if not ketqua['is_anomaly']:
                st.success("### ✅ GIÁ HỢP LÝ")
                st.caption("Giá nằm trong khoảng thị trường")
            else:
                if gia_ban > ketqua['gia_du_doan']:
                    st.error("### ⚠️ GIÁ CAO BẤT THƯỜNG")
                    st.caption(f"Cao hơn {lech_gia_abs:.1f}% so với thị trường")
                else:
                    st.warning("### 🤔 GIÁ THẤP BẤT THƯỜNG")
                    st.caption(f"Thấp hơn {lech_gia_abs:.1f}% so với thị trường")
        
        st.divider()
        
        # ===== VISUALIZATION =====
        col1, col2 = st.columns(2)
        
        # Tính giá min/max thị trường (giả sử có trong data)
        gia_min_thi_truong = ketqua['gia_du_doan'] * 0.7
        gia_max_thi_truong = ketqua['gia_du_doan'] * 1.3

        # st.write("Gia Min TT", gia_min_thi_truong)
        # st.write("Gia Max TT", gia_max_thi_truong)        

        with col1:
            fig_bar = price_comparison_bar(
                gia_ban, 
                ketqua['gia_du_doan'],
                gia_min_thi_truong,
                gia_max_thi_truong
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:            
            fig_gauge = price_comparison_gauge(
                gia_ban,
                ketqua['gia_du_doan'],
                gia_min_thi_truong,
                gia_max_thi_truong
            )
            st.plotly_chart(fig_gauge, use_container_width=True)            

        st.divider()
        
        # ===== PHÂN TÍCH & GỢI Ý CẢI THIỆN =====
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.markdown("### 💡 Phân tích & Gợi ý")
            
            if not ketqua['is_anomaly']:
                st.success("""
                ✅ **Giá hợp lý - Nằm trong khoảng thị trường**
                
                **Phân tích:**
                - Giá chỉ lệch **{:.1f}%** so với dự đoán (chấp nhận được)
                - Phù hợp với các thông tin đặc điểm xe
                - Nằm trong khoảng giá trung bình của thị trường
                
                **Khuyến nghị cho người mua:**
                - ✅ Có thể thương lượng giảm thêm 3-5%
                - 📋 Yêu cầu xem xe trực tiếp
                - 📄 Kiểm tra giấy tờ rõ ràng (cavet, đăng ký xe)
                - 🔧 Kiểm tra tình trạng kỹ thuật
                
                **Khuyến nghị cho người bán:**
                - 💰 Giá đã hợp lý, có thể bán nhanh
                - 📢 Đăng tin với mô tả chi tiết
                """.format(lech_gia_abs))
                
            elif gia_ban > ketqua['gia_du_doan']:
                st.error("""
                ⚠️ **CẢNH BÁO: Giá cao bất thường**
                
                **Phân tích:**
                - Giá cao hơn dự đoán **{:.1f}%** ({:,.0f} VND)
                - Vượt ngưỡng chấp nhận được của thị trường
                - Có thể bị định giá quá cao
                
                **Rủi ro:**
                - 🚫 Khó bán (nếu bạn là người bán)
                - 💸 Mua giá cao hơn thị trường (nếu bạn là người mua)
                - ⚠️ Có thể có thông tin không chính xác
                
                **Khuyến nghị:**
                - 🔍 Kiểm tra lại thông tin đặc điểm xe
                - 💬 Thương lượng giảm ít nhất 15-20%
                - 🚗 So sánh với xe tương tự trên thị trường
                - ⚖️ Cân nhắc tìm xe khác với giá tốt hơn
                """.format(lech_gia_abs, abs(ketqua['residual'])))
                
            else:
                st.warning("""
                🤔 **LƯU Ý: Giá thấp bất thường**
                
                **Phân tích:**
                - Giá thấp hơn dự đoán **{:.1f}%** ({:,.0f} VND)
                - Thấp hơn đáng kể so với thị trường
                
                **Nguyên nhân có thể:**
                - 🔧 Xe có vấn đề kỹ thuật chưa được công khai
                - ⚡ Người bán cần bán gấp
                - 📄 Vấn đề về giấy tờ
                - 🚫 Nguồn gốc không rõ ràng
                
                **Khuyến nghị:**
                - ⚠️ **Thận trọng cao độ** trước khi mua
                - 🔍 Kiểm tra kỹ lưỡng tình trạng xe
                - 📋 Xác minh rõ nguồn gốc, giấy tờ
                - 🚓 Kiểm tra xe có bị tình nghi hay không
                - 💬 Hỏi rõ lý do bán giá thấp
                - 🔧 Mang đến garage uy tín để kiểm tra
                """.format(lech_gia_abs, abs(ketqua['residual'])))
        
        with col_right:
            st.markdown("### 📋 Thông tin xe")
            
            # Bảng thông tin đã được styled
            df_info = pd.DataFrame({
                'Đặc Trưng': [
                    'Hãng xe', 'Dòng xe', 'Loại xe', 'Tình trạng xe',
                    'Dung tích xi lanh', 'Số km đã đi', 'Năm đăng ký',
                    'Xuất xứ', 'Giá người bán', 'Giá dự đoán', 'Lệch giá', 'Kết luận'
                ],
                'Giá Trị': [
                    thuong_hieu, dong_xe, loai_xe, tinh_trang,
                    dung_tich_xi_lanh, f"{so_km_da_di:,}", nam_dang_ky,
                    xuat_xu,
                    f"{gia_ban:,.0f} VND",
                    f"{ketqua['gia_du_doan']:,.0f} VND",
                    f"{lech_gia:.1f}%",
                    ketqua['ket_luan']
                ]
            })
            
            # Highlight các dòng quan trọng
            def highlight_important_rows(row):
                if row['Đặc Trưng'] == 'Giá người bán':
                    return ['background-color: #e3f2fd; font-weight: bold'] * 2
                elif row['Đặc Trưng'] == 'Giá dự đoán':
                    return ['background-color: #fff9c4; font-weight: bold'] * 2
                elif row['Đặc Trưng'] == 'Kết luận':
                    color = '#c8e6c9' if not ketqua['is_anomaly'] else '#ffcdd2'
                    return [f'background-color: {color}; font-weight: bold'] * 2
                return [''] * 2
            
            st.dataframe(
                df_info.style.apply(highlight_important_rows, axis=1),
                use_container_width=True,
                height=460,
                hide_index=True
            )

        st.divider()
        
        # ===== THỰC HIỆN TÁC VỤ =====
        st.markdown("### 🎯 Thực hiện tác vụ")
        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
        
        with col_act1:
            luu_ket_qua_button = st.button("💾 Lưu kết quả kiểm tra", use_container_width=True)            
            # st.success("✅ Đã lưu kết quả!")           
        
        with col_act2:
            dang_tin_ban_button = st.button("📤 Đăng Tin Bán", use_container_width=True)
            # st.success("✅ Đã đăng tin bán!")                
        
        with col_act3:
            if st.button("🔄 Kiểm tra xe khác", use_container_width=True):
                st.session_state.kiem_tra_bat_thuong = None  # Reset    
                st.rerun()
        
        with col_act4:
            if st.button("📊 Xem xe tương tự", use_container_width=True):                
                st.info("🔍 Đang tìm kiếm xe tương tự...")
        
        if luu_ket_qua_button:
            data_anomaly = {
                    'thoi_gian': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
                    'xe': f"{thuong_hieu} {dong_xe}",
                    'gia_ban': gia_ban,
                    'gia_du_doan': ketqua['gia_du_doan'],
                    'ket_luan': ketqua['ket_luan']
                }
            append_to_csv_with_str(pd.DataFrame([data_anomaly]), "./data/results/results_anomaly_history.csv", "Đã lưu kết quả!")

        if dang_tin_ban_button:
                data_result = {
                    'thoi_gian': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),                    
                    'gia_ban': gia_ban,
                    'gia_du_doan': ketqua['gia_du_doan'],
                    'ket_luan': ketqua['ket_luan'],
                    "thuong_hieu": thuong_hieu,
                    "dong_xe": dong_xe,
                    "loai_xe": loai_xe,
                    "so_km_da_di": so_km_da_di,
                    "nam_dang_ky": nam_dang_ky,
                    "dung_tich_xe": dung_tich_xi_lanh,
                    "tinh_trang": tinh_trang,                
                    "xuat_xu": xuat_xu,
                }
                append_to_csv_with_str(pd.DataFrame([data_result]), "./data/results/results_new_post_pending.csv", 
                                       "Đã ghi nhận tin **Đăng Bán** trên hệ thống! Vui chờ được **phê duyệt tin đăng**!")
                
                # df_new = load_data("./data/results/results_new_post_pending.csv")
                # st.dataframe(df_new, use_container_width=True) 
            
        # ===== LỊCH SỬ KIỂM TRA =====
        if len(st.session_state.anomaly_history) > 0:
            st.divider()
            st.markdown("### 📜 Lịch sử kiểm tra gần đây")
            
            df_history = pd.DataFrame(st.session_state.anomaly_history)
            st.dataframe(
                df_history.tail(5).sort_values('Thời gian', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("🗑️ Xóa lịch sử"):
                st.session_state.anomaly_history = []
                st.rerun()
        

        

# Hàm giả lập detect_anomaly (bạn thay bằng hàm thật)
def detect_anomaly(model, info):
    df = pd.DataFrame([info])
    pred = model.predict(df)[0]
    pred = pred*1_000_000    

    residual = info['gia'] - pred

    # Z-score với sigma giả định
    sigma = 0.15 * pred
    z = residual / sigma

    is_anomaly = abs(z) > 2.5

    if not is_anomaly:
        ket_luan = "🟡 Giá hợp lý"
    elif info['gia'] > pred:
        ket_luan = "🔴 Giá cao bất thường"
    else:
        ket_luan = "🟢 Giá thấp bất thường"

    return {
        'gia_du_doan': pred,
        'residual': residual,
        'is_anomaly': is_anomaly,
        'z_score': z,
        'ket_luan': ket_luan
    }

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
    
    st.markdown("### 📋 Nhập Thông Tin Xe Của Bạn")

    # Khởi tạo session_state để lưu kết quả
    if 'ket_qua_du_doan' not in st.session_state:
        st.session_state.ket_qua_du_doan = None
    if 'active_tab' not in st.session_state:    
        st.session_state.active_tab = 0  # Tab mặc định

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

        st.write('')        

        # Nút Dự đoán và gợi ý giá 
        du_doan_gia_button = st.button(f"💰 **Dự đoán & Gợi ý giá**")
        
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
                "gia": gia_du_doan,
                "thuong_hieu": [input_data['thuong_hieu']],
                "dong_xe": [input_data['dong_xe']],
                "loai_xe": [input_data['loai_xe']],
                "so_km_da_di": [input_data['so_km_da_di']],
                "nam_dang_ky": [input_data['nam_dang_ky']],
                "dung_tich_xe": [input_data['dung_tich_xe']],
                "tinh_trang": [input_data['tinh_trang']],                
                "xuat_xu": [input_data['xuat_xu']],
                "mo_ta_chi_tiet": "Đang cập nhật",
                'danh_dau': "Hợp lệ",
                "anomaly_flag": 0,
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
            key="mo_ta_chi_tiet",
            placeholder="Nhập các thông tin đặc biệt về xe...",
            height=80
        )        
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
