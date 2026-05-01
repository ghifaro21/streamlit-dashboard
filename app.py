import plotly.express as px
import streamlit as st
from data import *

# judul dashboard
def judul():
    st.title("🦠Dashboard Covid-19")
    st.write("Selamat Datang di Dashboard Covid-19, disini kita akan melihat data-data mengenai Covid-19 di Indonesia🟥⬜")

st.sidebar.title("🧭Navigasi")
menu = st.sidebar.radio("Menu", ["🏠Home", "📊Data Page"])

if menu == "🏠Home":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year)
    kolom(df_filtered)
    pie_chart(df_filtered)
    
elif menu == "📊Data Page":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)

st.markdown("---")
st.markdown("© 2026 I.T Ghifari/184240028. All Rights Reserved.")