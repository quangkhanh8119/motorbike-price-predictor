import streamlit as st

from src.config import BASE_DIR
from src.utils.ui_components import UIComponents
from src.pages import gioi_thieu, du_doan_gia, phat_hien_bat_thuong
from src.pages import phan_tich_thi_truong, tim_kiem_so_sanh


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
                "🔍 Tìm kiếm & So sánh",
                "📊 Thống kê & Phân tích",
                "📝 Quản lý tin đăng"
            ]
        )

        # Menu con cho "Tìm kiếm & So sánh"
        sub_menu = None
        if selected_page == "🔍 Tìm kiếm & So sánh":
            UIComponents.divider("dotted", "#ddd", "10px")
            sub_menu = st.radio(
                "Dữ liệu tìm kiếm:",
                [
                    "🗄️ Tìm trên dữ liệu mặc định",
                    "🔥 Tìm trên dữ liệu mới nhất",
                    "➕ Tìm trên tất cả dữ liệu"
                ],
                key="submenu_tim_kiem_so_sanh"
            )
        
        # Menu con cho "Thống kê & Phân tích"
        if selected_page == "📊 Thống kê & Phân tích":
            UIComponents.divider("dotted", "#ddd", "10px")
            sub_menu = st.radio(
                "Dữ liệu thống kê:",
                [
                    "🗄️ Tin đăng mặc định",
                    "🔥 Tin đăng mới nhất",
                    "➕ Tất cả các tin đăng"
                ],
                key="submenu_thong_ke"
            )

        # Menu con cho "Quản lý tin đăng"        
        if selected_page == "📝 Quản lý tin đăng":            
            UIComponents.divider("dotted", "#ddd", "10px")
            sub_menu = st.radio(
                "Chọn chức năng:",
                [
                    "➕ Đăng tin mới",
                    "📋 Thống kê tin đăng",
                    "🗄️ Tin đã lưu"
                ],
                key="submenu_ql_tin_dang"
            )
        
        
        
        UIComponents.divider("dotted", "#ddd", "20px")
        
        # Thêm info
        with st.expander("ℹ️ Thông tin"):
            st.write("""
            👨‍🎓 ***Học vien*** 
            - Nguyễn Quang Khánh
            - Nguyễn Đức Bằng
            """)           
            
            UIComponents.divider("dotted", "#ddd", "10px")

            st.write("""
            📚 ***Data & Models***
            - Cập nhật: 25/11/2024
            - Tổng tin: 6,821
            - Độ chính xác: 92%
            """)
                
    # Kiểm tra nếu trang thay đổi
    if st.session_state.current_page != selected_page:
        # Xóa dữ liệu cũ
        keys_to_delete = ['ket_qua_du_doan', 'kiem_tra_bat_thuong', 'tim_kiem_va_so_sanh', 'ket_qua_phan_tich_thi_truong', 'ket_qua_quan_ly_tin_dang']
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
        st.sidebar.image("./assets/logo_s.jpg", width=256)
        du_doan_gia.show()
        # Nội dung dự đoán giá
        
    elif selected_page == "🚨 Phát hiện giá bất thường":
        st.sidebar.image("./assets/logo_s.jpg", width=256)
        phat_hien_bat_thuong.show()
        # Nội dung phát hiện bất thường

    elif selected_page == "🔍 Tìm kiếm & So sánh":        
        st.sidebar.image("./assets/logo_s.jpg", width=256)        
         
        if sub_menu == "🗄️ Tìm trên dữ liệu mặc định":
            st.write("### 🗄️ Tin đăng mặc định")
            tim_kiem_so_sanh.show()
        elif sub_menu == "🔥 Tìm trên dữ liệu mới nhất":
            st.write("### 🔥 Tin đăng mới nhất")
            tim_kiem_so_sanh.show()
        elif sub_menu == "➕ Tìm trên tất cả dữ liệu":
            st.write("### ➕ Tất cả các tin đăng")
            tim_kiem_so_sanh.show()
        
    elif selected_page == "📊 Thống kê & Phân tích":
        st.sidebar.image("./assets/logo_s.jpg", width=256)
        
        if sub_menu == "🗄️ Tin đăng mặc định":
            st.write("### 🗄️ Tin đăng mặc định")
            phan_tich_thi_truong.show()
        elif sub_menu == "🔥 Tin đăng mới nhất":
            st.write("### 🔥 Tin đăng mới nhất")
            phan_tich_thi_truong.show()
        elif sub_menu == "➕ Tất cả các tin đăng":
            st.write("### ➕ Tất cả các tin đăng")
            phan_tich_thi_truong.show()
        # Nội dung phân tích
        
    elif selected_page == "📝 Quản lý tin đăng":
        st.title("📝 Quản Lý Tin Đăng")
        st.sidebar.image("./assets/logo_s.jpg", width=256)
        
        if sub_menu == "➕ Đăng tin mới":
            st.write("## ➕ Đăng Tin Mới")
            with st.form("form_dang_tin"):
                col1, col2 = st.columns(2)
                with col1:
                    tieu_de = st.text_input("Tiêu đề tin")
                    gia = st.number_input("Giá xe (VNĐ)", min_value=0)
                with col2:
                    hang_xe = st.selectbox("Hãng xe", ["Toyota", "Honda", "Ford", "BMW"])
                    nam_sx = st.number_input("Năm sản xuất", min_value=2000, max_value=2025)
                
                mo_ta = st.text_area("Mô tả chi tiết")
                
                if st.form_submit_button("📤 Đăng tin"):
                    st.success("✅ Đăng tin thành công!")
        
        elif sub_menu == "📋 Tin đang hoạt động":
            st.write("## 📋 Tin Đang Hoạt Động")
            # Hiển thị danh sách tin
            tin_list = [
                {"id": 1, "tieu_de": "Toyota Camry 2020", "gia": "950 triệu", "trang_thai": "Đang bán"},
                {"id": 2, "tieu_de": "Honda Civic 2019", "gia": "750 triệu", "trang_thai": "Đang bán"},
                {"id": 3, "tieu_de": "Ford Focus 2021", "gia": "650 triệu", "trang_thai": "Đang bán"}
            ]
            
            for tin in tin_list:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{tin['tieu_de']}**")
                        st.caption(f"Giá: {tin['gia']}")
                    with col2:
                        st.write(f"🟢 {tin['trang_thai']}")
                    with col3:
                        st.button("✏️ Sửa", key=f"edit_{tin['id']}")
                        st.button("🗑️ Xóa", key=f"delete_{tin['id']}")
        
        elif sub_menu == "🗄️ Tin đã lưu":
            st.write("## 🗄️ Tin Đã Lưu")
            saved_tin = [
                {"tieu_de": "Tesla Model 3 2022", "gia": "1.5 tỷ"},
                {"tieu_de": "BMW X5 2021", "gia": "2 tỷ"}
            ]
            
            for tin in saved_tin:
                st.write(f"📌 {tin['tieu_de']} - {tin['gia']}")
        # Nội dung quản lý

# Run if module executed
if __name__=="__main__":
    main()


