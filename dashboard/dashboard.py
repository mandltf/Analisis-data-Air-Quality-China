import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

st.title("🌬☁ Air Quality Analysis Dashboard")

BASE_DIR = os.path.dirname(__file__)
data_path = os.path.join(BASE_DIR, "main_data.csv")
df_clean_iter = pd.read_csv(data_path)

st.sidebar.markdown(
    f"""
    ### 🚩 Lokasi Stasiun Pemantauan Udara
    - **Dongsi** : Pusat Kota Beijing, area dengan kepadatan lalu lintas tinggi.
    - **Wanshouxigong** : Area perumahan di barat daya Beijing.
    - **Changping** : Terletak di pinggiran utara Beijing, dekat dengan area industri ringan.
    - **Huairou** : Terletak di pinggiran utara Beijing, dikenal dengan area wisata alamnya.
    """
    )
station_pilihan = st.sidebar.selectbox(
    "Pilih Stasiun",
    sorted(df_clean_iter["station"].unique())
)

with st.expander("Tingkat polusi udara di berbagai stasiun (2013–2017)"):
    rata_pm25_station = (
        df_clean_iter.groupby("station")["PM2.5"]
        .mean()
        .sort_values(ascending=False)
    )

    stations = rata_pm25_station.index.tolist()
    values = rata_pm25_station.values.tolist()

    st.subheader("Mean PM2.5")
    col_1, col_2, col_3, col_4 = st.columns(4)
    cols = [col_1, col_2, col_3, col_4]

    for col, station, value in zip(cols, stations, values):
        with col:
            st.metric(
                label=f"### {station}",
                value=f"{value:.2f}"
            )

    max_value = rata_pm25_station.max()
    warna = [
        "red" if value == max_value else "gray"
        for value in rata_pm25_station.values
    ]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(
        rata_pm25_station.index,
        rata_pm25_station.values,
        color=warna
    )

    ax.set_title("Rata-rata PM2.5 per Stasiun (2013–2017)")
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Rata-rata PM2.5")
    plt.tight_layout()
    st.pyplot(fig)

pm25_line = (
    df_clean_iter
    .groupby(["station", "year", "month"])["PM2.5"]
    .mean()
    .reset_index()
)

df_plot = pm25_line[pm25_line["station"] == station_pilihan]

bulan_tahun_terburuk = (
    df_plot
    .sort_values("PM2.5", ascending=False)
    .iloc[0]
)
bulan_terburuk = int(bulan_tahun_terburuk["month"])
tahun_terburuk = int(bulan_tahun_terburuk["year"])

df_waktu_terburuk = df_clean_iter[
    (df_clean_iter["station"] == station_pilihan) &
    (df_clean_iter["month"] == bulan_terburuk) &
    (df_clean_iter["year"] == tahun_terburuk)
]

pm25_per_jam = df_waktu_terburuk.groupby("hour")["PM2.5"].mean()
jam_terburuk = int(pm25_per_jam.idxmax())
jam_sebelumnya = jam_terburuk - 1 if jam_terburuk > 0 else 23

kolom_metric = ["PM2.5", "CO", "DEWP", "WSPM"]
data_jam_ini = df_waktu_terburuk[df_waktu_terburuk["hour"] == jam_terburuk][kolom_metric].mean()
data_jam_lalu = df_waktu_terburuk[df_waktu_terburuk["hour"] == jam_sebelumnya][kolom_metric].mean()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig, ax = plt.subplots(figsize=(8, 5))
    max_pm25 = df_plot["PM2.5"].max()
    tahun_tertinggi = df_plot[df_plot["PM2.5"] == max_pm25]["year"].unique()

    for year in sorted(df_plot["year"].unique()):
        yearly_data = df_plot[df_plot["year"] == year]
        if year in tahun_tertinggi:
            ax.plot(yearly_data["month"], yearly_data["PM2.5"], marker="o", linewidth=2.5, label=str(year))
        else:
            ax.plot(yearly_data["month"], yearly_data["PM2.5"], color="gray", alpha=0.3, linewidth=1)

    ax.set_title(f"Tren Bulanan PM2.5 – Stasiun {station_pilihan}")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata PM2.5")
    ax.set_xticks(range(1, 13))
    ax.legend(title="Tahun (PM2.5 Tertinggi)")
    ax.grid(True)
    st.pyplot(fig)

with col_chart2:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pm25_per_jam.index, pm25_per_jam.values, marker='o', color='crimson', linewidth=2, label='PM2.5 per Jam')
    ax.axvline(jam_terburuk, color='blue', linestyle='--', label=f'Jam Terburuk: {jam_terburuk}:00')
    ax.scatter(jam_terburuk, pm25_per_jam[jam_terburuk], color='blue', s=100)

    ax.set_title(f"PM2.5 per Jam – Bulan {bulan_terburuk}/{tahun_terburuk}")
    ax.set_xlabel("Jam (24h)")
    ax.set_ylabel("Rata-rata PM2.5")
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

st.subheader(
    f"🕒 Jam Terburuk: {jam_terburuk}:00 "
    f"(Bulan {bulan_terburuk}, Tahun {tahun_terburuk})"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("PM2.5", f"{data_jam_ini['PM2.5']:.2f}", f"{data_jam_ini['PM2.5'] - data_jam_lalu['PM2.5']:.2f}")
col2.metric("CO", f"{data_jam_ini['CO']:.2f}", f"{data_jam_ini['CO'] - data_jam_lalu['CO']:.2f}")
col3.metric("DEWP", f"{data_jam_ini['DEWP']:.2f}", f"{data_jam_ini['DEWP'] - data_jam_lalu['DEWP']:.2f}")
col4.metric("WSPM", f"{data_jam_ini['WSPM']:.2f}", f"{data_jam_ini['WSPM'] - data_jam_lalu['WSPM']:.2f}")

st.markdown(
    f"""
### 📌 Insight Singkat
- Stasiun **{station_pilihan}** mengalami tingkat PM2.5 tertinggi pada  
  **bulan {bulan_terburuk} tahun {tahun_terburuk}**.
- Puncak polusi terjadi pada **jam {jam_terburuk}:00**.
- Kenaikan PM2.5 berkorelasi dengan perubahan **CO**, **DEWP**, dan  
  **kecepatan angin (WSPM)** dibandingkan jam sebelumnya.
"""
)
