import plotly.express as px
import streamlit as st
from data import *

# judul dashboard
def judul():
    st.title("🦠Dashboard Covid-19")
    st.write("Selamat Datang di Dashboard Covid-19, disini kita akan melihat data-data mengenai Covid-19 di Indonesia🟥⬜")

st.sidebar.title("🧭Navigasi")
menu = st.sidebar.radio("Menu", ["🏠Home", "📊Data Page"])

df = load_data()
st.sidebar.markdown("### 🔎 Filter Data")

year = select_year()

# 👉 MULTI LOCATION
locations = sorted(df['Location'].unique())
selected_locations = st.sidebar.multiselect(
    "Pilih Provinsi 📍",
    options=locations,
    default=locations
)

df_filtered = filter_data(df, year, selected_locations)

if menu == "🏠Home":
    judul()

    kolom(df_filtered)
    map_chart(df_filtered, year)
    pie_chart(df_filtered)

    col1, col2 = st.columns(2)
    with col1:
        bar_chart1(df_filtered)
    with col2:
        bar_chart2(df_filtered)

elif menu == "📊Data Page":
    judul()
    show_data(df_filtered)

st.markdown("---")
st.markdown("© 2026 I.T Ghifari/184240028. All Rights Reserved.")