import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Konfigurasi Halaman Dashboard
st.set_page_config(page_title="Admin Monitoring - Bubble Wrap", layout="wide")

st.title("📊 Dashboard Monitoring: Efisiensi Material Bubble Wrap")
st.subheader("Admin Control & Real-Time Analytics")

DB_NAME = "bubble_wrap_system.db"

# Fungsi untuk mengambil data dari SQLite
def load_data_from_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT * FROM tabel_transaksi ORDER BY waktu DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Konversi kolom waktu ke format datetime pandas
        if not df.empty and 'waktu' in df.columns:
            df['datetime'] = pd.to_datetime(df['waktu'])
            df['tanggal'] = df['datetime'].dt.date
            
        return df
    except Exception as e:
        return pd.DataFrame()

# Load data awal
df_raw = load_data_from_db()

# --- SIDEBAR: FILTER TANGGAL ---
st.sidebar.header("🔍 Filter Dashboard")

if not df_raw.empty and 'tanggal' in df_raw.columns:
    min_date = df_raw['tanggal'].min()
    max_date = df_raw['tanggal'].max()
    
    # Widget Date Input rentang tanggal
    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter dataframe berdasarkan tanggal yang dipilih
    # Konversi start_date dan end_date menjadi tipe date agar kompatibel
    mask = (df_raw['tanggal'] >= start_date) & (df_raw['tanggal'] <= end_date)
    df = df_raw.loc[mask]
else:
    df = df_raw
    start_date, end_date = None, None

# Tombol Refresh Manual di Sidebar
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Copyright © 2026 Muryan Awaludin</p>", unsafe_allow_html=True)

# --- MAIN DASHBOARD (KPI METRICS) ---
col1, col2, col3 = st.columns(3)

if not df.empty:
    total_meter = df['panjang_meter'].sum()
    total_paket = len(df)
    
    col1.metric("Total Penggunaan (Filter)", f"{total_meter:.2f} Meter")
    col2.metric("Total Paket Diproses", f"{total_paket} Paket")
    col3.metric("Status Koneksi Database", "🟢 Connected (Live)")

    st.markdown("---")

    # --- GRAFIK & TABEL ---
    col_chart, col_table = st.columns([1, 1])

    with col_chart:
        st.subheader("📈 Tren Penggunaan per Waktu")
        if 'waktu' in df.columns and len(df) > 0:
            chart_data = df.set_index('waktu')['panjang_meter']
            st.line_chart(chart_data)

    with col_table:
        st.subheader("📋 Log Transaksi Pemotongan")
        # Tampilkan kolom yang relevan saja (sembunyikan kolom helper datetime)
        display_cols = [col for col in df.columns if col not in ['datetime', 'tanggal']]
        st.dataframe(df[display_cols], use_container_width=True)

else:
    st.warning("⚠️ Tidak ada data transaksi yang ditemukan pada rentang tanggal tersebut.")