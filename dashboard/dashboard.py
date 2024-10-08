import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Mengatur tampilan
st.title("Dashboard Kualitas Udara di Tiantan")

# Memuat dataset
data_path = "main_data.csv"
df = pd.read_csv(data_path)

# Mendapatkan nilai minimum dan maksimum tahun dari dataset
min_year = int(df['year'].min())
max_year = int(df['year'].max())

# Sidebar untuk memilih rentang tahun
st.sidebar.header("Filter Data")
selected_years = st.sidebar.slider("Pilih Rentang Tahun", min_year, max_year, (min_year, max_year))

# Memfilter data sesuai dengan rentang tahun yang dipilih
filtered_data = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

# Menampilkan data sesuai tahun yang dipilih
st.subheader(f"Data Kualitas Udara dari Tahun {selected_years[0]} hingga {selected_years[1]}")
st.write(filtered_data.head())  # Tampilkan data yang sudah difilter

# Layout untuk membuat dua kolom visualisasi
col1, col2 = st.columns(2)

# Analisis 1: Pengaruh polutan terhadap suhu dan kelembapan
with col1:
    st.subheader("Pengaruh Tingkat Polusi terhadap Suhu dan Kelembapan")

    # Visualisasi hubungan PM2.5, TEMP, dan DEWP
    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=filtered_data, x='PM2.5', y='TEMP', ax=ax1, label='TEMP', color='blue')
    sns.scatterplot(data=filtered_data, x='PM2.5', y='DEWP', ax=ax1, label='DEWP', color='green')
    ax1.set_title(f"Pengaruh PM2.5 terhadap Suhu dan Kelembapan ({selected_years[0]}-{selected_years[1]})")
    ax1.set_xlabel("PM2.5")
    ax1.set_ylabel("Suhu / Kelembapan")
    ax1.legend()
    st.pyplot(fig1)

# Analisis 2: Pola Konsentrasi Polutan
with col2:
    st.subheader("Tren Konsentrasi Polutan Sepanjang Tahun")

    # Menghitung rata-rata tahunan untuk CO dan NO2 dalam rentang tahun yang dipilih
    yearly_avg = df.groupby('year')[['CO', 'NO2']].mean().reset_index()
    yearly_avg_filtered = yearly_avg[(yearly_avg['year'] >= selected_years[0]) & (yearly_avg['year'] <= selected_years[1])]

    # Visualisasi tren
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=yearly_avg_filtered, x='year', y='CO', ax=ax2, label='CO', marker='o', color='red')
    sns.lineplot(data=yearly_avg_filtered, x='year', y='NO2', ax=ax2, label='NO2', marker='o', color='orange')
    ax2.set_title(f"Rata-rata Konsentrasi CO dan NO2 per Tahun ({selected_years[0]}-{selected_years[1]})")
    ax2.set_xlabel("Tahun")
    ax2.set_ylabel("Konsentrasi (µg/m³)")
    ax2.legend()
    st.pyplot(fig2)

# Visualisasi tambahan berdasarkan tahun yang dipilih
st.subheader(f"Analisis Detil untuk Tahun {selected_years[0]} hingga {selected_years[1]}")

# Boxplot untuk distribusi suhu berdasarkan PM2.5
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_data, x='PM2.5', y='TEMP', ax=ax3)
ax3.set_title(f"Distribusi Suhu berdasarkan PM2.5 ({selected_years[0]}-{selected_years[1]})")
st.pyplot(fig3)

# Menyediakan insight tambahan
st.subheader("Insight dan Kesimpulan")
st.write("Dari analisis ini, kita bisa melihat bagaimana polusi udara berpengaruh terhadap suhu dan kelembapan. Selain itu, tren rata-rata konsentrasi polutan menunjukkan perubahan signifikan selama rentang waktu yang dipilih. Pastikan untuk memantau kualitas udara secara berkala untuk memahami dampaknya terhadap kesehatan dan lingkungan.")
