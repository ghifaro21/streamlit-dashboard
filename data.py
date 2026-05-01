import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df = df[df['Location'] != "Indonesia"]
    return df

def select_location(df):
    locations = ["Semua Provinsi"] + sorted(list(df['Location'].unique()))
    return st.sidebar.selectbox(
        "Pilih Provinsi",
        options=locations
    )

def filter_data(df, year=None, location=None):
    if year and year != "Semua Tahun":
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location and location != "Semua Provinsi":
        df = df[df['Location'].isin(location)]
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
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

def total_death(df):
    total_meninggal = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_meninggal['Total Deaths'].sum()

def total_recovered(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

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

def bar_chart1(df):
    import plotly.express as px
    import streamlit as st

    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, "Total Deaths").sort_values("Total Deaths")

    fig = px.bar(
        top5,
        x='Total Deaths',
        y='Location',
        orientation='h',  # 👉 lebih clean horizontal
        color='Total Deaths',
        color_continuous_scale=[
            "#FFE5E5",
            "#FF9999",
            "#FF4D4D",
            "#CC0000"
        ],
        title='🔝 5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=0, r=0, t=50, b=0),
        title={"x": 0.5, "xanchor": "center"},
        coloraxis_showscale=False
    )

    fig.update_traces(
        texttemplate='%{x:.0f}',
        textposition='outside'
    )

    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    import plotly.express as px
    import streamlit as st

    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, "Total Recovered").sort_values("Total Recovered")

    fig = px.bar(
        top5,
        x='Total Recovered',
        y='Location',
        orientation='h',
        color='Total Recovered',
        color_continuous_scale=[
            "#1F1FFF",
            "#4949FF",
            "#7879FF",
            "#A3A3FF"
        ],
        title='🔝 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Sembuh', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=0, r=0, t=50, b=0),
        title={"x": 0.5, "xanchor": "center"},
        coloraxis_showscale=False
    )

    fig.update_traces(
        texttemplate='%{x:.0f}',
        textposition='outside'
    )

    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    import plotly.express as px
    import pandas as pd
    import streamlit as st

    df = df.copy()

    # Format tanggal
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filter tahun
    if year and year != "Semua Tahun":
        df = df[df['Date'].dt.year == int(year)]

    df_agg = df.groupby(
        ['Location', 'Latitude', 'Longitude'],
        as_index=False
    )['New Cases'].sum()

    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return

    df_map['Size'] = df_map['New Cases'] / df_map['New Cases'].max() * 40

    # Plot map
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="Size",
        color="New Cases",
        hover_name="Location",
        hover_data={
            "New Cases": True,
            "Latitude": False,
            "Longitude": False,
            "Size": False
        },
        zoom=3.5,
        center={"lat": -2.5, "lon": 118},
        size_max=40,
        opacity=0.75,
        color_continuous_scale=[
            "#FFE5E5",
            "#FF9999",
            "#FF4D4D",
            "#CC0000"
        ],
        title=f"📍 Sebaran Kasus Baru Covid-19 ({year if year else 'Semua Tahun'})"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        coloraxis_colorbar=dict(
            title="Kasus Baru",
            thickness=15,
            len=0.7
        )
    )

    fig.update_traces(
        marker=dict(opacity=0.8)
    )

    st.plotly_chart(fig, use_container_width=True)