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
    """)

    # ============================================================
    # INTRO
    # ============================================================
    
    st.markdown("""
    ### 🚀 Tổng Quan Dự Án
    Dự án được triển khai dựa trên bộ dữ liệu thực tế từ **Chợ Tốt**, bao gồm thông tin về hàng chục nghìn tin rao bán xe máy.  
    Nhóm đã thực hiện **2 bài toán** chính nhằm phân tích dữ liệu, xây dựng mô hình học máy và đề xuất giải pháp thực tế.
    """)

    st.markdown("---")

    # ============================================================
    # REGRESSION MODEL
    # ============================================================
    st.markdown("""
    ### 🏷️ **Dự đoán giá xe máy - Price Prediction**    
    Xây dựng mô hình hồi quy Machine Learning để dự đoán **giá bán hợp lý** dựa trên các đặc trưng:
    - Thương hiệu, dòng xe, loại xe
    - Dung tích, số km đã đi
    - Năm đăng ký, tình trạng, xuất xứ

    👉 *Ứng dụng*: Hỗ trợ người bán định giá đúng, giúp người mua tham khảo giá thị trường chính xác.
                
    #### 💡 **Mô hình tốt nhất sử dụng cho bài toán**:
    - LightGBM Regressor hoặc XGBoost Regressor
    - Target dùng log1p(gia) → ổn định phân phối
    - Sai số MAPE: ~8–12%, R² cao                   
    """)        
    st.markdown("#### ➗ Hàm dự đoán giá (Price Prediction)")
    st.code("""
    def predict_price(info, model_path, features=None, inverse_log=True):
        if not os.path.exists(model_path):
            raise FileNotFoundError(model_path)

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        if features is None:
            try:
                features = model.named_steps["preprocessor"].feature_names_in_.tolist()
            except:
                features = [
                    'thuong_hieu','dong_xe','nam_dang_ky','so_km_da_di',
                    'tinh_trang','loai_xe','dung_tich_xe','xuat_xu'
                ]

        df = prepare_input(info, features)

        try:
            pred = model.predict(df)[0]
        except Exception as e:
            raise RuntimeError(f"[Predict Error] {e}\\nDF:\\n{df}")

        return float(np.expm1(pred) if inverse_log else pred)

    """, language="python")
    
    st.markdown("#### 📝 Ví dụ dự đoán")
    st.code("""
    input_vehicle = {
        'thuong_hieu': 'Honda',
        'dong_xe': 'Air Blade',
        'loai_xe': 'Xe tay ga',
        'dung_tich_xe': '100 - 175 cc',
        'so_km_da_di': 25000,
        'nam_dang_ky': 2019,
        'xuat_xu': 'Việt Nam'
    }

    price = predict_price(input_vehicle, "./Data/model_regression_best.pkl")
    print(f"Giá dự đoán: {price:,.0f} VND")
    """, language="python")

    st.markdown("#### 💾 Lưu kết quả dự đoán → `result_regression_predictions.csv`")
    st.code("""
    df_save = pd.DataFrame([input_vehicle])
    df_save['gia_du_doan'] = price
    df_save.to_csv("regression_predictions.csv", index=False)
    """, language="python")

    st.markdown("---")

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================
    st.markdown("""
    ### 🚨 **Phát hiện giá bất thường - Anomaly Detection**
    Sử dụng mô hình dự đoán giá + nhiều kỹ thuật outlier detection để nhận diện các tin đăng có mức giá rao bán **bình thường** hay **bất thường**
    - Rao quá rẻ bất thường
    - Rao quá đắt so với thị trường 

    👉 *Ứng dụng*: Cảnh báo tin đăng bất thường, tăng tính minh bạch & phát hiện gian lận.
    #### 💡 **Mô hình tốt nhất sử dụng cho bài toán**:
    - **Isolation Forest**
    - hoặc **AutoEncoder Tree-Based**
    """)

    st.markdown("#### ➗ Hàm kiểm tra giá bất thường")
    st.code("""
    def detect_price_anomaly(info, model_path, threshold=0.5):
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        df = prepare_input(info, model.feature_names_in_)

        score = -model.decision_function(df)[0]
        label = "ANOMALY" if score > threshold else "NORMAL"

        return score, label
    """, language="python")

    st.markdown("#### 📝 Ví dụ chạy anomaly detection")
    st.code("""
    input_vehicle = {
        'thuong_hieu': 'Honda',
        'dong_xe': 'Vision',
        'loai_xe': 'Xe tay ga',
        'dung_tich_xe': '50 - 100 cc',
        'so_km_da_di': 15000,
        'gia': 55_000_000
    }

    score, label = detect_price_anomaly(input_vehicle, "./Data/model_anomaly_best.pkl")
    print("Kết luận:", label)
    """, language="python")

    st.markdown("#### 💾 Lưu kết quả tin phát hiện bất thường → `result_anomaly_detection.csv`")
    st.code("""
    df_save = pd.DataFrame([input_vehicle])
    df_save['gia_du_doan'] = price
    df_save.to_csv("regression_predictions.csv", index=False)
    """, language="python")

    st.markdown("---")

    # ============================================================
    # MODEL EVALUATION
    # ============================================================
    st.markdown("### 🏅 Đánh giá mô hình")
    st.markdown("""
    ### **Regression**
    - RMSE  
    - MAE  
    - MAPE  
    - R²  

    ### **Anomaly Detection**
    - Precision / Recall anomaly  
    - ROC-AUC  
    - Biểu đồ phân phối anomaly score  
    """)

    st.write("---")

    # ============================================================
    # PROJECT STRUCTURE
    # ============================================================
    st.markdown("""
    ### 📂 Cấu trúc Dự Án
    """)
    st.code("""
    project
    │
    ├── assets
    │   ├── logo.png
    │
    ├── data
    │   ├── raw
    │       ├── data_motobikes.xlsx
    │   ├── processed
    │       ├── data_motobikes_cleaned.csv
    │       ├── vietnamese-stopwords.txt
    │   ├── results
    │       ├── result_regression_predictions.csv
    │       ├── results_with_anomalies.csv            
    │    
    ├── models
    │   ├── model_regression_best.pkl
    │   ├── cosine_similarity.pkl
    │
    ├── src
    │   ├── pages
    │       ├── gioi_thieu.py
    │       ├── du_doan_gia.py
    │       ├── phat_hien_bat_thuong.py
    │       ├── phan_tich_thi_truong.py
    │       ├── quan_ly_tin_dang.py
    │   ├── utils
    │       ├── ui_components.py
    │       ├── charts.py
    │       ├── data_processor.py
    │       ├── price_functions.py    
    │
    ├── home.py
    """)

    st.markdown("---")

    # ============================================================
    # STREAMLIT UI
    # ============================================================
    st.markdown("### ✨ Giao diện Streamlit")
    st.markdown("""
    Ứng dụng Streamlit bao gồm:
    - Giới thiệu dự án
    - Form cho người dùng (User):
        - Form Dự đoán giá xe → Sự đoán và gợi ý giá bán
        - Form Thị Trường Giá → Xem giá thị trường theo thông tin loại xe
        - Form Phát hiện bất thường + giá → kiểm tra bất thường  
    - Form cho quản lý (Admin):                
        - Form Thống kê -> Thống kê tin nhắn theo ngày, loại xe và biểu đồ thị trường
        - Form Quản lý tin đăng -> Xem, cập nhật tin đăng bất thường
    """)
    
    st.write("---")

    # ============================================================
    # CONCLUSION
    # ============================================================
    st.markdown("""
    ### 🎯 **Kết luận**
    Các bài toán trên tạo thành một hệ thống phân tích & gợi ý toàn diện giúp:
    - Định giá chính xác
    - Phát hiện bất thường
    - Gợi ý thông minh
    - Phân khúc thị trường hiệu quả
                
    Kết quả mang lại một bộ công cụ hỗ trợ phân tích tốt cho việc đưa ra gợi ý hiệu quả trong hệ thống mua bán xe máy trực tuyến.
    """)
