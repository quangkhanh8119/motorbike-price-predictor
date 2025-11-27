# Motorbike Price Predictor

Một ứng dụng học máy để dự đoán giá xe máy và phát hiện các trường hợp giá bất thường trên tập dữ liệu từ Chợ Tốt.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

## Tính năng

* **Dự đoán giá** sử dụng các mô hình hồi quy (regression models)
* **Phát hiện bất thường** (Anomaly detection) đối với các mức giá không phổ biến
* **Trực quan hóa dữ liệu** tương tác
* **Phân tích thị trường** và thông tin chi tiết

## Bắt đầu

### Cài đặt
```bash
git clone https://github.com/yourusername/motorbike-price-predictor.git
cd motorbike-price-predictor
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
streamlit run home.py
```

## Cấu trúc dự án
```
motorbike-price-predictor/
├── assets/          		# Images, logos, styles
├── data/           		# Raw, processed, results data
├── models/         		# Trained ML models
├── src/            		# Source code
│   ├── utils/      		# Utility functions
│   ├── visualization/  	# Charts and plots
│   └── pages/      		# Streamlit pages
└── home.py         		# Main application
```

## Công nghệ sử dụng

- **Framework**: Streamlit
- **ML Libraries**: Scikit-learn, XGBoost
- **Visualization**: Plotly, Matplotlib
- **Data Processing**: Pandas, NumPy

## Bộ dữ liệu

Data collected from Vietnamese motorcycle marketplaces including:
- Price information
- Motorcycle specifications
- Seller details
- Market conditions

## Models

- **Regression Model**: Random Forest / XGBoost for price prediction
- **Anomaly Detection**: Isolation Forest / DBSCAN
- **Text Processing**: TF-IDF for description analysis


## Tác giả

- **Nguyễn Quang Khánh** - [GitHub](https://github.com/quangkhanh8119)
- **Nguyễn Đức Bằng** - [GitHub](https://github.com/????)

