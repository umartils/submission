import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as ticker

sns.set(style='dark')

data = pd.read_csv('main_data.csv')

data['dteday'] = pd.to_datetime(data['dteday'])

minDate = data['dteday'].min()
maxDate = data['dteday'].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=minDate,
        max_value=maxDate,
        value=[minDate, maxDate]
    )
df = data
df = data[(data["dteday"] >= str(start_date)) & 
          (data["dteday"] <= str(end_date))]

def kelompok_waktu(jam):
    if 5 <= jam < 12:
        return 'Pagi'
    elif 12 <= jam < 15:
        return 'Siang'
    elif 15 <= jam < 18:
        return 'Sore'
    else:
        return 'Malam'

st.header('Bike Sharing Dataset Dashboard')

df_season = df.groupby(by='season').agg({'cnt': 'sum'})

st.subheader("Jumlah Penyewaan Berdasarkan Musim")
color_map = {1: '#D3D3D3', 2: '#D3D3D3', 3: '#90CAF9', 4: '#D3D3D3'}
colors_season = [color_map[season] for season in df_season.index]

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(x=df_season.index, height=df_season['cnt'], color=colors_season)
ax.set_xlabel('Musim (season)')
ax.set_ylabel('Jumlah Penyewaan (cnt)')
ax.set_xticks([1, 2, 3, 4], ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)
with st.expander("**Insight**"):
    st.write(
        """
        - Penyewa paling banyak terjadi ketika di musim gugur dengan total **1061129** penyewa
        - Pola tersebut konsisten baik di tahun 2011 maupun di tahun 2012
        """
    )
    
df_hr = df.groupby(by='hr').agg({
    'cnt' : 'sum'
})
st.subheader("Jumlah Penyewaan Berdasarkan Jam Penyewaan")
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_hr.index, df_hr.values, color='blue', marker='o', linestyle='-')  # Line chart
ax.set_xlabel('Jam (hr)')
ax.set_ylabel('Jumlah Penyewaan (cnt)')
ax.grid(True)   
st.pyplot(fig)
with st.expander("**Insight**"):
    st.write(
        """
        - Berdasarkan grafik terlihat jumlah penyewaan terbanyak terjadi pada sore hari
        - Titik tertinggi penyewaan berada di jam 17 dengan total **336860** penyewa
        - Pola tersebut konsisten baik di tahun 2011 maupun di tahun 2012
        """
    )

st.subheader("Jumlah Penyewaan Berdasarkan Status Libur")
df_holiday = df.groupby('holiday')['cnt'].sum()
colors_holiday = ['#90CAF9', '#D3D3D3']  

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(x=df_holiday.index, height=df_holiday.values, color=colors_holiday)
ax.set_xlabel('Holiday')
ax.set_ylabel('Jumlah Penyewaan (cnt)')
ax.set_xticks([0, 1])
ax.set_xticklabels(['Non-Holiday', 'Holiday'])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)
with st.expander("**Insight**"):
    st.write(
        """
        - Berdasarkan grafik terlihat jumlah penyewaan terbanyak terjadi pada selain hari libur
        - Dari data tersebut dapat disimpulkan bahwa sepeda yang disewa digunakan untuk kebutuhan produktivitas penyewa
        - Data ini dapat digunakan untuk menyesuaikan kebutuhan sepeda yaitu dengan memaksimalkan momen di waktu kerja atau selain hari libur
        """
    )

df['kelompok_waktu'] = df['hr'].apply(kelompok_waktu)
df_waktu = df.groupby(by='kelompok_waktu')['cnt'].sum()
color_waktu_map = {'Malam': '#90CAF9', 'Pagi': '#D3D3D3',  'Siang': '#D3D3D3', 'Sore': '#D3D3D3'}  # Warna khusus untuk Musim Gugur (season 3)
colors_waktu = [color_waktu_map[waktu] for waktu in df_waktu.index]

st.subheader("Analisis Lanjutan : Frekuensi Penyewaan Berdasarkan Waktu Penggunaan")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(x=df_waktu.index, height=df_waktu.values, color=colors_waktu)
# ax.set_xlabel('Waktu Penyewaan')
ax.set_ylabel('Jumlah Penyewaan (cnt)') 
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)
with st.expander("**Insight**"):
    st.write(
        """
        - Berdasarkan data penyewaan berdasarkan kelompok waktu, penyewaan pada malam hari memiliki frekuensi paling tinggi dengan total penyewaan mencapai 1jt penyewaan
        - Hal tersebut wajar saja karena rentang waktu untuk malam hari lebih panjang dibandingkan waktu lainnya.
        """
    )
