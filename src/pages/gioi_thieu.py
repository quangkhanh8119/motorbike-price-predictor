import streamlit as st

from src.utils.ui_components import UIComponents  # type: ignore

# Set page layout
st.set_page_config(
    page_title="Giới Thiệu Dự Án Môn Học",  
    layout="wide",
)

# Khởi tạo class
ui = UIComponents()

def show():
    # Set page layout    
    ui.set_page_layout(width=960, hide_branding=False)

    # Show logo
    UIComponents.show_logo_conditional('capstone_project2', width=960, centered=False)

    # st.title("🌟 GIỚI THIỆU DỰ ÁN MÔN HỌC")    
    # st.subheader("Phân tích & xây dựng mô hình hóa dữ liệu xe máy đã qua sử dụng – Chợ Tốt")
    ui.centered_title_normal("Phân tích & xây dựng hệ thống mô hình hóa dữ liệu xe máy đã qua sử dụng trên ChợTốt")

    st.markdown("---")

    # Giảng viên & Học viên
    st.markdown("""
    ### 👨‍🏫 **Giảng viên hướng dẫn**
    - **Cô Khuất Thùy Phương**

    ### 👨‍🎓 **Học viên thực hiện**
    - **Nguyễn Quang Khánh**  
    - **Nguyễn Đức Bằng**
    - Ngày báo cáo: 22/11/2025

    ---
    """)

    # Tổng quan
    st.markdown("""
    ### 🚀 Tổng Quan Dự Án
    Dự án được triển khai dựa trên bộ dữ liệu thực tế từ **Chợ Tốt**, bao gồm thông tin về hàng chục nghìn tin rao bán xe máy.  
    Nhóm đã thực hiện **4 bài toán** chính nhằm phân tích dữ liệu, xây dựng mô hình học máy và đề xuất giải pháp thực tế.
    """)

    st.markdown("---")

    # Bài toán 1
    st.markdown("""
    ### 🏷️ **Dự đoán giá xe máy - Price Prediction**    
    Xây dựng mô hình hồi quy Machine Learning để dự đoán **giá bán hợp lý** dựa trên các đặc trưng:
    - Thương hiệu, dòng xe, loại xe
    - Dung tích, số km đã đi
    - Năm đăng ký, tình trạng, xuất xứ  

    👉 *Ứng dụng*: Hỗ trợ người bán định giá đúng, giúp người mua tham khảo giá thị trường chính xác.
    """)

    # Bài toán 2
    st.markdown("""
    ### 🚨 **Phát hiện giá bất thường - Anomaly Detection**
    Sử dụng mô hình dự đoán giá + nhiều kỹ thuật outlier detection để nhận diện các tin đăng có mức giá rao bán **bình thường** hay **bất thường**
    - Rao quá rẻ bất thường
    - Rao quá đắt so với thị trường 

    👉 *Ứng dụng*: Cảnh báo tin đăng bất thường, tăng tính minh bạch & phát hiện gian lận.
    """
)
    # Bài toán 3
    st.markdown("""
    ### ⭐ **Gợi ý xe tương tự - Recommendation System**
    Gợi ý xe tương tự dựa trên đặc trưng kỹ thuật của xe & nội dung mô tả:
    - Thông tin kỹ thuật xe                
    - Khoảng cách vector đặc trưng
    - Nội dung mô tả xe
    
    👉 *Ứng dụng*: hỗ trợ người dùng nhanh chóng tìm được mẫu xe phù hợp nhu cầu.
    """)

    # Bài toán 4
    st.markdown("""
    ### 📊 **Gợi ý theo cụm - Recommendation System with Clustering**
    Sử dụng thuật toán **KMeans Clustering** để phân nhóm xe theo các đặc trưng quan trọng, từ đó gợi ý theo phân khúc xe:
    - Phân nhóm theo thương hiệu, loại xe, dung tích
    - Phân nhóm theo mức giá, năm đăng ký

    👉 *Ứng dụng*: Hiểu rõ phân khúc thị trường và cá nhân hóa trải nghiệm người dùng
    """)

    st.markdown("---")

    # Cấu truc dự án
    st.markdown("""
    ### 📂 Cấu trúc Dự Án
    """)
    st.code("""
    project/
    │
    ├── assets/
    │   ├── logo.png    
    │
    ├── data/
    │   ├── data_motobikes_cleaned.csv
    │   ├── data_motobikes_cleaned_content_wt.csv
    │   ├── result_regression_predictions.csv
    │   ├── results_with_anomalies.csv
    │   ├── vietnamese-stopwords.txt
    │
    ├── models/
    │   ├── model_regression_best.pkl
    │   ├── cosine_sim.pkl
    │   ├── tfidf_matrix.pkl
    │   ├── tfidf_vectorizer.pkl    
    │
    ├── src/
    │   ├── gioi_thieu.py
    │   ├── capstone_project1.py
    │   ├── capstone_project2.py
    │   ├── project1_control_page.py
    │   ├── project2_control_page.py
    │
    ├── ui/
    │   ├── ui_components.py
    │
    ├── home.py
    """)

    st.markdown("---")

    # Kết luận
    st.markdown("""
    ## 🎯 **Kết luận**
    Cả bốn bài toán trên tạo thành một hệ thống phân tích & gợi ý toàn diện giúp:
    - Định giá chính xác
    - Phát hiện bất thường
    - Gợi ý thông minh
    - Phân khúc thị trường hiệu quả
                
    Kết quả mang lại một bộ công cụ hỗ trợ phân tích tốt cho cả Project 1 và Project 2 trong việc đưa ra gợi ý hiệu quả trong hệ thống mua bán xe máy trực tuyến.
    """)
