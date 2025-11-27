import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def price_comparison_chart(gia_ban_nhanh, gia_de_xuat, gia_toi_da, gia_min, gia_max):
    """Biểu đồ so sánh các mức giá - Bar Chart ngang"""
    
    data = {
        'Loại giá': [
            'Giá bán nhanh<br>(Nhanh chóng)',
            'Giá đề xuất<br>(Cân bằng)',
            'Giá tối đa<br>(Lợi nhuận cao)'
        ],
        'Giá trị': [gia_ban_nhanh, gia_de_xuat, gia_toi_da],
        'Màu': ['#28a745', '#ffc107', '#dc3545']
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=data['Loại giá'],
        x=data['Giá trị'],
        orientation='h',
        marker=dict(color=data['Màu']),
        text=[f"{v/1000000:.1f}M" for v in data['Giá trị']],
        textposition='outside',
        hovertemplate='%{y}<br>%{x:,.0f} VND<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '📊 So sánh các mức giá',
            'font': {'size': 16, 'family': 'Arial'}
        },
        xaxis_title='',
        yaxis_title='',
        height=320,
        width=550,
        margin=dict(l=30, r=30, t=30, b=20),
        showlegend=False,
        xaxis=dict(
            range=[gia_min * 0.9, gia_max * 1.1],
            tickformat=',.0f',
            ticksuffix='M',
            tickvals=[i * 1000000 for i in range(int(gia_min/1000000), int(gia_max/1000000)+2)],
            ticktext=[f"{i}M" for i in range(int(gia_min/1000000), int(gia_max/1000000)+2)]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig


def price_range_chart(gia_ban_nhanh, gia_de_xuat, gia_toi_da, gia_min, gia_max):
    # Biểu đồ khoảng giá hợp lý - Range với markers
    
    fig = go.Figure()
    
    # Vùng nền gradient
    fig.add_trace(go.Bar(
        x=[gia_max - gia_min],
        y=['Khoảng giá'],
        base=gia_min,
        orientation='h',
        marker=dict(
            color='rgba(200,200,200,0.2)',
            line=dict(width=0)
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Markers cho các mức giá
    markers_data = [
        (gia_min, 'Thấp nhất', '#28a745', 'triangle-down', 15),
        (gia_ban_nhanh, '⚡', '#28a745', 'line-ns-open', 30),
        (gia_de_xuat, '⭐ ĐỀ XUẤT', '#ffc107', 'line-ns-open', 35),
        (gia_toi_da, '💰', '#dc3545', 'line-ns-open', 30),
        (gia_max, 'Cao nhất', '#dc3545', 'triangle-down', 15)
    ]
    
    for price, label, color, symbol, size in markers_data:
        fig.add_trace(go.Scatter(
            x=[price],
            y=['Khoảng giá'],
            mode='markers+text',
            marker=dict(size=size, color=color, symbol=symbol, line=dict(width=2, color='white')),
            text=[label],
            textposition='bottom center',
            textfont=dict(size=12, color=color, family='Arial Bold'),
            showlegend=False,
            hovertemplate=f'{label}<br><br>{price:,.0f} VND<extra></extra>'
        ))
    
    # Thêm giá trị số
    for price in [gia_min, gia_ban_nhanh, gia_de_xuat, gia_toi_da, gia_max]:
        fig.add_annotation(
            x=price,
            y='Khoảng giá',
            text=f"{price/1000000:.1f}M",
            showarrow=False,
            yshift=30,
            font=dict(size=12, color='#333')
        )
    
    fig.update_layout(
        title={
            'text': '📏 Khoảng giá hợp lý',
            'font': {'size': 22, 'family': 'Arial'}
        },
        xaxis_title='',
        yaxis_title='',
        height=160,
        margin=dict(l=20, r=20, t=36, b=50),
        showlegend=False,
        xaxis=dict(
            range=[gia_min * 0.95, gia_max * 1.05],
            showticklabels=False,
            showgrid=False
        ),
        yaxis=dict(showticklabels=False),
        plot_bgcolor='rgba(240,240,240,0.3)',
        paper_bgcolor='white'
    )
    
    return fig

def show_price_suggestion(gia_ban_nhanh, gia_de_xuat, gia_toi_da):
    """Hiển thị toàn bộ phần gợi ý giá bán"""
    
    # Header
    st.markdown("### 💡 Gợi ý giá bán")
    st.markdown("*Chọn mức giá phù hợp với mục tiêu của bạn*")    

    # 3. Cards chi tiết
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                    padding: 15px; border-radius: 5px; border: 2px solid #28a745;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 30px; margin-bottom: 5px;">⚡ Giá bán nhanh</div>            
            <h2 style="color: #28a745; margin: 5px 0;">{gia_ban_nhanh:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #155724;">✅ Giá cạnh tranh tốt</p>
            <p style="margin: 5px 0; font-size: 14px; color: #155724;">✅ Thu hút nhiều người mua</p>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">⚠️ Lợi nhuận <b>thấp hơn -5%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    padding: 15px; border-radius: 5px; border: 3px solid #ffc107;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
            <div style="font-size: 30px; margin-bottom: 5px;">⭐ Giá đề xuất</div>            
            <h2 style="color: #d39e00; margin: 5px 0;">{gia_de_xuat:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">✅ Giá hợp lý, cạnh tranh công bằng</p>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">✅ Khách hàng tin tưởng</p>
            <p style="margin: 5px 0; font-size: 14px; color: #28a745; font-weight: bold;">⭐ KHUYẾN NGHỊ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                    padding: 15px; border-radius: 5px; border: 2px solid #dc3545;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 30px; margin-bottom: 5px;">💰 Giá tối đa</div>            
            <h2 style="color: #dc3545; margin: 5px 0;">{gia_toi_da:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #721c24;">✅ Lợi nhuận <b>cao hơn +10%</b></p>
            <p style="margin: 5px 0; font-size: 14px; color: #721c24;">✅ Kén khách mua, bán chậm</p>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">⚠️ Cần phải có thêm ưu điểm đặc biệt</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")

    # Lưu ý
    st.info("💡 **Lưu ý:** Giá đề xuất (⭐) là mức giá cân bằng tốt nhất giữa tốc độ bán và lợi nhuận, dựa trên phân tích thị trường và đặc điểm xe của bạn.")

# =============================================================== 

def gauge_chart_gia(gia_pred, gia_min, gia_max):
    """
    Biểu đồ đồng hồ đánh giá mức giá
    Màu xanh lá = Rẻ, Vàng = Hợp lý, Đỏ = Mắc
    Hiển thị giá trị tại vị trí ranh giới giữa các vùng màu
    """
    # Tính phần trăm vị trí
    if gia_max != gia_min:
        vi_tri = ((gia_pred - gia_min) / (gia_max - gia_min)) * 100
    else:
        vi_tri = 50
    
    # Xác định mức giá
    if vi_tri < 33:
        muc_gia = "RẺ"
        mau = "#28a745"  # Xanh lá
    elif vi_tri < 67:
        muc_gia = "HỢP LÝ"
        mau = "#ffc107"  # Vàng
    else:
        muc_gia = "MẮC"
        mau = "#dc3545"  # Đỏ
    
    # Tính giá trị tại ranh giới
    gia_ranh_gioi_1 = gia_min + (gia_max - gia_min) * 0.33  # Ranh giới xanh-vàng
    gia_ranh_gioi_2 = gia_min + (gia_max - gia_min) * 0.67  # Ranh giới vàng-hồng
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gia_pred,
        domain={'x': [0, 1], 'y': [0, 1]},        
        gauge={
            'axis': {
                'range': [gia_min, gia_max], 
                'tickwidth': 1, 
                'tickcolor': "darkgray",
                'tickmode': 'array',
                'tickvals': [gia_min, gia_ranh_gioi_1, gia_ranh_gioi_2, gia_max],
                'ticktext': [f'{gia_min/1_000_000:.02f}M', f'{gia_ranh_gioi_1/1_000_000:.02f}M', f'{gia_ranh_gioi_2/1_000_000:.02f}M', f'{gia_max/1_000_000:.02f}M'],
                # 'tickfont': {'size': 12, 'color': 'black'}
            },
            'bar': {'color': mau, 'thickness': 0.5},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [gia_min, gia_ranh_gioi_1], 'color': '#d4edda'},
                {'range': [gia_ranh_gioi_1, gia_ranh_gioi_2], 'color': '#fff3cd'},
                {'range': [gia_ranh_gioi_2, gia_max], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': mau, 'width': 4},
                'thickness': 0.6,
                'value': gia_pred
            }
        }
    ))    
    
    fig.update_layout(        
        height=300,
        margin=dict(l=20, r=20, t=80, b=20),
        font={'family': "Arial"},
        # font={'family': "Roboto", 'color': "black"}
        title={
            'text': f"<b>MỨC GIÁ: {muc_gia}</b>",
            'y': 0.85,       # Vị trí theo chiều dọc (0-1). 0.9 là gần đỉnh.
            'x': 0.5,        # Vị trí theo chiều ngang (0-1). 0.5 là giữa.
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': "#2c3e50"}
        }          
    )
    return fig

def price_comparison_gauge(gia_nguoi_ban, gia_du_doan, gia_min_thi_truong, gia_max_thi_truong):
    """Biểu đồ gauge so sánh giá"""
    fig = go.Figure()
    
    # Xác định màu dựa vào mức lệch
    lech_phan_tram = abs((gia_nguoi_ban - gia_du_doan) / gia_du_doan * 100)
    if lech_phan_tram > 20:
        bar_color = '#dc3545'  # Đỏ
    elif lech_phan_tram > 10:
        bar_color = '#ffc107'  # Vàng
    else:
        bar_color = '#28a745'  # Xanh
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=gia_nguoi_ban,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Giá người bán</b>", 'font': {'size': 20}},
        number={'suffix': " VND", 'font': {'size': 32}, 'valueformat': ',.0f'},
        gauge={
            'axis': {
                'range': [gia_min_thi_truong, gia_max_thi_truong],
                'tickformat': ',.0f',
                'ticksuffix': 'M',
                'tickvals': [gia_min_thi_truong, gia_du_doan, gia_max_thi_truong],
                'ticktext': [f'{gia_min_thi_truong/1000000:.1f}M', 
                           f'{gia_du_doan/1000000:.1f}M', 
                           f'{gia_max_thi_truong/1000000:.1f}M']
            },
            'bar': {'color': bar_color, 'thickness': 0.6},
            'bgcolor': "white",
            'steps': [
                {'range': [gia_min_thi_truong, gia_du_doan], 'color': '#d4edda'},
                {'range': [gia_du_doan, gia_max_thi_truong], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': '#ffc107', 'width': 4},
                'thickness': 0.75,
                'value': gia_du_doan
            }
        }
    ))

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def thanh_mau_gia(gia_pred, gia_min, gia_max):
    """
    Biểu đồ thanh với 3 vùng màu: Rẻ (Xanh) - Hợp lý (Vàng) - Mắc (Đỏ)
    """
    # Tính phần trăm vị trí
    if gia_max != gia_min:
        vi_tri_phan_tram = ((gia_pred - gia_min) / (gia_max - gia_min)) * 100
    else:
        vi_tri_phan_tram = 50
    
    # Xác định mức giá và màu
    if vi_tri_phan_tram < 33:
        muc_gia = "RẺ"
        mau_chi = "#28a745"
    elif vi_tri_phan_tram < 67:
        muc_gia = "HỢP LÝ"
        mau_chi = "#ffc107"
    else:
        muc_gia = "MẮC"
        mau_chi = "#dc3545"
    
    fig = go.Figure()
    
    # Vẽ 3 vùng màu nền
    khoang = (gia_max - gia_min) / 3
    
    # Vùng RẺ (xanh)
    fig.add_shape(type="rect",
        x0=gia_min, y0=-0.5, x1=gia_min + khoang, y1=0.5,
        fillcolor="#d4edda", line=dict(width=0), layer="below"
    )
    
    # Vùng HỢP LÝ (vàng)
    fig.add_shape(type="rect",
        x0=gia_min + khoang, y0=-0.5, x1=gia_min + 2*khoang, y1=0.5,
        fillcolor="#fff3cd", line=dict(width=0), layer="below"
    )
    
    # Vùng MẮC (đỏ)
    fig.add_shape(type="rect",
        x0=gia_min + 2*khoang, y0=-0.5, x1=gia_max, y1=0.5,
        fillcolor="#f8d7da", line=dict(width=0), layer="below"
    )
    
    # Đường viền ngoài
    fig.add_shape(type="rect",
        x0=gia_min, y0=-0.5, x1=gia_max, y1=0.5,
        fillcolor="rgba(0,0,0,0)", line=dict(color="gray", width=2)
    )
    
    # Thêm chỉ báo giá hiện tại (mũi tên + chấm)
    fig.add_trace(go.Scatter(
        x=[gia_pred],
        y=[0],
        mode='markers+text',
        marker=dict(size=20, color=mau_chi, symbol='diamond', 
                    line=dict(color='white', width=2)),
        text=[f'{gia_pred} tr'],
        textposition='top center',
        textfont=dict(size=16, color=mau_chi, family='Arial Black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Thêm nhãn vùng
    fig.add_trace(go.Scatter(
        x=[gia_min + khoang/2, gia_min + 1.5*khoang, gia_min + 2.5*khoang],
        y=[0, 0, 0],
        mode='text',
        text=['RẺ', 'HỢP LÝ', 'MẮC'],
        textfont=dict(size=14, color=['#28a745', '#ff8c00', '#dc3545'], 
                      family='Arial Black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Thêm giá trị min/max
    fig.add_trace(go.Scatter(
        x=[gia_min, gia_max],
        y=[-0.5, -0.5],
        mode='text',
        text=[f'{gia_min} tr', f'{gia_max} tr'],
        textposition=['top left', 'top right'],
        textfont=dict(size=11, color='gray'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'<b>ĐÁNH GIÁ GIÁ: {muc_gia}</b>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color=mau_chi)
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[gia_min - 0.3, gia_max + 0.3]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-1, 1]
        ),
        plot_bgcolor='white',
        height=250,
        margin=dict(l=20, r=20, t=80, b=40)
    )
    
    return fig


def chi_so_gia(gia_pred, gia_min, gia_max):
    """
    Indicator đơn giản với số lớn và màu sắc
    """
    # Tính phần trăm
    if gia_max != gia_min:
        vi_tri = ((gia_pred - gia_min) / (gia_max - gia_min)) * 100
    else:
        vi_tri = 50
    
    if vi_tri < 33:
        muc_gia = "RẺ"
        mau = "#28a745"
        icon = "👍"
    elif vi_tri < 67:
        muc_gia = "HỢP LÝ"
        mau = "#ffc107"
        icon = "✅"
    else:
        muc_gia = "MẮC"
        mau = "#dc3545"
        icon = "⚠️"
    
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=gia_pred,
        number={'suffix': " triệu", 'font': {'size': 60, 'color': mau}},
        title={'text': f"{icon} <b>{muc_gia}</b> {icon}", 
               'font': {'size': 30, 'color': mau}},
        delta={'reference': (gia_min + gia_max) / 2, 
               'relative': False,
               'valueformat': '.2f',
               'suffix': ' tr so với trung bình',
               'font': {'size': 14}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig

def price_comparison_bar(gia_nguoi_ban, gia_du_doan, gia_min_thi_truong, gia_max_thi_truong):
    """Biểu đồ cột so sánh giá"""
    fig = go.Figure()
    
    data = {
        'Loại giá': ['Giá thấp nhất\n(thị trường)', 'Giá dự đoán\n(hệ thống)', 
                     'Giá người bán', 'Giá cao nhất\n(thị trường)'],
        'Giá trị': [gia_min_thi_truong, gia_du_doan, gia_nguoi_ban, gia_max_thi_truong],
        'Màu': ['#28a745', '#ffc107', "#4070f3", '#dc3545']
    }
    
    fig.add_trace(go.Bar(
        x=data['Loại giá'],
        y=data['Giá trị'],
        marker=dict(
            color=data['Màu'],
            line=dict(color='white', width=2)
        ),
        text=[f"{v/1000000:.1f}M" for v in data['Giá trị']],
        textposition='outside',
        hovertemplate='%{x}<br>%{y:,.0f} VND<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': '📊 So sánh với thị trường', 'font': {'size': 18}},
        yaxis_title='Giá (VND)',
        yaxis=dict(tickformat=',.0f'),
        height=380,
        margin=dict(l=20, r=20, t=60, b=0),
        showlegend=False,        
        plot_bgcolor='white'
    )
    
    return fig

# =============================================================== 
def show_price_suggestion_advance(gia_ban_nhanh, gia_de_xuat, gia_toi_da):
    """Hiển thị toàn bộ phần gợi ý giá bán với khả năng chọn"""
    
    # Khởi tạo session state để lưu lựa chọn
    if 'selected_price' not in st.session_state:
        st.session_state.selected_price = None
    if 'selected_price_value' not in st.session_state:
        st.session_state.selected_price_value = None
    
    # Header
    st.markdown("### 💡 Gợi ý giá bán")
    st.markdown("*Chọn mức giá phù hợp với mục tiêu của bạn*")
    st.divider()
    
    # 3. Cards chi tiết - CÓ THỂ CLICK
    col1, col2, col3 = st.columns(3)
    
    # Dữ liệu các card
    cards = [
        {
            'key': 'nhanh',
            'title': 'Giá bán nhanh',
            'price': gia_ban_nhanh,
            'icon': '⚡',
            'bg_color': '#d4edda',
            'border_color': '#28a745',
            'text_color': '#155724',
            'price_color': '#28a745',
            'features': [
                '✅ Bán trong 1-2 tuần',
                '✅ Thu hút nhiều người mua',
                '⚠️ Lợi nhuận thấp hơn 5%'
            ]
        },
        {
            'key': 'de_xuat',
            'title': 'Giá đề xuất',
            'price': gia_de_xuat,
            'icon': '⭐',
            'bg_color': '#fff3cd',
            'border_color': '#ffc107',
            'text_color': '#856404',
            'price_color': '#d39e00',
            'features': [
                '✅ Cân bằng tốt nhất',
                '✅ Bán trong 2-4 tuần',
                '⭐ KHUYẾN NGHỊ'
            ]
        },
        {
            'key': 'toi_da',
            'title': 'Giá tối đa',
            'price': gia_toi_da,
            'icon': '💰',
            'bg_color': '#f8d7da',
            'border_color': '#dc3545',
            'text_color': '#721c24',
            'price_color': '#dc3545',
            'features': [
                '✅ Lợi nhuận cao nhất',
                '⚠️ Cần thời gian bán lâu',
                '⚠️ Ít người mua quan tâm'
            ]
        }
    ]
    
    # Hiển thị 3 cards với buttons
    for col, card in zip([col1, col2, col3], cards):
        with col:
            # Kiểm tra xem card này có được chọn không
            is_selected = st.session_state.selected_price == card['key']
            
            # Thêm checkmark nếu được chọn
            checkmark = '<div style="position: absolute; top: 10px; right: 10px; font-size: 24px; color: #28a745;">✔</div>' if is_selected else ''
            
            # Border thêm nếu được chọn
            border_width = '4px' if is_selected else '2px'
            box_shadow = '0 6px 12px rgba(0,0,0,0.2)' if is_selected else '0 2px 4px rgba(0,0,0,0.1)'
            
            # Hiển thị card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {card['bg_color']} 0%, {card['bg_color']}dd 100%); 
                        padding: 20px; border-radius: 10px; border: {border_width} solid {card['border_color']};
                        box-shadow: {box_shadow}; position: relative; cursor: pointer;
                        transition: all 0.3s ease;">
                {checkmark}
                <div style="font-size: 40px; margin-bottom: 10px;">{card['icon']}</div>
                <h4 style="color: {card['text_color']}; margin: 0;">{card['title']}</h4>
                <h2 style="color: {card['price_color']}; margin: 10px 0;">{card['price']:,.0f}</h2>
                {''.join([f'<p style="margin: 5px 0; font-size: 13px; color: {card["text_color"]};">{f}</p>' for f in card['features']])}
            </div>
            """, unsafe_allow_html=True)
            
            # Button ẩn để click
            if st.button(f"Chọn {card['title']}", key=f"btn_{card['key']}", use_container_width=True):
                st.session_state.selected_price = card['key']
                st.session_state.selected_price_value = card['price']
                st.rerun()
    
    st.markdown("")
    
    # Hiển thị giá đã chọn
    if st.session_state.selected_price_value:
        st.success(f"✅ **Giá đã chọn:** {st.session_state.selected_price_value:,.0f} VND")
        
        # Form nhập giá (có thể chỉnh sửa)
        with st.form("price_form"):
            st.markdown("#### 📝 Xác nhận giá bán")
            gia_ban_cuoi = st.number_input(
                "Giá bán cuối cùng (VND)",
                min_value=0,
                value=st.session_state.selected_price_value,
                step=100000,
                format="%d"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("💾 Xác nhận giá", type="primary", use_container_width=True)
            with col_b:
                reset = st.form_submit_button("🔄 Chọn lại", use_container_width=True)
            
            if submit:
                st.success(f"✅ Đã lưu giá bán: **{gia_ban_cuoi:,.0f} VND**")
                # Ở đây bạn có thể lưu vào database hoặc xử lý tiếp
                return gia_ban_cuoi
            
            if reset:
                st.session_state.selected_price = None
                st.session_state.selected_price_value = None
                st.rerun()
    
    # Lưu ý
    st.info("💡 **Lưu ý:** Giá đề xuất (⭐) là mức giá cân bằng tốt nhất giữa tốc độ bán và lợi nhuận, dựa trên phân tích thị trường và đặc điểm xe của bạn.")
    
    return st.session_state.selected_price_value

def bieu_do_gia_xe(thuong_hieu, dong_xe, df):
    fig = go.Figure()
        
    fig.add_trace(go.Histogram(
        x=df['gia'],
        nbinsx=30,
        name='Phân bố giá',
        marker=dict(color='#3498db', opacity=0.7),
        hovertemplate='Giá: %{x:.1f}M<br>Số tin: %{y}<extra></extra>'
    ))
    
    # Add average line
    fig.add_vline(
        x=df['gia'].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Giá TB: {df['gia'].mean():.1f}M",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title=f"Phân Bố Giá {thuong_hieu} {dong_xe}",
        xaxis_title="Giá (Triệu VNĐ)",
        yaxis_title="Số Lượng Tin",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)    
    
    return fig    