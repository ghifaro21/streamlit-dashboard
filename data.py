import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    return df

def filter_data(df, year="Semua Tahun"):
    if year and year != "Semua Tahun":
        df = df[df['Date'].astype(str).str.contains(str(year))]
    return df

def select_year():
    return st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun", 2020, 2021, 2022])
    
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 di Indonesia🟥⬜")
    st.dataframe(df_selected.head(10))
    st.subheader("📊Statistik Deskriptif Dataset")
    st.write(df.describe()  )

def total_case(df):
    return df['New Cases'].sum()

def total_death(df):
    return df['New Deaths'].sum()

def total_recovered(df):
    return df['New Recovered'].sum()

def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovered(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🚩Total Kasus", value=f"{kasus/1000:.1f}K", border=True)
    col2.metric("☠️Total Kematian", value=f"{kematian/1000:.1f}K", border=True)
    col3.metric("❤️‍🩹Total Sembuh", value=f"{sembuh/1000:.1f}K", border=True)

def pie_chart(df):
    jml_kematian = total_death(df)
    jml_sembuh = total_recovered(df)
    
    data = {
        'Status' : ['Meninggal', 'Sembuh'],
        'Jumlah' : [jml_kematian, jml_sembuh]
    }
    fig = px.pie(
        data,
        names = 'Status',
        values = 'Jumlah',
        title = 'Perbandingan Total Kematian V Total Sembuh',
        hole = 0.5,
        color_discrete_map = {
            'Meninggal' : 'red',
            'Sembuh' : 'blue'
        }
    )
    st.plotly_chart(fig, use_container_width=True)