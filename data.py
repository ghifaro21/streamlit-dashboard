import pandas as pd
import streamlit as st

def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    return df

def show_data():
    df = load_data()
    st.subheader("📊Data Covid-19 di Indonesia")
    
    total_kasus = df['Total Cases'].max()
    st.metric(label="Total Kasus Keseluruhan", value=f"{total_kasus:,}")
    
    df_selected = df.loc[:, 'Location':'Total Recovered']
    st.dataframe(df_selected.head(10))

    st.subheader("📊Statistik Deskriptif Dataset")
    st.write(df.describe())