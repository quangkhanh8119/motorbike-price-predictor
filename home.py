import streamlit as st

from src.config import BASE_DIR
from src.utils.ui_components import UIComponents
from src.pages import gioi_thieu, du_doan_gia, phat_hien_bat_thuong
from src.pages import phan_tich_thi_truong, quan_ly_tin_dang


st.set_page_config(
    page_title="Dự Đoán Giá & Phát Hiện Bất Thường",    
    layout="wide"
)

# test
# st.write(BASE_DIR)

# Config layout
UIComponents.set_page_width_centered(width=960)

def main():    
    menu_sidebar()

def menu_sidebar():
    # Lưu trang hiện tại vào session_state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = None

    with st.sidebar:
        # st.image("./assets/logo.jpg", width=256)
        st.markdown("### Hệ Thống Dự Đoán Giá Xe")        
        
        selected_page = st.radio(
            "📍 Chọn chức năng:",
            [
                "ℹ️ Giới thiệu",
                "💰 Dự đoán giá xe",
                "🚨 Phát hiện giá bất thường", 
                "📊 Phân tích thị trường",
                "📝 Quản lý tin đăng"
            ]
        )
        
        st.markdown("---")
        
        # Thêm info
        with st.expander("ℹ️ Thông tin"):
            st.write("""
            - 📅 Cập nhật: 25/11/2024
            - 📊 Tổng tin: 10,234
            - 🎯 Độ chính xác: 92%
            """)
        
        with st.expander("💰 Dự đoán giá xe"):
            st.write("""
            - 📅 Cập nhật: 25/11/2024
            - 📊 Tổng tin: 7,234
            - 🎯 Độ chính xác: 90%
            """)

    # Kiểm tra nếu trang thay đổi
    if st.session_state.current_page != selected_page:
        # Xóa dữ liệu cũ
        keys_to_delete = ['ket_qua_du_doan', 'kiem_tra_bat_thuong', 'ket_qua_phan_tich_thi_truong', 'ket_qua_quan_ly_tin_dang']
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
    
    # Cập nhật trang hiện tại
    st.session_state.current_page = selected_page


    # Xử lý routing
    if selected_page == "ℹ️ Giới thiệu":        
        gioi_thieu.show()
        # st.title("🏠 Giới thiệu")
        # st.write("Chào mừng đến với hệ thống dự đoán giá xe máy!")
        # Nội dung trang chủ
        
    elif selected_page == "💰 Dự đoán giá xe":
        st.sidebar.image("./assets/logo.jpg", width=256)
        du_doan_gia.show()
        # Nội dung dự đoán giá
        
    elif selected_page == "🚨 Phát hiện giá bất thường":
        st.sidebar.image("./assets/logo.jpg", width=256)     
        phat_hien_bat_thuong.show()
        # Nội dung phát hiện bất thường
        
    elif selected_page == "📊 Phân tích thị trường":
        st.title("📊 Phân Tích Thị Trường")
        phan_tich_thi_truong.show()
        # Nội dung phân tích
        
    elif selected_page == "📝 Quản lý tin đăng":
        st.title("📝 Quản Lý Tin Đăng")
        quan_ly_tin_dang.show()
        # Nội dung quản lý

# Run if module executed
if __name__=="__main__":
    main()


