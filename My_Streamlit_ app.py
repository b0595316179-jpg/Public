import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from pathlib import Path

st.set_page_config(
    page_title="سجل صمود العائلات",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    :root {
        --deep-slate: #2C3E50;
        --muted-teal: #5F9EA0;
        --warm-terracotta: #E07A5F;
        --soft-cream: #F8F5F2;
        --gentle-gray: #95A5A6;
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 700;
        color: var(--deep-slate);
        text-align: center;
        margin-bottom: 1rem;
        padding: 2rem 0;
        border-bottom: 3px solid var(--muted-teal);
    }
    
    .subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        color: var(--gentle-gray);
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.8;
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--soft-cream) 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--muted-teal) 0%, #4A7C7E 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(95, 158, 160, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4A7C7E 0%, var(--muted-teal) 100%);
        box-shadow: 0 6px 20px rgba(95, 158, 160, 0.4);
        transform: translateY(-2px);
    }
    
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #E8E8E8;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--muted-teal);
        box-shadow: 0 0 0 3px rgba(95, 158, 160, 0.1);
    }
    
    .story-box {
        background: linear-gradient(135deg, #FFF8F3 0%, #FFEEE4 100%);
        border-right: 4px solid var(--warm-terracotta);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        line-height: 1.9;
        color: var(--deep-slate);
    }
    
    .css-1d391kg {
        background-color: var(--soft-cream);
    }
    
    h2, h3 {
        color: var(--deep-slate);
        font-weight: 600;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--muted-teal);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--deep-slate);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem;
        color: var(--gentle-gray);
        font-weight: 500;
    }
    
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .success-message {
        background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%);
        color: #155724;
        padding: 1.5rem;
        border-radius: 12px;
        border-right: 4px solid #28A745;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #FFF3CD 0%, #FFE69C 100%);
        color: #856404;
        padding: 1.5rem;
        border-radius: 12px;
        border-right: 4px solid #FFC107;
        margin: 1rem 0;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

class DataManager:
    def __init__(self, filename="families_data.csv"):
        self.filename = filename
        self.filepath = Path(filename)
    
    def load_data(self):
        if self.filepath.exists():
            try:
                df = pd.read_csv(self.filename, encoding='utf-8-sig')
                return df
            except Exception as e:
                st.error(f"خطأ في تحميل البيانات: {str(e)}")
                return self._create_empty_dataframe()
        else:
            return self._create_empty_dataframe()
    
    def _create_empty_dataframe(self):
        return pd.DataFrame(columns=[
            'التاريخ',
            'اسم_العائلة',
            'عدد_الأفراد',
            'نوع_الفقد',
            'الاحتياجات_العاجلة',
            'الموقع_الجغرافي',
            'ملاحظات',
            'رقم_التواصل'
        ])
    
    def save_data(self, df):
        try:
            df.to_csv(self.filename, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            st.error(f"خطأ في حفظ البيانات: {str(e)}")
            return False
    
    def add_family(self, family_data):
        df = self.load_data()
        family_data['التاريخ'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        df = pd.concat([df, pd.DataFrame([family_data])], ignore_index=True)
        return self.save_data(df)
    
    def export_data(self, df):
        return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

def render_data_entry_form(data_manager):
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>سجل صمود عائلة جديدة</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-box'>
    <p style='margin: 0; font-size: 1.05rem;'>
    كل عائلة لها قصة، وكل قصة تستحق أن تُروى وأن تُدعم. 
    من خلال هذا النموذج، نوثق صمود عائلاتنا ونضمن وصول المساعدة لمن يحتاجها.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("family_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            family_name = st.text_input(
                "اسم العائلة *",
                placeholder="أدخل اسم العائلة الكريم",
                help="الاسم الكامل للعائلة"
            )
            
            num_members = st.number_input(
                "عدد أفراد العائلة *",
                min_value=1,
                max_value=50,
                value=5,
                help="إجمالي عدد الأفراد في العائلة"
            )
            
            loss_type = st.selectbox(
                "نوع الفقد أو الضرر *",
                [
                    "اختر نوع الفقد",
                    "فقد أحد أفراد العائلة",
                    "فقد المنزل بالكامل",
                    "فقد المنزل جزئياً",
                    "فقد مصدر الدخل",
                    "إصابات جسدية",
                    "نزوح قسري",
                    "متعدد (فقد وإصابات)"
                ],
                help="حدد نوع الضرر أو الفقد الذي تعرضت له العائلة"
            )
        
        with col2:
            needs = st.multiselect(
                "الاحتياجات العاجلة *",
                [
                    "مأوى مؤقت",
                    "غذاء ومياه",
                    "رعاية طبية",
                    "أدوية",
                    "ملابس",
                    "مواد نظافة",
                    "دعم نفسي",
                    "مساعدات مالية"
                ],
                help="اختر جميع الاحتياجات العاجلة (يمكن اختيار أكثر من حاجة)"
            )
            
            location = st.selectbox(
                "الموقع الجغرافي *",
                [
                    "اختر المنطقة",
                    "شمال غزة",
                    "غزة",
                    "الوسطى (دير البلح)",
                    "خان يونس",
                    "رفح",
                    "نازح خارج القطاع"
                ],
                help="المنطقة التي تتواجد فيها العائلة حالياً"
            )
            
            contact = st.text_input(
                "رقم التواصل (اختياري)",
                placeholder="+970 xx xxx xxxx",
                help="رقم هاتف للتواصل مع العائلة"
            )
        
        notes = st.text_area(
            "ملاحظات إضافية",
            placeholder="أي معلومات إضافية قد تساعد في تقديم الدعم الأمثل...",
            height=120,
            help="قصة العائلة أو أي تفاصيل إضافية مهمة"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submitted = st.form_submit_button("تسجيل البيانات", use_container_width=True)
        
        if submitted:
            if not family_name or family_name.strip() == "":
                st.error("الرجاء إدخال اسم العائلة")
            elif loss_type == "اختر نوع الفقد":
                st.error("الرجاء اختيار نوع الفقد")
            elif not needs:
                st.error("الرجاء تحديد الاحتياجات العاجلة")
            elif location == "اختر المنطقة":
                st.error("الرجاء اختيار الموقع الجغرافي")
            else:
                family_data = {
                    'اسم_العائلة': family_name.strip(),
                    'عدد_الأفراد': num_members,
                    'نوع_الفقد': loss_type,
                    'الاحتياجات_العاجلة': ", ".join(needs),
                    'الموقع_الجغرافي': location,
                    'ملاحظات': notes.strip() if notes else "لا توجد ملاحظات",
                    'رقم_التواصل': contact.strip() if contact else "غير متوفر"
                }
                
                if data_manager.add_family(family_data):
                    st.markdown("""
                    <div class='success-message'>
                    تم تسجيل بيانات العائلة بنجاح<br>
                    شكراً لك على توثيق هذه المعلومات المهمة
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("حدث خطأ في حفظ البيانات، الرجاء المحاولة مرة أخرى")

def render_analytics_dashboard(df):
    if df.empty:
        st.markdown("""
        <div class='warning-message'>
        لا توجد بيانات لعرضها حالياً<br>
        ابدأ بتسجيل بيانات العائلات من القسم أعلاه
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>لوحة الإحصائيات والتحليلات</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="إجمالي العائلات المسجلة",
            value=len(df),
            delta=None
        )
    
    with col2:
        st.metric(
            label="إجمالي الأفراد",
            value=df['عدد_الأفراد'].sum(),
            delta=None
        )
    
    with col3:
        avg_family_size = df['عدد_الأفراد'].mean()
        st.metric(
            label="متوسط أفراد العائلة",
            value=f"{avg_family_size:.1f}",
            delta=None
        )
    
    with col4:
        unique_locations = df['الموقع_الجغرافي'].nunique()
        st.metric(
            label="المناطق المتأثرة",
            value=unique_locations,
            delta=None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### التوزيع الجغرافي للعائلات")
        location_counts = df['الموقع_الجغرافي'].value_counts()
        
        fig_location = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            labels={'x': 'المنطقة', 'y': 'عدد العائلات'},
            color=location_counts.values,
            color_continuous_scale=['#5F9EA0', '#2C3E50'],
            text=location_counts.values
        )
        
        fig_location.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Tajawal", size=12),
            height=400,
            xaxis=dict(tickangle=-45)
        )
        
        fig_location.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        
        st.plotly_chart(fig_location, use_container_width=True)
    
    with col_chart2:
        st.markdown("### أنواع الفقد والأضرار")
        loss_counts = df['نوع_الفقد'].value_counts()
        
        fig_loss = px.pie(
            values=loss_counts.values,
            names=loss_counts.index,
            color_discrete_sequence=px.colors.sequential.Teal,
            hole=0.4
        )
        
        fig_loss.update_layout(
            font=dict(family="Tajawal", size=12),
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        
        fig_loss.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        
        st.plotly_chart(fig_loss, use_container_width=True)
    
    st.markdown("### الاحتياجات العاجلة الأكثر طلباً")
    
    all_needs = []
    for needs_str in df['الاحتياجات_العاجلة']:
        needs_list = [need.strip() for need in needs_str.split(',')]
        all_needs.extend(needs_list)
    
    needs_series = pd.Series(all_needs)
    needs_counts = needs_series.value_counts()
    
    fig_needs = go.Figure(go.Bar(
        x=needs_counts.values,
        y=needs_counts.index,
        orientation='h',
        marker=dict(
            color=needs_counts.values,
            colorscale=[[0, '#5F9EA0'], [0.5, '#E07A5F'], [1, '#2C3E50']],
            line=dict(color='white', width=2)
        ),
        text=needs_counts.values,
        textposition='outside'
    ))
    
    fig_needs.update_layout(
        xaxis_title="عدد العائلات",
        yaxis_title="نوع الحاجة",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Tajawal", size=12),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_needs, use_container_width=True)
    
    st.markdown("### توزيع أحجام العائلات")
    
    fig_family_size = px.histogram(
        df,
        x='عدد_الأفراد',
        nbins=20,
        labels={'عدد_الأفراد': 'عدد الأفراد', 'count': 'عدد العائلات'},
        color_discrete_sequence=['#5F9EA0']
    )
    
    fig_family_size.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Tajawal", size=12),
        height=350,
        showlegend=False,
        bargap=0.1
    )
    
    fig_family_size.update_traces(
        marker_line_color='white',
        marker_line_width=1.5
    )
    
    st.plotly_chart(fig_family_size, use_container_width=True)

def render_stories_section(df):
    if df.empty:
        return
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>القصص خلف الأرقام</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-box'>
    <p style='margin: 0; font-size: 1.05rem;'>
    خلف كل رقم وإحصائية، هناك عائلة بأحلامها وآلامها وصمودها. 
    هنا نروي قصصهم بكرامة واحترام.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### تصفية حسب المنطقة")
    selected_location = st.selectbox(
        "اختر المنطقة",
        ["جميع المناطق"] + list(df['الموقع_الجغرافي'].unique()),
        key="location_filter"
    )
    
    if selected_location != "جميع المناطق":
        filtered_df = df[df['الموقع_الجغرافي'] == selected_location]
    else:
        filtered_df = df
    
    st.markdown(f"**عدد العائلات: {len(filtered_df)}**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='story-box'>
                <h4 style='color: #2C3E50; margin-top: 0; font-size: 1.4rem;'>
                    عائلة {row['اسم_العائلة']}
                </h4>
                <p style='margin: 0.5rem 0; line-height: 1.8;'>
                    <strong>الموقع:</strong> {row['الموقع_الجغرافي']}<br>
                    <strong>عدد الأفراد:</strong> {row['عدد_الأفراد']} فرداً<br>
                    <strong>نوع الفقد:</strong> {row['نوع_الفقد']}<br>
                    <strong>الاحتياجات:</strong> {row['الاحتياجات_العاجلة']}<br>
                    <strong>التواصل:</strong> {row['رقم_التواصل']}<br>
                    <strong>تاريخ التسجيل:</strong> {row['التاريخ']}
                </p>
                <div style='background-color: rgba(255,255,255,0.5); padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
                    <strong style='color: #E07A5F;'>ملاحظات:</strong><br>
                    <em style='color: #2C3E50;'>{row['ملاحظات']}</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def render_data_table(df, data_manager):
    if df.empty:
        st.info("لا توجد بيانات لعرضها")
        return
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>جدول البيانات الكامل</h2>", unsafe_allow_html=True)
    
    col_options1, col_options2 = st.columns(2)
    
    with col_options1:
        show_columns = st.multiselect(
            "اختر الأعمدة للعرض",
            options=df.columns.tolist(),
            default=df.columns.tolist()
        )
    
    with col_options2:
        sort_by = st.selectbox(
            "ترتيب حسب",
            options=['التاريخ', 'اسم_العائلة', 'عدد_الأفراد', 'الموقع_الجغرافي']
        )
    
    display_df = df[show_columns].sort_values(by=sort_by, ascending=False)
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    st.markdown("### تصدير البيانات")
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        csv_data = data_manager.export_data(df)
        st.download_button(
            label="تحميل CSV",
            data=csv_data,
            file_name=f"families_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_export2:
        try:
            import io
            excel_buffer = io.BytesIO()
            
            try:
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='العائلات')
            except ImportError:
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='العائلات')
            
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="تحميل Excel",
                data=excel_data,
                file_name=f"families_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"تعذر إنشاء ملف Excel: {str(e)}\nيرجى استخدام CSV بدلاً منه")
            st.download_button(
                label="تحميل CSV (بديل)",
                data=csv_data,
                file_name=f"families_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_export3:
        json_data = df.to_json(orient='records', force_ascii=False, indent=2)
        st.download_button(
            label="تحميل JSON",
            data=json_data,
            file_name=f"families_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

def main():
    apply_custom_styling()
    
    st.markdown("""
    <div class='main-title'>
        سجل صمود العائلات - غزة
    </div>
    <div class='subtitle'>
        منصة إنسانية لتوثيق ودعم العائلات المنكوبة في قطاع غزة<br>
        كل عائلة لها قصة، وكل قصة تستحق أن تُروى
    </div>
    """, unsafe_allow_html=True)
    
    data_manager = DataManager()
    
    df = data_manager.load_data()
    
    with st.sidebar:
        st.markdown("### القائمة الرئيسية")
        st.markdown("---")
        
        page = st.radio(
            "اختر القسم",
            [
                "تسجيل عائلة جديدة",
                "لوحة الإحصائيات",
                "القصص خلف الأرقام",
                "عرض البيانات"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### إحصائيات سريعة")
        st.info(f"**إجمالي العائلات:** {len(df)}")
        st.info(f"**إجمالي الأفراد:** {df['عدد_الأفراد'].sum() if not df.empty else 0}")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #F8F5F2; border-radius: 10px;'>
            <p style='margin: 0; font-size: 0.9rem; color: #2C3E50;'>
                <strong>معاً نبني الأمل</strong><br>
                كل مساهمة تحدث فرقاً
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if page == "تسجيل عائلة جديدة":
        render_data_entry_form(data_manager)
        
    elif page == "لوحة الإحصائيات":
        render_analytics_dashboard(df)
        
    elif page == "القصص خلف الأرقام":
        render_stories_section(df)
        
    elif page == "عرض البيانات":
        render_data_table(df, data_manager)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #95A5A6;'>
        <p style='margin: 0;'>
            <strong>سجل صمود العائلات</strong> | تطبيق مفتوح المصدر للإنسانية<br>
            صُمم لخدمة أهلنا في غزة
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

