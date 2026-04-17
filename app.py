import streamlit as st
from data import *

# judul dashboard
def judul():
    st.title("📊Dashboard Covid-19")
    st.write("Selamat Datang di Dashboard Covid-19, disini kita akan melihat data-data mengenai Covid-19 di seluruh dunia")

st.sidebar.title("🧭Navigasi")
menu = st.sidebar.radio("Menu", ["🏠Home", "📊Data"])

if menu == "🏠Home":
    judul()
elif menu == "📊Data":
    judul()
    show_data()

st.markdown("---")
st.markdown("© 2026 I.T Ghifari/184240028. All Rights Reserved.")